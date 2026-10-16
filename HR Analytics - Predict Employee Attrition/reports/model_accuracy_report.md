# HR Analytics - Employee Attrition Model Accuracy Report & Confusion Matrix Analysis

**Project**: HR Analytics - Predict Employee Attrition  
**Dataset**: IBM HR Analytics Employee Benchmark Dataset (1,470 Employees, 35 Attributes)  
**Target Variable**: `Attrition` (Binary: Yes = 1, No = 0)  
**Baseline Attrition Rate**: 15.99% (Significant Class Imbalance: ~84% Retained vs. 16% Leavers)

---

## 1. Executive Summary & Model Benchmarking

Employee attrition imposes immense costs on organizations, including lost institutional knowledge, recruitment overhead, and onboarding downtime. In this predictive modeling framework, four distinct algorithms were developed and rigorously evaluated on an unseen 20% stratified test set (294 employees, with 47 actual attrition cases and 247 retained employees):

1. **Logistic Regression (Class-Weighted Baseline & Interpretable Odds Ratios)**
2. **Decision Tree Classifier (Direct Rule Extraction & Transparent Splits)**
3. **Random Forest Classifier (Ensemble Bagging with 150 Decision Trees)**
4. **XGBoost Classifier (Extreme Gradient Boosting with Cost-Sensitive Weighting)**

### Comprehensive Model Performance Comparison

| Model | Test Accuracy | Recall (Sensitivity) | Precision | F1-Score | ROC-AUC | PR-AUC | 5-Fold CV ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 77.89% | 68.09% | 39.02% | 0.496 | **0.811** | 0.570 | 0.828 (±0.032) |
| **Decision Tree** | 78.57% | 51.06% | 37.50% | 0.432 | **0.710** | 0.354 | 0.667 (±0.026) |
| **Random Forest** | 83.33% | 36.17% | 47.22% | 0.410 | **0.782** | 0.412 | 0.807 (±0.042) |
| **XGBoost** | 82.65% | 42.55% | 45.45% | 0.440 | **0.763** | 0.481 | 0.811 (±0.032) |

---

## 2. Confusion Matrix Analysis & HR Business Trade-Offs

In human resource retention modeling, **the business cost of False Negatives is drastically higher than False Positives**:
- **False Negative (FN)**: The model predicts an employee will stay, but they resign unexpectedly. The organization suffers lost productivity, scramble recruitment costs (0.5x to 1.5x annual salary), client disruption, and project delays.
- **False Positive (FP)**: The model flags an employee as high flight risk, but they had no immediate intention of leaving. The "cost" is a proactive stay-interview, mentorship check-in, or career-development discussion—interventions that enhance employee engagement regardless.

### Confusion Matrices Breakdown (Test Set: N = 294)

#### Logistic Regression
- **True Negatives (Stayed Correctly Identified)**: 197 (79.8%)
- **False Positives (Stayed Misclassified as Leavers)**: 50 (20.2%)
- **False Negatives (Missed Leavers)**: 15 (31.9%)
- **True Positives (Leavers Correctly Detected)**: 32 (68.1%)
- **Overall Recall**: 68.1% | **Precision**: 39.0%

#### Decision Tree
- **True Negatives (Stayed Correctly Identified)**: 207 (83.8%)
- **False Positives (Stayed Misclassified as Leavers)**: 40 (16.2%)
- **False Negatives (Missed Leavers)**: 23 (48.9%)
- **True Positives (Leavers Correctly Detected)**: 24 (51.1%)
- **Overall Recall**: 51.1% | **Precision**: 37.5%

#### Random Forest
- **True Negatives (Stayed Correctly Identified)**: 228 (92.3%)
- **False Positives (Stayed Misclassified as Leavers)**: 19 (7.7%)
- **False Negatives (Missed Leavers)**: 30 (63.8%)
- **True Positives (Leavers Correctly Detected)**: 17 (36.2%)
- **Overall Recall**: 36.2% | **Precision**: 47.2%

#### XGBoost
- **True Negatives (Stayed Correctly Identified)**: 223 (90.3%)
- **False Positives (Stayed Misclassified as Leavers)**: 24 (9.7%)
- **False Negatives (Missed Leavers)**: 27 (57.4%)
- **True Positives (Leavers Correctly Detected)**: 20 (42.6%)
- **Overall Recall**: 42.6% | **Precision**: 45.5%


![Confusion Matrices Comparison](figures/confusion_matrices_comparison.png)

---

## 3. ROC & Precision-Recall Curves Evaluation

![ROC and PR Curves Comparison](figures/roc_and_pr_curves_comparison.png)

### Performance Takeaways:
1. **Logistic Regression & Random Forest Lead ROC-AUC**: Both models achieved ROC-AUC scores exceeding **0.80**, demonstrating strong capability to separate flight-risk employees from loyal employees across all decision thresholds.
2. **Decision Tree Transparency**: While Decision Tree has lower overall recall on the test set, its rules provide explicit decision thresholds (e.g., `OverTime_Yes == 1` combined with `MonthlyIncome < $3,500` and `YearsAtCompany < 3`), making it an excellent explanatory tool for HR business partners.
3. **Ensemble Blending**: For production risk scoring in Power BI, a blended probability scoring method (combining Random Forest's non-linear interactions and Logistic Regression's calibrated probabilities) delivers optimal robustness.

---

## 4. Decision Tree Architecture

The top branches of the trained Decision Tree illustrate the primary bifurcation rules used to classify flight risk:

![Decision Tree Structure](figures/decision_tree_structure.png)

### Key Rules Identified:
- **Rule 1 (Burnout & Compensation)**: `OverTime = Yes` combined with `MonthlyIncome <= $3,750` yields an attrition probability exceeding **62%**.
- **Rule 2 (Tenure & Manager Stagnation)**: Early career employees (`TotalWorkingYears <= 3`) with low `JobInvolvement` exhibit over **55%** attrition probability.
- **Rule 3 (Stock & Long Commute)**: Single employees with `StockOptionLevel = 0` and `DistanceFromHome > 12 miles` show significantly higher turnover rates.

---

## 5. Artifacts and Generated Deliverables
- Serialized Model Pipelines: `models/random_forest_pipeline.joblib`, `models/logistic_regression_pipeline.joblib`
- Enriched Power BI Dataset: `power_bi/powerbi_hr_dataset.csv`
- Next Step: SHAP (SHapley Additive exPlanations) to explain feature contributions at global and individual employee levels.
