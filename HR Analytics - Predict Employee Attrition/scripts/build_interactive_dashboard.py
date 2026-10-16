"""
build_interactive_dashboard.py
-------------------------------
Generates a standalone, interactive HTML Power BI simulation dashboard.
Integrates Chart.js, real data from powerbi_hr_dataset.csv, dynamic slicers,
employee flight risk search table, and retention ROI calculator.
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'power_bi', 'powerbi_hr_dataset.csv')
HTML_OUTPUT_PATH = os.path.join(BASE_DIR, 'power_bi', 'interactive_dashboard.html')


def build_dashboard():
    df = pd.read_csv(DATA_PATH)
    
    # Pre-aggregate summary stats for fast rendering
    records = df.to_dict(orient='records')
    records_json = json.dumps(records)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Power BI Simulation: HR Analytics & Attrition Prediction</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg-dark: #0f172a;
      --card-bg: #1e293b;
      --card-border: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-blue: #38bdf8;
      --accent-indigo: #6366f1;
      --accent-red: #ef4444;
      --accent-green: #10b981;
      --accent-amber: #f59e0b;
      --pbi-yellow: #f2c811;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}

    /* Top Power BI Ribbon */
    .pbi-header {{
      background: #182234;
      border-bottom: 2px solid #2d3b50;
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .pbi-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .pbi-logo {{
      width: 28px;
      height: 28px;
      background: var(--pbi-yellow);
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      color: #000;
      font-size: 16px;
    }}

    .pbi-title {{
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.3px;
    }}

    .pbi-subtitle {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .header-badge {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
      padding: 5px 12px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}

    /* Main Container */
    .dashboard-container {{
      display: flex;
      flex: 1;
    }}

    /* Sidebar / Navigation */
    .sidebar {{
      width: 250px;
      background: #111a2e;
      border-right: 1px solid var(--card-border);
      padding: 18px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .nav-label {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      padding: 6px 12px;
      margin-top: 10px;
    }}

    .nav-btn {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      border-radius: 8px;
      color: var(--text-muted);
      background: transparent;
      border: none;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      text-align: left;
      transition: all 0.2s ease;
      width: 100%;
    }}

    .nav-btn:hover {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-main);
    }}

    .nav-btn.active {{
      background: var(--card-bg);
      color: var(--accent-blue);
      border-left: 3px solid var(--accent-blue);
    }}

    /* Filter Area */
    .filter-panel {{
      margin-top: auto;
      padding: 14px;
      background: #0b1120;
      border-radius: 8px;
      border: 1px solid var(--card-border);
    }}

    .filter-panel h4 {{
      font-size: 12px;
      margin-bottom: 10px;
      color: var(--text-muted);
    }}

    .filter-select {{
      width: 100%;
      padding: 8px 10px;
      background: #1e293b;
      border: 1px solid #475569;
      border-radius: 6px;
      color: #fff;
      font-size: 12px;
      margin-bottom: 8px;
      outline: none;
    }}

    /* Main Content Area */
    .content-area {{
      flex: 1;
      padding: 24px;
      overflow-y: auto;
      background: #0b1120;
    }}

    /* KPI Cards Ribbon */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px 20px;
      position: relative;
      overflow: hidden;
      transition: transform 0.2s;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
    }}

    .kpi-title {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 600;
    }}

    .kpi-value {{
      font-size: 28px;
      font-weight: 800;
      margin: 6px 0 4px 0;
      letter-spacing: -0.5px;
    }}

    .kpi-subtext {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .kpi-card.red .kpi-value {{ color: var(--accent-red); }}
    .kpi-card.green .kpi-value {{ color: var(--accent-green); }}
    .kpi-card.blue .kpi-value {{ color: var(--accent-blue); }}
    .kpi-card.amber .kpi-value {{ color: var(--accent-amber); }}

    /* Grid for Charts */
    .charts-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }}

    .charts-grid.single-col {{
      grid-template-columns: 1fr;
    }}

    .chart-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      min-height: 340px;
      display: flex;
      flex-direction: column;
    }}

    .chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}

    .chart-title {{
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .chart-badge {{
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(255,255,255,0.06);
      padding: 3px 8px;
      border-radius: 6px;
    }}

    .chart-container {{
      flex: 1;
      position: relative;
    }}

    /* Data Table */
    .table-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      margin-top: 24px;
    }}

    .table-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      gap: 12px;
    }}

    .search-box {{
      padding: 8px 14px;
      background: #0f172a;
      border: 1px solid #475569;
      border-radius: 8px;
      color: #fff;
      font-size: 13px;
      width: 300px;
      outline: none;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    th {{
      background: #111a2e;
      color: var(--text-muted);
      text-align: left;
      padding: 10px 14px;
      font-weight: 600;
      border-bottom: 1px solid var(--card-border);
    }}

    td {{
      padding: 10px 14px;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      color: var(--text-main);
    }}

    tr:hover td {{
      background: rgba(255,255,255,0.02);
    }}

    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }}

    .badge-high {{ background: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }}
    .badge-med {{ background: rgba(245, 158, 11, 0.2); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.4); }}
    .badge-low {{ background: rgba(16, 185, 129, 0.2); color: #a7f3d0; border: 1px solid rgba(16, 185, 129, 0.4); }}
    .badge-urgent {{ background: #dc2626; color: #fff; font-weight: 700; }}

    /* ROI Calculator Widget */
    .roi-widget {{
      background: linear-gradient(135deg, #1e293b, #0f172a);
      border: 1px solid #3b82f6;
      border-radius: 12px;
      padding: 20px;
      margin-top: 24px;
    }}

    .slider-container {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin: 16px 0;
    }}

    input[type=range] {{
      flex: 1;
      height: 6px;
      border-radius: 3px;
      background: #334155;
      outline: none;
      cursor: pointer;
    }}

    .roi-results {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 14px;
    }}

    .roi-stat {{
      background: rgba(0,0,0,0.25);
      padding: 12px 16px;
      border-radius: 8px;
      border: 1px solid #334155;
    }}

    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
    }}
  </style>
</head>
<body>

  <!-- Power BI Header -->
  <header class="pbi-header">
    <div class="pbi-brand">
      <div class="pbi-logo">Pb</div>
      <div>
        <div class="pbi-title">HR Analytics: Employee Attrition & Predictive Retention Hub</div>
        <div class="pbi-subtitle">Power BI Executive Dashboard Simulation | 1,470 Employees Evaluated</div>
      </div>
    </div>
    <div style="display: flex; gap: 12px; align-items: center;">
      <span class="header-badge">ML Model: Logistic Reg + Random Forest (ROC-AUC: 0.81)</span>
      <span class="header-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3);">Data: Live Processed</span>
    </div>
  </header>

  <div class="dashboard-container">
    <!-- Sidebar Navigation & Slicers -->
    <aside class="sidebar">
      <div class="nav-label">Report Pages</div>
      <button class="nav-btn active" onclick="switchTab('tab-exec')">📊 1. Executive Overview</button>
      <button class="nav-btn" onclick="switchTab('tab-dept')">🏢 2. Department & Roles</button>
      <button class="nav-btn" onclick="switchTab('tab-comp')">💰 3. Compensation & Tenure</button>
      <button class="nav-btn" onclick="switchTab('tab-radar')">🎯 4. Retention Action Center</button>

      <!-- Power BI Slicers -->
      <div class="filter-panel">
        <h4>⚡ Power BI Slicers</h4>
        <label style="font-size: 11px; color: var(--text-muted);">Department Filter</label>
        <select id="deptFilter" class="filter-select" onchange="applyFilters()">
          <option value="ALL">All Departments (3)</option>
          <option value="Research & Development">Research & Development</option>
          <option value="Sales">Sales</option>
          <option value="Human Resources">Human Resources</option>
        </select>

        <label style="font-size: 11px; color: var(--text-muted);">OverTime Slicer</label>
        <select id="otFilter" class="filter-select" onchange="applyFilters()">
          <option value="ALL">All OverTime Status</option>
          <option value="Yes">OverTime: Yes</option>
          <option value="No">OverTime: No</option>
        </select>

        <label style="font-size: 11px; color: var(--text-muted);">Flight Risk Tier</label>
        <select id="riskFilter" class="filter-select" onchange="applyFilters()">
          <option value="ALL">All Risk Tiers</option>
          <option value="High Risk (>60%)">High Risk (>60%)</option>
          <option value="Medium Risk (30-60%)">Medium Risk (30-60%)</option>
          <option value="Low Risk (<30%)">Low Risk (<30%)</option>
        </select>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="content-area">

      <!-- Global Top KPI Ribbon (Dynamically updated by slicers) -->
      <div class="kpi-grid">
        <div class="kpi-card blue">
          <div class="kpi-title">Selected Headcount</div>
          <div class="kpi-value" id="kpi-headcount">1,470</div>
          <div class="kpi-subtext">Active: <span id="kpi-active">1,233</span> | Left: <span id="kpi-left">237</span></div>
        </div>
        <div class="kpi-card red">
          <div class="kpi-title">Attrition Rate</div>
          <div class="kpi-value" id="kpi-attrition-rate">16.1%</div>
          <div class="kpi-subtext">Target Threshold: < 12.0%</div>
        </div>
        <div class="kpi-card amber">
          <div class="kpi-title">High-Risk Active Staff</div>
          <div class="kpi-value" id="kpi-high-risk">40</div>
          <div class="kpi-subtext">Require Immediate Intervention</div>
        </div>
        <div class="kpi-card green">
          <div class="kpi-title">Avg Monthly Salary</div>
          <div class="kpi-value" id="kpi-avg-salary">$6,503</div>
          <div class="kpi-subtext">Annual Base: $78.0K</div>
        </div>
        <div class="kpi-card red">
          <div class="kpi-title">Annual Turnover Exposure</div>
          <div class="kpi-value" id="kpi-turnover-cost">$16.8M</div>
          <div class="kpi-subtext">Replacement @ 0.6x - 1.2x salary</div>
        </div>
      </div>

      <!-- TAB 1: EXECUTIVE OVERVIEW -->
      <div id="tab-exec" class="tab-content active">
        <div class="charts-grid">
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Department Attrition Rate & Leavers Breakdown</div>
              <span class="chart-badge">Power BI Bar Visual</span>
            </div>
            <div class="chart-container">
              <canvas id="chartDeptRate"></canvas>
            </div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">OverTime Impact: Turnover Multiplier (3.0x Risk)</div>
              <span class="chart-badge">Power BI Donut Visual</span>
            </div>
            <div class="chart-container">
              <canvas id="chartOvertime"></canvas>
            </div>
          </div>
        </div>

        <div class="charts-grid">
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Top 8 Machine Learning Drivers of Resignation (SHAP Impact)</div>
              <span class="chart-badge">Explainable AI</span>
            </div>
            <div class="chart-container">
              <canvas id="chartShapDrivers"></canvas>
            </div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Attrition Rate (%) by Salary Band</div>
              <span class="chart-badge">Compensation Analysis</span>
            </div>
            <div class="chart-container">
              <canvas id="chartSalaryBand"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 2: DEPARTMENT & ROLES -->
      <div id="tab-dept" class="tab-content">
        <div class="charts-grid single-col">
          <div class="chart-card" style="min-height: 400px;">
            <div class="chart-header">
              <div class="chart-title">Attrition Rate Across All 9 Job Roles (Ranked)</div>
              <span class="chart-badge">Role Vulnerability Diagnostic</span>
            </div>
            <div class="chart-container">
              <canvas id="chartJobRoles"></canvas>
            </div>
          </div>
        </div>
        <div class="charts-grid">
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Business Travel Frequency vs. Attrition</div>
              <span class="chart-badge">Travel Exhaustion</span>
            </div>
            <div class="chart-container">
              <canvas id="chartTravel"></canvas>
            </div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Commute Distance Band vs. Attrition Rate</div>
              <span class="chart-badge">Distance Strain</span>
            </div>
            <div class="chart-container">
              <canvas id="chartDistance"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: COMPENSATION & CAREER -->
      <div id="tab-comp" class="tab-content">
        <div class="charts-grid">
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Impact of Stock Option Grants on Retention</div>
              <span class="chart-badge">Equity Golden Handcuffs</span>
            </div>
            <div class="chart-container">
              <canvas id="chartStockOptions"></canvas>
            </div>
          </div>
          <div class="chart-card">
            <div class="chart-header">
              <div class="chart-title">Promotion Stagnation vs. Company Tenure</div>
              <span class="chart-badge">Career Velocity</span>
            </div>
            <div class="chart-container">
              <canvas id="chartPromotion"></canvas>
            </div>
          </div>
        </div>

        <!-- Built-in ROI Calculator Widget -->
        <div class="roi-widget">
          <h3 style="color: var(--accent-blue); margin-bottom: 6px;">💼 Interactive Retention Cost Savings & ROI Calculator</h3>
          <p style="font-size: 13px; color: var(--text-muted);">Simulate enterprise dollar savings achieved by proactively intervening with high-flight-risk employees:</p>
          <div class="slider-container">
            <span style="font-weight: 700; font-size: 14px;">Target Attrition Reduction:</span>
            <input type="range" id="roiSlider" min="5" max="40" value="20" step="5" oninput="updateROI()">
            <span id="roiSliderVal" style="font-weight: 800; font-size: 16px; color: var(--accent-blue);">20% Cut</span>
          </div>
          <div class="roi-results">
            <div class="roi-stat">
              <div style="font-size: 11px; color: var(--text-muted);">Resignations Prevented / Year</div>
              <div id="roi-saved-count" style="font-size: 22px; font-weight: 800; color: var(--accent-green); margin-top: 4px;">47 Employees</div>
            </div>
            <div class="roi-stat">
              <div style="font-size: 11px; color: var(--text-muted);">Direct Turnover Cost Saved</div>
              <div id="roi-saved-cost" style="font-size: 22px; font-weight: 800; color: var(--accent-green); margin-top: 4px;">$3,360,000</div>
            </div>
            <div class="roi-stat">
              <div style="font-size: 11px; color: var(--text-muted);">Net ROI (Assumes $600K Program Budget)</div>
              <div id="roi-pct" style="font-size: 22px; font-weight: 800; color: var(--accent-blue); margin-top: 4px;">460% Net ROI</div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 4: RETENTION ACTION RADAR -->
      <div id="tab-radar" class="tab-content">
        <div class="table-card">
          <div class="table-controls">
            <div>
              <h3 style="font-size: 16px; font-weight: 700;">Employee Flight Risk Radar & Action Prescriptions</h3>
              <p style="font-size: 12px; color: var(--text-muted);">Machine Learning Risk Scores (0-100%) and personalized HR interventions</p>
            </div>
            <input type="text" id="employeeSearch" class="search-box" placeholder="🔍 Search Employee #, Role, or Action..." oninput="renderTable()">
          </div>
          
          <div style="overflow-x: auto; max-height: 500px;">
            <table id="employeeTable">
              <thead>
                <tr>
                  <th>Emp #</th>
                  <th>Department</th>
                  <th>Job Role</th>
                  <th>Salary ($/mo)</th>
                  <th>OverTime</th>
                  <th>Tenure</th>
                  <th>Flight Risk %</th>
                  <th>Risk Tier</th>
                  <th>Recommended Retention Action</th>
                </tr>
              </thead>
              <tbody id="employeeTableBody">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
          <div id="table-footer" style="padding-top: 12px; font-size: 12px; color: var(--text-muted); display: flex; justify-content: space-between;">
            <span>Showing top matches</span>
            <span id="matchCount"></span>
          </div>
        </div>
      </div>

    </main>
  </div>

  <script>
    // Embedded dataset
    const RAW_DATA = {records_json};

    let charts = {{}};

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
      
      document.getElementById(tabId).classList.add('active');
      event.currentTarget.classList.add('active');
    }}

    function getFilteredData() {{
      const dept = document.getElementById('deptFilter').value;
      const ot = document.getElementById('otFilter').value;
      const risk = document.getElementById('riskFilter').value;

      return RAW_DATA.filter(r => {{
        if (dept !== 'ALL' && r.Department !== dept) return false;
        if (ot !== 'ALL' && r.OverTime !== ot) return false;
        if (risk !== 'ALL' && r.Attrition_Risk_Tier !== risk) return false;
        return true;
      }});
    }}

    function updateKPIs(data) {{
      const total = data.length;
      const leavers = data.filter(r => r.Attrition === 'Yes').length;
      const active = total - leavers;
      const rate = total > 0 ? ((leavers / total) * 100).toFixed(1) : '0.0';
      const highRisk = data.filter(r => r.Attrition === 'No' && r.Retention_Action === 'Urgent Retention Check-in').length;
      
      const totalCost = data
        .filter(r => r.Attrition === 'Yes')
        .reduce((sum, r) => sum + (r.Estimated_Replacement_Cost || 0), 0);
      
      const avgSalary = total > 0 
        ? Math.round(data.reduce((sum, r) => sum + r.MonthlyIncome, 0) / total) 
        : 0;

      document.getElementById('kpi-headcount').innerText = total.toLocaleString();
      document.getElementById('kpi-active').innerText = active.toLocaleString();
      document.getElementById('kpi-left').innerText = leavers.toLocaleString();
      document.getElementById('kpi-attrition-rate').innerText = rate + '%';
      document.getElementById('kpi-high-risk').innerText = highRisk.toLocaleString();
      document.getElementById('kpi-avg-salary').innerText = '$' + avgSalary.toLocaleString();
      document.getElementById('kpi-turnover-cost').innerText = '$' + (totalCost / 1000000).toFixed(1) + 'M';
    }}

    function renderTable() {{
      const query = document.getElementById('employeeSearch').value.toLowerCase();
      const data = getFilteredData();
      const tbody = document.getElementById('employeeTableBody');
      tbody.innerHTML = '';

      const filtered = data.filter(r => {{
        return (
          String(r.EmployeeNumber).includes(query) ||
          r.JobRole.toLowerCase().includes(query) ||
          r.Department.toLowerCase().includes(query) ||
          r.Retention_Action.toLowerCase().includes(query) ||
          r.Attrition_Risk_Tier.toLowerCase().includes(query)
        );
      }});

      // Show top 100 matches for high performance
      const slice = filtered.slice(0, 100);

      slice.forEach(r => {{
        const tr = document.createElement('tr');
        
        let badgeClass = 'badge-low';
        if (r.Attrition_Risk_Tier.includes('High')) badgeClass = 'badge-high';
        else if (r.Attrition_Risk_Tier.includes('Medium')) badgeClass = 'badge-med';

        let actionBadge = '';
        if (r.Retention_Action.includes('Urgent')) {{
          actionBadge = `<span class="badge badge-urgent">${{r.Retention_Action}}</span>`;
        }} else if (r.Retention_Action.includes('Watchlist')) {{
          actionBadge = `<span class="badge badge-med">${{r.Retention_Action}}</span>`;
        }} else if (r.Retention_Action.includes('Departed')) {{
          actionBadge = `<span class="badge" style="background:#475569; color:#cbd5e1;">Departed</span>`;
        }} else {{
          actionBadge = `<span class="badge badge-low">${{r.Retention_Action}}</span>`;
        }}

        tr.innerHTML = `
          <td><strong>#${{r.EmployeeNumber}}</strong></td>
          <td>${{r.Department}}</td>
          <td>${{r.JobRole}}</td>
          <td>$${{r.MonthlyIncome.toLocaleString()}}</td>
          <td style="color:${{r.OverTime === 'Yes' ? '#ef4444' : '#10b981'}}; font-weight:600;">${{r.OverTime}}</td>
          <td>${{r.YearsAtCompany}} yrs</td>
          <td style="font-weight:700;">${{(r.Attrition_Risk_Score * 100).toFixed(1)}}%</td>
          <td><span class="badge ${{badgeClass}}">${{r.Attrition_Risk_Tier}}</span></td>
          <td>${{actionBadge}}</td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('matchCount').innerText = `${{filtered.length}} employees found`;
    }}

    function initCharts() {{
      const data = RAW_DATA;

      // 1. Dept Rate Chart
      const depts = ['Sales', 'Research & Development', 'Human Resources'];
      const deptRates = depts.map(d => {{
        const sub = data.filter(r => r.Department === d);
        const leavers = sub.filter(r => r.Attrition === 'Yes').length;
        return ((leavers / sub.length) * 100).toFixed(1);
      }});

      charts.dept = new Chart(document.getElementById('chartDeptRate'), {{
        type: 'bar',
        data: {{
          labels: depts,
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: deptRates,
            backgroundColor: ['#ef4444', '#38bdf8', '#f59e0b'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 2. Overtime Donut
      const otYes = data.filter(r => r.OverTime === 'Yes');
      const otNo = data.filter(r => r.OverTime === 'No');
      const otYesRate = ((otYes.filter(r => r.Attrition === 'Yes').length / otYes.length) * 100).toFixed(1);
      const otNoRate = ((otNo.filter(r => r.Attrition === 'Yes').length / otNo.length) * 100).toFixed(1);

      charts.overtime = new Chart(document.getElementById('chartOvertime'), {{
        type: 'doughnut',
        data: {{
          labels: [`OverTime Required (${{otYesRate}}% Attrition)`, `Standard Hours (${{otNoRate}}% Attrition)`],
          datasets: [{{
            data: [otYesRate, otNoRate],
            backgroundColor: ['#ef4444', '#38bdf8'],
            borderColor: '#1e293b',
            borderWidth: 3
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1' }} }}
          }}
        }}
      }});

      // 3. SHAP Top Drivers Bar
      const shapDrivers = [
        'Works OverTime', 'StockOptionLevel = 0', 'MonthlyIncome < $3.5K',
        'Younger Age (<28)', 'Low Satisfaction Score', 'TotalWorkingYears < 3',
        'YearsWithCurrManager < 2', 'DistanceFromHome > 15mi'
      ];
      const shapScores = [0.048, 0.034, 0.033, 0.032, 0.029, 0.025, 0.023, 0.015];

      charts.shap = new Chart(document.getElementById('chartShapDrivers'), {{
        type: 'bar',
        data: {{
          labels: shapDrivers,
          datasets: [{{
            label: 'SHAP Value (Feature Push)',
            data: shapScores,
            backgroundColor: '#6366f1',
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ ticks: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
          }}
        }}
      }});

      // 4. Salary Band
      const salaryBands = ['<$3.5K (Entry)', '$3.5K-$7K (Mid)', '$7K-$12K (Senior)', '$12K+ (Exec)'];
      const bandRates = [28.1, 11.2, 15.1, 7.5];

      charts.salary = new Chart(document.getElementById('chartSalaryBand'), {{
        type: 'bar',
        data: {{
          labels: salaryBands,
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: bandRates,
            backgroundColor: ['#ef4444', '#38bdf8', '#f59e0b', '#10b981'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 5. Job Roles Breakdown
      const roles = [
        'Sales Representative', 'Laboratory Technician', 'Human Resources',
        'Sales Executive', 'Research Scientist', 'Manufacturing Director',
        'Healthcare Representative', 'Manager', 'Research Director'
      ];
      const roleRates = [39.8, 23.9, 19.0, 17.5, 16.1, 6.9, 6.9, 4.9, 2.5];

      charts.roles = new Chart(document.getElementById('chartJobRoles'), {{
        type: 'bar',
        data: {{
          labels: roles,
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: roleRates,
            backgroundColor: roleRates.map(r => r > 16.1 ? '#ef4444' : '#38bdf8'),
            borderRadius: 6
          }}]
        }},
        options: {{
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            y: {{ ticks: {{ color: '#cbd5e1' }} }}
          }}
        }}
      }});

      // 6. Travel Frequency
      charts.travel = new Chart(document.getElementById('chartTravel'), {{
        type: 'bar',
        data: {{
          labels: ['Travel Frequently', 'Travel Rarely', 'Non-Travel'],
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: [24.9, 15.0, 8.0],
            backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 7. Commute Distance
      charts.distance = new Chart(document.getElementById('chartDistance'), {{
        type: 'line',
        data: {{
          labels: ['Near (1-5 mi)', 'Moderate (6-15 mi)', 'Far (>15 mi)'],
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: [13.2, 16.8, 22.4],
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            fill: true,
            tension: 0.3,
            pointRadius: 6,
            pointBackgroundColor: '#ef4444'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 8. Stock Options Impact
      charts.stock = new Chart(document.getElementById('chartStockOptions'), {{
        type: 'bar',
        data: {{
          labels: ['Level 0 (No Options)', 'Level 1 (Standard Grant)', 'Level 2 (Senior Grant)', 'Level 3 (Exec Grant)'],
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: [24.4, 9.4, 7.6, 17.6],
            backgroundColor: ['#ef4444', '#10b981', '#10b981', '#f59e0b'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      // 9. Promotion Stagnation
      charts.promo = new Chart(document.getElementById('chartPromotion'), {{
        type: 'bar',
        data: {{
          labels: ['Recent (0-1 yr)', 'Moderate (2-4 yrs)', 'Stagnant (5+ yrs)'],
          datasets: [{{
            label: 'Attrition Rate (%)',
            data: [15.8, 14.9, 19.8],
            backgroundColor: ['#38bdf8', '#f59e0b', '#ef4444'],
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8', callback: v => v + '%' }} }},
            x: {{ ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});
    }}

    function applyFilters() {{
      const filtered = getFilteredData();
      updateKPIs(filtered);
      renderTable();
    }}

    function updateROI() {{
      const cutPct = parseInt(document.getElementById('roiSlider').value);
      document.getElementById('roiSliderVal').innerText = cutPct + '% Cut';

      const totalDepartures = 237;
      const avgCostPerDeparture = 71000; // ~$71K average replacement cost
      const prevented = Math.round(totalDepartures * (cutPct / 100));
      const savedCost = prevented * avgCostPerDeparture;
      const programCost = 600000;
      const netSavings = savedCost - programCost;
      const roi = Math.round((netSavings / programCost) * 100);

      document.getElementById('roi-saved-count').innerText = prevented + ' Employees';
      document.getElementById('roi-saved-cost').innerText = '$' + (savedCost / 1000000).toFixed(2) + 'M';
      document.getElementById('roi-pct').innerText = roi + '% Net ROI';
    }}

    window.onload = function() {{
      initCharts();
      updateKPIs(RAW_DATA);
      renderTable();
      updateROI();
    }};
  </script>
</body>
</html>
"""
    with open(HTML_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated standalone interactive Power BI simulation dashboard at: {HTML_OUTPUT_PATH}")


if __name__ == '__main__':
    build_dashboard()
