# Power BI Implementation Guide: HR Analytics Employee Attrition Dashboard

This guide provides the complete blueprint for building the **Power BI Employee Attrition & Predictive Retention Dashboard**.

---

## 1. Data Connection & Architecture

### Source File
- **Location**: `power_bi/powerbi_hr_dataset.csv`
- **Total Records**: 1,470 Employees
- **Primary Key**: `EmployeeNumber`
- **Target / Status**: `Attrition` ('Yes', 'No')
- **Machine Learning Outputs Included**:
  - `Attrition_Risk_Score`: Probability of voluntary departure (0.000 to 1.000)
  - `Attrition_Risk_Tier`: 'High Risk (>60%)', 'Medium Risk (30-60%)', 'Low Risk (<30%)'
  - `Retention_Action`: 'Urgent Retention Check-in', 'Quarterly Review Watchlist', 'Low Flight Risk / Stable', 'Departed'
  - `Estimated_Replacement_Cost`: Financial impact of replacing each specific employee (based on seniority & annual compensation)

---

## 2. Core DAX Measures (Ready to Copy-Paste)

Create a dedicated DAX measure table named `_Measures` in Power BI:

### A. Headcount & Basic KPIs
```dax
Total Employees = COUNTROWS(powerbi_hr_dataset)
```

```dax
Active Employees = 
CALCULATE(
    COUNTROWS(powerbi_hr_dataset),
    powerbi_hr_dataset[Attrition] = "No"
)
```

```dax
Attrition Count = 
CALCULATE(
    COUNTROWS(powerbi_hr_dataset),
    powerbi_hr_dataset[Attrition] = "Yes"
)
```

```dax
Attrition Rate % = 
DIVIDE([Attrition Count], [Total Employees], 0)
```

### B. Compensation & Cost Analytics
```dax
Avg Monthly Income = 
AVERAGE(powerbi_hr_dataset[MonthlyIncome])
```

```dax
Avg Annual Salary = 
AVERAGE(powerbi_hr_dataset[AnnualSalary])
```

```dax
Total Replacement Cost Exposure = 
CALCULATE(
    SUM(powerbi_hr_dataset[Estimated_Replacement_Cost]),
    powerbi_hr_dataset[Attrition] = "Yes"
)
```

```dax
Potential At-Risk Replacement Cost = 
CALCULATE(
    SUM(powerbi_hr_dataset[Estimated_Replacement_Cost]),
    powerbi_hr_dataset[Attrition] = "No",
    powerbi_hr_dataset[Attrition_Risk_Tier] = "High Risk (>60%)"
)
```

### C. Predictive Risk Metrics
```dax
High Risk Employees Count = 
CALCULATE(
    COUNTROWS(powerbi_hr_dataset),
    powerbi_hr_dataset[Attrition] = "No",
    powerbi_hr_dataset[Attrition_Risk_Tier] = "High Risk (>60%)"
)
```

```dax
Watchlist Employees Count = 
CALCULATE(
    COUNTROWS(powerbi_hr_dataset),
    powerbi_hr_dataset[Attrition] = "No",
    powerbi_hr_dataset[Attrition_Risk_Tier] = "Medium Risk (30-60%)"
)
```

```dax
Average Flight Risk Score = 
CALCULATE(
    AVERAGE(powerbi_hr_dataset[Attrition_Risk_Score]),
    powerbi_hr_dataset[Attrition] = "No"
)
```

### D. Overtime & Work-Life Dynamics
```dax
Overtime Attrition Rate % = 
CALCULATE(
    [Attrition Rate %],
    powerbi_hr_dataset[OverTime] = "Yes"
)
```

```dax
Non-Overtime Attrition Rate % = 
CALCULATE(
    [Attrition Rate %],
    powerbi_hr_dataset[OverTime] = "No"
)
```

```dax
OverTime Turnover Multiplier = 
DIVIDE([Overtime Attrition Rate %], [Non-Overtime Attrition Rate %], 0)
```

---

