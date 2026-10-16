"""
run_pipeline.py
----------------
Master orchestration script for the HR Analytics Employee Attrition project.
Executes all steps in sequence:
  1. Exploratory Data Analysis & Visualization (01_eda_hr_analytics.py)
  2. Model Training, Evaluation & Accuracy Report (02_model_training_evaluation.py)
  3. SHAP Explainability Analysis (03_shap_explainability.py)
  4. Strategic Retention PDF Report Generation (04_generate_attrition_prevention_report.py)
  5. Interactive Power BI Simulation Dashboard Build (build_interactive_dashboard.py)
"""

import sys
import subprocess
import time

def run_step(script_name, description):
    print(f"\n{'='*70}")
    print(f">> RUNNING: {description}")
    print(f">> Script: {script_name}")
    print(f"{'='*70}\n")
    start = time.time()
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"\n[ERROR] Step '{description}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"\n[SUCCESS] Completed in {elapsed:.2f} seconds.")

def main():
    print("""
======================================================================
     HR ANALYTICS: PREDICT EMPLOYEE ATTRITION END-TO-END PIPELINE
======================================================================
    """)
    run_step("scripts/01_eda_hr_analytics.py", "Exploratory Data Analysis & Feature Engineering")
    run_step("scripts/02_model_training_evaluation.py", "Machine Learning Model Training & Evaluation")
    run_step("scripts/03_shap_explainability.py", "SHAP Explainability & Root-Cause Analysis")
    run_step("scripts/04_generate_attrition_prevention_report.py", "PDF Attrition Prevention Strategy Compilation")
    run_step("scripts/build_interactive_dashboard.py", "Interactive Power BI Dashboard Build")
    
    print("""
======================================================================
                      ALL DELIVERABLES READY!
======================================================================
1. Power BI Ready Dataset:  data/processed/powerbi_hr_dataset.csv
2. Power BI DAX Blueprint:  power_bi/power_bi_data_model_and_dax.md
3. Interactive Dashboard:   power_bi/interactive_dashboard.html
4. Model Accuracy Report:   reports/model_accuracy_report.md
5. Confusion Matrices:      reports/figures/confusion_matrices_comparison.png
6. SHAP Importance Charts:  reports/figures/shap_01_feature_importance_bar.png
7. Attrition Prevention PDF: reports/HR_Employee_Attrition_Prevention_Strategy.pdf
======================================================================
    """)

if __name__ == '__main__':
    main()
