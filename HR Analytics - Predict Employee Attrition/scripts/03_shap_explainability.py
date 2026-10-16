"""
03_shap_explainability.py
--------------------------
Performs SHAP (SHapley Additive exPlanations) analysis to interpret model predictions.
Generates:
  1. Global Feature Importance Bar Plot
  2. SHAP Beeswarm Summary Plot (Feature values vs. directional attrition impact)
  3. Feature Dependence Plots (Monthly Income, OverTime, Age)
  4. Local Waterfall Explanations for High-Risk and Low-Risk Employees
  5. Quantitative SHAP Impact Drivers Table
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'hr_employee_attrition.csv')
FIGURES_DIR = os.path.join(BASE_DIR, 'reports', 'figures')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def clean_feature_names(feature_names):
    """Clean sklearn transformed feature names for human-readable plotting."""
    cleaned = []
    for name in feature_names:
        name = name.replace('num__', '').replace('cat__', '')
        # Clean prefix names
        name = name.replace('BusinessTravel_', 'Travel: ')
        name = name.replace('Department_', 'Dept: ')
        name = name.replace('EducationField_', 'Edu: ')
        name = name.replace('JobRole_', 'Role: ')
        name = name.replace('MaritalStatus_', 'Marital: ')
        name = name.replace('Gender_Male', 'Gender: Male')
        name = name.replace('OverTime_Yes', 'Works OverTime')
        cleaned.append(name)
    return cleaned


def run_shap_analysis():
    print("Loading models and preparing data for SHAP analysis...")
    df = pd.read_csv(RAW_DATA_PATH)

    # Feature engineering matching model_training
    df['IncomePerWorkingYear'] = df['MonthlyIncome'] / (df['TotalWorkingYears'] + 1)
    df['YearsWithoutPromotion'] = df['YearsSinceLastPromotion']
    df['PromotionRatio'] = df['YearsSinceLastPromotion'] / (df['YearsAtCompany'] + 1)
    df['SatisfactionScoreAvg'] = (
        df['EnvironmentSatisfaction'] + df['JobSatisfaction'] + 
        df['RelationshipSatisfaction'] + df['JobInvolvement']
    ) / 4.0

    drop_cols = ['Attrition', 'EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber']
    X = df.drop(columns=drop_cols)

    # Load trained Random Forest pipeline
    rf_pipe = joblib.load(os.path.join(MODELS_DIR, 'random_forest_pipeline.joblib'))
    preprocessor = rf_pipe.named_steps['preprocessor']
    rf_clf = rf_pipe.named_steps['classifier']

    # Transform features
    X_transformed = preprocessor.transform(X)
    raw_feature_names = preprocessor.get_feature_names_out()
    clean_names = clean_feature_names(raw_feature_names)

    X_trans_df = pd.DataFrame(X_transformed, columns=clean_names)

    print(f"Dataset transformed to {X_trans_df.shape[1]} features.")
    
    # Initialize TreeExplainer
    print("Computing SHAP values with TreeExplainer...")
    explainer = shap.TreeExplainer(rf_clf)
    
    # SHAP values for class 1 (Attrition = Yes)
    shap_values = explainer(X_trans_df)
    
    # Check shape: if 3D (samples, features, classes), pick class 1
    if len(shap_values.values.shape) == 3:
        shap_values_class1 = shap_values[:, :, 1]
    else:
        shap_values_class1 = shap_values

    # 1. SHAP Global Feature Importance Bar Chart
    plt.figure(figsize=(11, 7))
    shap.plots.bar(shap_values_class1, max_display=15, show=False)
    plt.title('Top 15 Drivers of Employee Attrition (Mean |SHAP| Value)', fontsize=13, fontweight='bold', pad=14)
    plt.xlabel('Mean |SHAP Value| (Impact on Model Output)', fontsize=11, fontweight='semibold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'shap_01_feature_importance_bar.png'), dpi=300)
    plt.close()
    print("Saved shap_01_feature_importance_bar.png")

    # 2. SHAP Beeswarm Plot (Directional Impact)
    plt.figure(figsize=(12, 8))
    shap.plots.beeswarm(shap_values_class1, max_display=15, show=False)
    plt.title('SHAP Beeswarm Summary: How Employee Factors Drive or Mitigate Attrition', fontsize=13, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'shap_02_summary_beeswarm.png'), dpi=300)
    plt.close()
    print("Saved shap_02_summary_beeswarm.png")

    # 3. Local Explanation: High Risk Employee Case Study
    # Find employee with highest attrition risk probability
    preds_prob = rf_pipe.predict_proba(X)[:, 1]
    high_risk_idx = int(np.argmax(preds_prob))
    low_risk_idx = int(np.argmin(preds_prob))

    print(f"High risk employee index: {high_risk_idx} (Risk Prob = {preds_prob[high_risk_idx]:.2%})")
    print(f"Low risk employee index: {low_risk_idx} (Risk Prob = {preds_prob[low_risk_idx]:.2%})")

    # High Risk Waterfall Plot
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values_class1[high_risk_idx], max_display=10, show=False)
    plt.title(f'Case Study: High-Risk Employee (#{df.iloc[high_risk_idx]["EmployeeNumber"]}) - Flight Risk: {preds_prob[high_risk_idx]:.1%}', fontsize=12, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'shap_03_high_risk_employee_waterfall.png'), dpi=300)
    plt.close()
    print("Saved shap_03_high_risk_employee_waterfall.png")

    # Low Risk Waterfall Plot
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values_class1[low_risk_idx], max_display=10, show=False)
    plt.title(f'Case Study: Loyal / Low-Risk Employee (#{df.iloc[low_risk_idx]["EmployeeNumber"]}) - Flight Risk: {preds_prob[low_risk_idx]:.1%}', fontsize=12, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'shap_04_low_risk_employee_waterfall.png'), dpi=300)
    plt.close()
    print("Saved shap_04_low_risk_employee_waterfall.png")

    # 4. Export Quantitative SHAP Rankings to CSV
    mean_abs_shap = np.abs(shap_values_class1.values).mean(axis=0)
    shap_ranking_df = pd.DataFrame({
        'Feature': clean_names,
        'Mean_Absolute_SHAP': np.round(mean_abs_shap, 4)
    }).sort_values(by='Mean_Absolute_SHAP', ascending=False).reset_index(drop=True)

    # Add business interpretation tag
    def categorize_driver(feat):
        if 'OverTime' in feat or 'WorkLife' in feat:
            return 'Burnout & Work-Life Balance'
        elif 'Income' in feat or 'Rate' in feat or 'Hike' in feat or 'Stock' in feat:
            return 'Compensation & Equity'
        elif 'Promotion' in feat or 'Years' in feat or 'Role' in feat or 'Level' in feat:
            return 'Career Growth & Tenure'
        elif 'Satisfaction' in feat or 'Involvement' in feat or 'Environment' in feat:
            return 'Engagement & Culture'
        elif 'Travel' in feat or 'Distance' in feat:
            return 'Commute & Mobility'
        else:
            return 'Demographics / Personal'

    shap_ranking_df['Category'] = shap_ranking_df['Feature'].apply(categorize_driver)
    shap_ranking_df.to_csv(os.path.join(PROCESSED_DIR, 'shap_top_drivers.csv'), index=False)
    print("Saved shap_top_drivers.csv")

    print("\nTop 10 Most Influential Attrition Drivers according to SHAP:")
    for idx, row in shap_ranking_df.head(10).iterrows():
        print(f"  {idx+1}. {row['Feature']}: {row['Mean_Absolute_SHAP']} ({row['Category']})")


if __name__ == '__main__':
    run_shap_analysis()
    print("SHAP explainability pipeline completed successfully.")
