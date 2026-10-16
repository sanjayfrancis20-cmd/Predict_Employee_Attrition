# HR Analytics - Predict Employee Attrition & Strategic Retention Framework

An end-to-end People Analytics solution designed to understand the empirical root causes of employee turnover, train predictive machine learning classification models, explain predictions using **SHAP values**, and deliver an executive **Power BI dashboard** alongside an intervention strategy report.

---

## 📌 Project Objectives & Scope
- **Objective**: Identify why employees resign, forecast future flight risk with calibrated machine learning models, and empower HR business partners with proactive retention playbooks.
- **Tools**: Python (`pandas`, `seaborn`, `matplotlib`, `scikit-learn`, `xgboost`, `shap`, `reportlab`), Power BI, HTML5/Chart.js.
- **Dataset**: IBM HR Analytics Employee Benchmark Dataset (1,470 Employees, 35 Features).

---

## 📦 Key Deliverables

| Deliverable | Location / File | Description |
| :--- | :--- | :--- |
| **Power BI Interactive Dashboard** | [`power_bi/interactive_dashboard.html`](file:///c:/Users/Bullone/Documents/data%20project/HR%20Analytics%20-%20Predict%20Employee%20Attrition/power_bi/interactive_dashboard.html) | Standalone interactive dashboard simulation featuring live slicers, KPI ribbons, role breakdown, and flight risk search. |
| **Power BI DAX & Data Model** | [`power_bi/power_bi_data_model_and_dax.md`](file:///c:/Users/Bullone/Documents/data%20project/HR%20Analytics%20-%20Predict%20Employee%20Attrition/power_bi/power_bi_data_model_and_dax.md) | Ready-to-use DAX measures, schema design, and step-by-step layout guide for Power BI Desktop. |
| **Power BI Enriched Dataset** | [`power_bi/powerbi_hr_dataset.csv`](file:///c:/Users/Bullone/Documents/data%20project/HR%20Analytics%20-%20Predict%20Employee%20Attrition/power_bi/powerbi_hr_dataset.csv) | Full dataset enriched with ML probability scores, risk tiers (`High`, `Medium`, `Low`), and retention action flags. |
| **Model Accuracy Report** | [`reports/model_accuracy_report.md`](file:///c:/Users/Bullone/Documents/data%20project/HR%20Analytics%20-%20Predict%20Employee%20Attrition/reports/model_accuracy_report.md) | Comprehensive benchmarking of Logistic Regression, Decision Tree, Random Forest, and XGBoost with confusion matrix analysis. |
| **Attrition Prevention Suggestions PDF** | [`reports/HR_Employee_Attrition_Prevention_Strategy.pdf`](file:///c:/Users/Bullone/Documents/data%20project/HR%20Analytics%20-%20Predict%20Employee%20Attrition/reports/HR_Employee_Attrition_Prevention_Strategy.pdf) | Executive-ready PDF report featuring department playbooks, 30-60-90 day roadmap, and a 460% ROI cost savings calculator. |

---

## 📊 Summary of Machine Learning Benchmarking

Evaluated on an unseen 20% stratified test set ($N = 294$, 47 actual attrition cases):

| Algorithm | Test Accuracy | Recall (Sensitivity) | Precision | F1-Score | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Class-Weighted)** | **77.89%** | **68.09%** | **38.55%** | **0.492** | **0.811** | **0.485** |
| **Decision Tree (Tuned Split)** | 78.57% | 51.06% | 37.50% | 0.432 | 0.710 | 0.354 |
| **Random Forest (150 Estimators)** | 83.33% | 36.17% | 47.22% | 0.410 | 0.782 | 0.440 |
| **XGBoost (Cost-Sensitive)** | 82.65% | 42.55% | 45.45% | 0.440 | 0.763 | 0.428 |

> **Business Rationale**: In HR retention, **False Negatives are far costlier than False Positives**. Logistic Regression with balanced weighting detects **68.1% of all voluntary leavers** (ROC-AUC: 0.811), preventing expensive unpredicted resignations.

---

## 🔍 Top Empirical Drivers of Attrition (SHAP Analysis)

1. **Mandatory Overtime (`Works OverTime`)**: 30.5% attrition rate vs. 10.4% without overtime (nearly 3.0x turnover multiplier).
2. **Stock Options (`StockOptionLevel = 0`)**: Employees lacking equity incentives face a 24.4% turnover rate vs. 8.7% for option holders.
3. **Entry Salary Band (`MonthlyIncome < $3,500`)**: 28.1% turnover in entry roles vs. 11.2% in mid-level roles.
4. **Early Tenure & Manager Relationship**: Over 52% of leavers depart within the first 2 years under their current manager.
5. **Commute Distance (`> 15 miles`)**: High commute distance elevates flight risk to 22.4%.

---

## 🚀 How to Run the Pipeline

To regenerate all exploratory analyses, models, figures, and deliverables in one command:

```bash
python run_pipeline.py
```

To open the interactive Power BI dashboard simulation:
- Open [`power_bi/interactive_dashboard.html`](file:///c:/Users/Bullone/Documents/data%20project/HR%20Analytics%20-%20Predict%20Employee%20Attrition/power_bi/interactive_dashboard.html) in your browser.
