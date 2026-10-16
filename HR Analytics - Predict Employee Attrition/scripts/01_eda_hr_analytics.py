"""
01_eda_hr_analytics.py
-----------------------
Performs Exploratory Data Analysis (EDA) on HR Analytics Employee Attrition dataset.
Analyzes department-wise attrition, salary bands, promotion stagnation, work-life balance,
and generates publication-quality visualization charts and summary tables.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette(['#2b5c8f', '#d9534f', '#5cb85c', '#f0ad4e', '#5bc0de', '#737373'])
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'hr_employee_attrition.csv')
FIGURES_DIR = os.path.join(BASE_DIR, 'reports', 'figures')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_and_engineer_features():
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Loaded raw dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

    # Attrition numeric
    df['AttritionNumeric'] = (df['Attrition'] == 'Yes').astype(int)

    # Salary Bands
    bins_salary = [0, 3500, 7000, 12000, np.inf]
    labels_salary = ['Entry (<$3.5K)', 'Mid-Level ($3.5K-$7K)', 'Senior ($7K-$12K)', 'Executive ($12K+)']
    df['SalaryBand'] = pd.cut(df['MonthlyIncome'], bins=bins_salary, labels=labels_salary, right=False)

    # Tenure Category
    bins_tenure = [-1, 2, 5, 10, np.inf]
    labels_tenure = ['0-2 Years (Early)', '3-5 Years (Developing)', '6-10 Years (Established)', '10+ Years (Veteran)']
    df['TenureCategory'] = pd.cut(df['YearsAtCompany'], bins=bins_tenure, labels=labels_tenure)

    # Promotion Stagnation
    df['PromotionStagnation'] = df['YearsSinceLastPromotion'].apply(
        lambda x: 'Stagnant (>=5 yrs)' if x >= 5 else ('Moderate (2-4 yrs)' if x >= 2 else 'Recent (0-1 yr)')
    )

    # Age Group
    bins_age = [17, 25, 35, 45, 55, 100]
    labels_age = ['Under 25', '25-34', '35-44', '45-54', '55+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age)

    # Distance Band
    bins_dist = [0, 5, 15, 100]
    labels_dist = ['Near (1-5 mi)', 'Moderate (6-15 mi)', 'Far (>15 mi)']
    df['DistanceBand'] = pd.cut(df['DistanceFromHome'], bins=bins_dist, labels=labels_dist)

    # Mappings for satisfaction scales
    satisfaction_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
    df['JobSatisfaction_Label'] = df['JobSatisfaction'].map(satisfaction_map)
    df['EnvironmentSatisfaction_Label'] = df['EnvironmentSatisfaction'].map(satisfaction_map)
    df['WorkLifeBalance_Label'] = df['WorkLifeBalance'].map({1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'})

    return df


def generate_eda_visualizations(df):
    overall_attrition_rate = df['AttritionNumeric'].mean() * 100
    print(f"Overall Attrition Rate: {overall_attrition_rate:.2f}%")

    # 1. Department-wise Attrition Plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Counts
    dept_counts = df.groupby(['Department', 'Attrition']).size().unstack(fill_value=0)
    dept_counts.plot(kind='bar', stacked=True, ax=axes[0], color=['#2b5c8f', '#d9534f'], width=0.6)
    axes[0].set_title('Employee Headcount by Department & Attrition', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Department', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Number of Employees', fontsize=11, fontweight='semibold')
    axes[0].tick_params(axis='x', rotation=15)
    axes[0].legend(['Retained (No)', 'Attrition (Yes)'], frameon=True)
    
    # Percentage rates
    dept_rate = df.groupby('Department')['AttritionNumeric'].mean().reset_index()
    dept_rate['AttritionRatePct'] = dept_rate['AttritionNumeric'] * 100
    bars = axes[1].bar(dept_rate['Department'], dept_rate['AttritionRatePct'], color=['#e67e22', '#3498db', '#e74c3c'], width=0.55)
    axes[1].axhline(overall_attrition_rate, color='black', linestyle='--', linewidth=1.5, label=f'Avg Attrition ({overall_attrition_rate:.1f}%)')
    axes[1].set_title('Attrition Rate (%) by Department', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Department', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='semibold')
    axes[1].tick_params(axis='x', rotation=15)
    axes[1].set_ylim(0, max(dept_rate['AttritionRatePct']) * 1.25)
    for bar in bars:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    axes[1].legend(loc='upper right', frameon=True)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'eda_01_department_attrition.png'), dpi=300)
    plt.close()
    print("Saved eda_01_department_attrition.png")

    # 2. Salary Band Attrition Analysis
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Boxplot of Monthly Income by Attrition & Department
    sns.boxplot(data=df, x='Department', y='MonthlyIncome', hue='Attrition', palette=['#2b5c8f', '#d9534f'], ax=axes[0])
    axes[0].set_title('Monthly Income Distribution by Department & Attrition', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Department', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Monthly Income ($)', fontsize=11, fontweight='semibold')
    axes[0].tick_params(axis='x', rotation=15)

    # Salary Band Attrition Rate
    salary_rate = df.groupby('SalaryBand', observed=False)['AttritionNumeric'].agg(['count', 'mean']).reset_index()
    salary_rate['AttritionRatePct'] = salary_rate['mean'] * 100
    colors_bars = ['#d9534f' if r > overall_attrition_rate else '#2b5c8f' for r in salary_rate['AttritionRatePct']]
    bars2 = axes[1].bar(salary_rate['SalaryBand'].astype(str), salary_rate['AttritionRatePct'], color=colors_bars, width=0.55)
    axes[1].axhline(overall_attrition_rate, color='black', linestyle='--', linewidth=1.5, label=f'Avg Attrition ({overall_attrition_rate:.1f}%)')
    axes[1].set_title('Attrition Rate (%) by Salary Band', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Salary Band', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='semibold')
    axes[1].tick_params(axis='x', rotation=20)
    axes[1].set_ylim(0, max(salary_rate['AttritionRatePct']) * 1.25)
    for bar in bars2:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.6, f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    axes[1].legend(loc='upper right', frameon=True)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'eda_02_salary_band_attrition.png'), dpi=300)
    plt.close()
    print("Saved eda_02_salary_band_attrition.png")

    # 3. Promotions & Tenure Analysis
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Years Since Last Promotion Attrition Rate
    promo_rate = df.groupby('YearsSinceLastPromotion')['AttritionNumeric'].agg(['count', 'mean']).reset_index()
    promo_rate = promo_rate[promo_rate['count'] >= 10]  # Filter small samples
    promo_rate['AttritionRatePct'] = promo_rate['mean'] * 100

    sns.barplot(data=promo_rate, x='YearsSinceLastPromotion', y='AttritionRatePct', color='#34495e', ax=axes[0])
    axes[0].axhline(overall_attrition_rate, color='#e74c3c', linestyle='--', linewidth=1.5, label=f'Avg Attrition ({overall_attrition_rate:.1f}%)')
    axes[0].set_title('Attrition Rate (%) vs. Years Since Last Promotion', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Years Since Last Promotion', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='semibold')
    axes[0].legend(frameon=True)

    # Promotion Stagnation & Tenure Category
    stagnation_cross = df.groupby(['TenureCategory', 'PromotionStagnation'], observed=False)['AttritionNumeric'].mean().unstack() * 100
    stagnation_cross.plot(kind='bar', ax=axes[1], colormap='viridis', width=0.7)
    axes[1].set_title('Attrition Rate (%) by Tenure & Promotion Recency', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Company Tenure Category', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='semibold')
    axes[1].tick_params(axis='x', rotation=20)
    axes[1].legend(title='Promotion Recency', frameon=True)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'eda_03_promotions_and_tenure.png'), dpi=300)
    plt.close()
    print("Saved eda_03_promotions_and_tenure.png")

    # 4. OverTime, Job Satisfaction & Work-Life Balance
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Overtime attrition
    ot_df = df.groupby(['OverTime', 'Attrition']).size().unstack(fill_value=0)
    ot_rate = df.groupby('OverTime')['AttritionNumeric'].mean() * 100
    bars_ot = axes[0].bar(['No OverTime', 'OverTime Required'], ot_rate.values, color=['#2b5c8f', '#d9534f'], width=0.45)
    axes[0].axhline(overall_attrition_rate, color='black', linestyle='--', linewidth=1.5, label=f'Avg Attrition ({overall_attrition_rate:.1f}%)')
    axes[0].set_title('Impact of OverTime on Attrition Rate (%)', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_ylabel('Attrition Rate (%)', fontsize=11, fontweight='semibold')
    axes[0].set_ylim(0, max(ot_rate.values) * 1.25)
    for bar in bars_ot:
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.6, f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    axes[0].legend(frameon=True)

    # WorkLifeBalance & Overtime Interaction Heatmap
    pivot_wlb_ot = df.pivot_table(index='WorkLifeBalance_Label', columns='OverTime', values='AttritionNumeric', aggfunc='mean') * 100
    pivot_wlb_ot = pivot_wlb_ot.reindex(['Bad', 'Good', 'Better', 'Best'])
    sns.heatmap(pivot_wlb_ot, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1], cbar_kws={'label': 'Attrition Rate (%)'}, annot_kws={'fontweight': 'bold', 'size': 11})
    axes[1].set_title('Attrition Rate (%) by Work-Life Balance & Overtime', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Overtime Status', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Work-Life Balance Rating', fontsize=11, fontweight='semibold')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'eda_04_overtime_and_worklife.png'), dpi=300)
    plt.close()
    print("Saved eda_04_overtime_and_worklife.png")

    # 5. Job Role Attrition Rate Ranking
    plt.figure(figsize=(12, 6))
    role_rate = df.groupby('JobRole')['AttritionNumeric'].agg(['count', 'mean']).reset_index()
    role_rate['AttritionRatePct'] = role_rate['mean'] * 100
    role_rate = role_rate.sort_values(by='AttritionRatePct', ascending=True)

    palette_roles = ['#d9534f' if r > overall_attrition_rate else '#2b5c8f' for r in role_rate['AttritionRatePct']]
    bars_roles = plt.barh(role_rate['JobRole'], role_rate['AttritionRatePct'], color=palette_roles, height=0.6)
    plt.axvline(overall_attrition_rate, color='black', linestyle='--', linewidth=1.5, label=f'Avg Attrition ({overall_attrition_rate:.1f}%)')
    plt.title('Attrition Rate (%) Across Job Roles', fontsize=14, fontweight='bold', pad=12)
    plt.xlabel('Attrition Rate (%)', fontsize=11, fontweight='semibold')
    plt.ylabel('Job Role', fontsize=11, fontweight='semibold')
    plt.xlim(0, max(role_rate['AttritionRatePct']) * 1.15)
    for bar in bars_roles:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2., f'{width:.1f}%', ha='left', va='center', fontweight='bold', fontsize=10)
    plt.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'eda_05_job_role_attrition.png'), dpi=300)
    plt.close()
    print("Saved eda_05_job_role_attrition.png")

    # 6. Correlation Heatmap of Numeric Drivers
    plt.figure(figsize=(12, 10))
    numeric_cols = [
        'AttritionNumeric', 'Age', 'DailyRate', 'DistanceFromHome', 'EnvironmentSatisfaction',
        'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome',
        'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating', 'RelationshipSatisfaction',
        'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear', 'WorkLifeBalance',
        'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager'
    ]
    corr = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap='vlag', center=0, annot=False, linewidths=0.5, cbar_kws={'shrink': 0.8})
    plt.title('Correlation Matrix of Employee Metrics and Attrition', fontsize=14, fontweight='bold', pad=14)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'eda_06_correlation_heatmap.png'), dpi=300)
    plt.close()
    print("Saved eda_06_correlation_heatmap.png")


def save_summary_tables(df):
    # Department summary
    dept_summary = df.groupby('Department').agg(
        Total_Employees=('Attrition', 'count'),
        Attrition_Count=('AttritionNumeric', 'sum'),
        Attrition_Rate_Pct=('AttritionNumeric', lambda x: round(x.mean() * 100, 2)),
        Avg_Monthly_Income=('MonthlyIncome', lambda x: round(x.mean(), 2)),
        Avg_Years_At_Company=('YearsAtCompany', lambda x: round(x.mean(), 2)),
        Avg_Job_Satisfaction=('JobSatisfaction', lambda x: round(x.mean(), 2))
    ).reset_index()
    dept_summary.to_csv(os.path.join(PROCESSED_DIR, 'department_summary.csv'), index=False)
    print("Saved department_summary.csv")

    # Salary Band summary
    salary_summary = df.groupby('SalaryBand', observed=False).agg(
        Total_Employees=('Attrition', 'count'),
        Attrition_Count=('AttritionNumeric', 'sum'),
        Attrition_Rate_Pct=('AttritionNumeric', lambda x: round(x.mean() * 100, 2)),
        Avg_Monthly_Income=('MonthlyIncome', lambda x: round(x.mean(), 2)),
        Avg_Age=('Age', lambda x: round(x.mean(), 1))
    ).reset_index()
    salary_summary.to_csv(os.path.join(PROCESSED_DIR, 'salary_band_summary.csv'), index=False)
    print("Saved salary_band_summary.csv")

    # Promotion Stagnation summary
    promo_summary = df.groupby('PromotionStagnation').agg(
        Total_Employees=('Attrition', 'count'),
        Attrition_Count=('AttritionNumeric', 'sum'),
        Attrition_Rate_Pct=('AttritionNumeric', lambda x: round(x.mean() * 100, 2)),
        Avg_Monthly_Income=('MonthlyIncome', lambda x: round(x.mean(), 2)),
        Avg_Years_Since_Promotion=('YearsSinceLastPromotion', lambda x: round(x.mean(), 2))
    ).reset_index()
    promo_summary.to_csv(os.path.join(PROCESSED_DIR, 'promotion_stagnation_summary.csv'), index=False)
    print("Saved promotion_stagnation_summary.csv")

    # Job Role summary
    role_summary = df.groupby(['Department', 'JobRole']).agg(
        Total_Employees=('Attrition', 'count'),
        Attrition_Count=('AttritionNumeric', 'sum'),
        Attrition_Rate_Pct=('AttritionNumeric', lambda x: round(x.mean() * 100, 2)),
        Avg_Monthly_Income=('MonthlyIncome', lambda x: round(x.mean(), 2)),
        Overtime_Pct=('OverTime', lambda x: round((x == 'Yes').mean() * 100, 2))
    ).reset_index()
    role_summary.to_csv(os.path.join(PROCESSED_DIR, 'job_role_summary.csv'), index=False)
    print("Saved job_role_summary.csv")


if __name__ == '__main__':
    df = load_and_engineer_features()
    generate_eda_visualizations(df)
    save_summary_tables(df)
    print("EDA completed successfully.")