## 3. Four-Page Dashboard Layout & Visual Guide

### Page 1: Executive Overview & Macro KPIs
* **Top Ribbon Cards**:
  1. `Total Employees` (1,470)
  2. `Attrition Count` (237)
  3. `Attrition Rate %` (16.12% - formatted with Red conditional formatting if > 15%)
  4. `Total Turnover Cost` ($16.8M)
  5. `High Risk Active Staff` (86 employees requiring intervention)
* **Visual 1 (Donut Chart)**: Headcount Split by Attrition (`Active` vs. `Departed`)
* **Visual 2 (Clustered Bar Chart)**: Attrition Rate % by Department (`Sales` 20.6%, `Human Resources` 19.0%, `R&D` 13.8%)
* **Visual 3 (Stacked Bar Chart)**: Headcount & Attrition by Job Role (Highlighting Sales Reps at 39.8% & Lab Techs at 23.9%)
* **Visual 4 (KPI Gauge)**: Enterprise Retention Health Index (Current: 83.88% Retained vs 90.00% Target)

### Page 2: Department & Role Vulnerability Deep Dive
* **Slicers**: Department, Job Role, Gender, Marital Status
* **Visual 1 (Matrix Table)**:
  - Rows: `Department`, `JobRole`
  - Values: `Total Employees`, `Attrition Count`, `Attrition Rate %`, `Avg Monthly Income`, `Overtime %`
  - Conditional formatting: Red data bars for Attrition Rate > 20%
* **Visual 2 (Heatmap / Scatter Plot)**:
  - X-axis: `YearsAtCompany`
  - Y-axis: `MonthlyIncome`
  - Legend: `Attrition`
* **Visual 3 (100% Stacked Column Chart)**: Business Travel Frequency vs. Attrition

### Page 3: Compensation, Equity & Career Velocity
* **Visual 1 (Clustered Column Chart)**: Attrition Rate % across `SalaryBand` (<$3.5K: 28.1%, $3.5K-$7K: 11.2%, $7K-$12K: 15.1%, $12K+: 7.5%)
* **Visual 2 (Bar Chart)**: Impact of Stock Option Level on Attrition (Level 0: 24.4% vs Level 1-2: 8.7%)
* **Visual 3 (Line Chart)**: Attrition Rate vs `YearsSinceLastPromotion` (Spikes at 0-1 yr entry and 7+ years stagnation)
* **Visual 4 (Decomposition Tree)**: Root Cause Breakdown:
  - Analyze: `Attrition Count`
  - Explain By: `OverTime` -> `StockOptionLevel` -> `SalaryBand` -> `JobSatisfaction`

### Page 4: Predictive Retention Action Center (HRBP Flight Risk Radar)
* **Slicers**: `Attrition_Risk_Tier` (High / Medium / Low), `Retention_Action`, `Department`
* **Visual 1 (Summary Cards)**:
  - High-Risk Active Headcount (86)
  - Potential At-Risk Payroll Value ($5.9M)
  - Replacement Cost at Risk ($4.1M)
* **Visual 2 (Interactive Employee Risk Grid)**:
  - Columns: `EmployeeNumber`, `Department`, `JobRole`, `MonthlyIncome`, `OverTime`, `YearsAtCompany`, `YearsWithCurrManager`, `Attrition_Risk_Score`, `Attrition_Risk_Tier`, `Retention_Action`
  - Conditional formatting: Soft red highlight for `High Risk (>60%)`, amber for `Medium Risk`
* **Actionable Tooltip**: Shows top SHAP drivers for that specific employee (e.g. Overtime = Yes, Low Stock Options, Long Commute).

---

## 4. Color Palette Specifications
- **Primary Navy**: `#1B365D`
- **Slate Gray**: `#2C3E50`
- **Attrition Alert (Red/Crimson)**: `#C0392B`
- **Retention Safe (Forest Green)**: `#27AE60`
- **Warning / Medium Risk (Amber)**: `#E67E22`
- **Background Light Neutral**: `#F8F9FA`
