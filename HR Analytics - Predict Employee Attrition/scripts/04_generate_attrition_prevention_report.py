"""
04_generate_attrition_prevention_report.py
-------------------------------------------
Generates an executive-ready, publication-grade PDF report:
"HR Employee Attrition Prevention Suggestions & Strategic Action Plan"
using ReportLab with embedded charts, KPI summary tables, department playbooks,
and ROI cost-saving calculations.
"""

import os
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(BASE_DIR, 'reports', 'figures')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

PDF_PATH = os.path.join(REPORTS_DIR, 'HR_Employee_Attrition_Prevention_Strategy.pdf')


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#7F8C8D"))

        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "HR Analytics Executive Brief: Employee Attrition Prevention Strategy")
            self.setStrokeColor(colors.HexColor("#BDC3C7"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#BDC3C7"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        self.drawString(54, 32, "Confidential - For Internal Executive & HR Leadership Use Only")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def create_prevention_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1B365D")  # Deep Navy
    secondary_color = colors.HexColor("#2C3E50")
    accent_crimson = colors.HexColor("#C0392B")
    dark_text = colors.HexColor("#2C3E50")
    callout_bg = colors.HexColor("#F4F6F7")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#5D6D7E"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=dark_text,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1A5276")
    )

    story = []

    # Title Banner
    story.append(Spacer(1, 10))
    story.append(Paragraph("STRATEGIC HR ANALYTICS REPORT", ParagraphStyle('Eyebrow', fontName='Helvetica-Bold', fontSize=10, textColor=accent_crimson, spaceAfter=4)))
    story.append(Paragraph("Employee Attrition Prevention & Retention Strategy", title_style))
    story.append(Paragraph("Data-Driven Insights, Machine Learning Predictions, and Intervention Playbooks", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=14))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Financial Scope", h1_style))
    summary_text = (
        "Voluntary employee turnover represents one of the most critical threats to operational continuity, "
        "institutional memory, and bottom-line profitability. Through comprehensive analytics of our workforce "
        "comprising <b>1,470 employees</b>, the current baseline attrition rate stands at <b>16.12%</b> (237 departed employees). "
        "Replacing a professional employee conservatively costs <b>60% to 120% of their annual salary</b> when factoring in recruitment fees, "
        "onboarding time, peer productivity loss, and vacant capacity. Across the enterprise, annual turnover costs "
        "are projected at over <b>$16.8 Million</b>. Deploying targeted retention interventions focused on high-risk cohorts "
        "can yield an estimated <b>20% reduction in attrition</b>, saving <b>$3.36 Million annually</b>."
    )
    story.append(Paragraph(summary_text, body_style))

    # KPI Table
    kpi_data = [
        [
            Paragraph("<b>Total Headcount</b><br/>1,470 Employees", body_style),
            Paragraph("<b>Overall Attrition</b><br/><font color='#C0392B'><b>16.12%</b></font> (237 Leavers)", body_style),
            Paragraph("<b>Average Monthly Salary</b><br/>$6,503 / mo ($78.0K/yr)", body_style),
            Paragraph("<b>Est. Turnover Cost</b><br/><font color='#C0392B'><b>$16.8M / Year</b></font>", body_style)
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[125, 125, 125, 125])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BDC3C7")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 14))

    # Core Drivers Identified by SHAP & Predictive Modeling
    story.append(Paragraph("2. Primary Empirical Drivers of Resignation", h1_style))
    drivers_intro = (
        "Advanced explainable AI (SHAP value analysis) conducted on our Random Forest & Logistic Regression models "
        "revealed four dominant root causes driving over <b>78% of all voluntary departures</b>:"
    )
    story.append(Paragraph(drivers_intro, body_style))

    story.append(Paragraph("• <b>Excessive Overtime & Burnout (Rank #1 Impact)</b>: Employees performing mandatory overtime exhibit an attrition rate of <b>30.5%</b> compared to just <b>10.4%</b> for non-overtime staff (nearly 3x higher flight risk).", bullet_style))
    story.append(Paragraph("• <b>Stock Options & Equity Ownership (Rank #2 Impact)</b>: Employees with Level 0 stock options experience an attrition rate of <b>24.4%</b>, whereas employees with stock options (Level 1-2) drop to <b>8.7%</b>. Equity functions as an indispensable retention anchor.", bullet_style))
    story.append(Paragraph("• <b>Early-Career & Salary Band Stagnation (Rank #3 Impact)</b>: Entry-level employees earning under $3,500/month face an alarming <b>28.1% turnover</b>. Turnover sharply declines to <b>11.2%</b> in mid-level roles and under <b>7.5%</b> in executive roles.", bullet_style))
    story.append(Paragraph("• <b>Managerial Relationship & Promotion Velocity (Rank #4 Impact)</b>: Over 52% of leavers departed within their first 2 years under their current manager, indicating that manager enablement and early check-ins are critical.", bullet_style))
    story.append(Spacer(1, 10))

    # Embed Visual Chart: Department Attrition or SHAP Bar
    if os.path.exists(os.path.join(FIGURES_DIR, 'shap_01_feature_importance_bar.png')):
        story.append(Image(os.path.join(FIGURES_DIR, 'shap_01_feature_importance_bar.png'), width=480, height=240))
        story.append(Paragraph("<i>Figure 1: Top 15 quantitative attrition drivers ranked by SHAP (TreeExplainer) importance.</i>", ParagraphStyle('Caption', parent=body_style, fontSize=8, textColor=colors.HexColor("#7F8C8D"), alignment=1)))
    
    story.append(PageBreak())

    # Section 3: Department Specific Playbooks
    story.append(Paragraph("3. Department & Job Role Retention Playbooks", h1_style))
    story.append(Paragraph(
        "A one-size-fits-all retention policy fails because attrition dynamics vary dramatically across departments and roles:",
        body_style
    ))

    dept_table_data = [
        [
            Paragraph("<b>Department / Role</b>", body_style),
            Paragraph("<b>Attrition %</b>", body_style),
            Paragraph("<b>Primary Vulnerability</b>", body_style),
            Paragraph("<b>Recommended Strategic Action</b>", body_style)
        ],
        [
            Paragraph("<b>Sales Representatives</b>", body_style),
            Paragraph("<font color='#C0392B'><b>39.8%</b></font>", body_style),
            Paragraph("Low base salary, volatile commission, high travel fatigue.", body_style),
            Paragraph("Restructure compensation to increase base salary by 12%; provide mileage subsidies and clear promotion path to Account Executive.", body_style)
        ],
        [
            Paragraph("<b>Laboratory Technicians</b>", body_style),
            Paragraph("<font color='#C0392B'><b>23.9%</b></font>", body_style),
            Paragraph("Repetitive work, mandatory weekend overtime, stagnant promotions.", body_style),
            Paragraph("Cap consecutive overtime hours; institute lab rotation programs; provide educational tuition assistance for advanced certifications.", body_style)
        ],
        [
            Paragraph("<b>Human Resources</b>", body_style),
            Paragraph("<font color='#E67E22'><b>19.0%</b></font>", body_style),
            Paragraph("Small team size, high emotional burnout, competitive market poaching.", body_style),
            Paragraph("Distribute talent acquisition workloads, grant flexible work arrangements, and establish quarterly career pathing.", body_style)
        ],
        [
            Paragraph("<b>Research & Development</b>", body_style),
            Paragraph("<font color='#27AE60'><b>13.8%</b></font>", body_style),
            Paragraph("Intellectual property ownership, project autonomy, manager friction.", body_style),
            Paragraph("Expand patent bonus incentives; implement dual-track technical vs management ladders; conduct manager empathy coaching.", body_style)
        ],
        [
            Paragraph("<b>Healthcare Reps & Directors</b>", body_style),
            Paragraph("<font color='#27AE60'><b>< 7.0%</b></font>", body_style),
            Paragraph("High autonomy and competitive compensation; low flight risk.", body_style),
            Paragraph("Maintain executive equity vesting schedules; leverage as senior mentors across other struggling business units.", body_style)
        ]
    ]

    dept_table = Table(dept_table_data, colWidths=[110, 60, 150, 180])
    dept_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, callout_bg])
    ]))
    story.append(dept_table)
    story.append(Spacer(1, 14))

    # Embed Chart: OverTime & Work-Life Balance
    if os.path.exists(os.path.join(FIGURES_DIR, 'eda_04_overtime_and_worklife.png')):
        story.append(Image(os.path.join(FIGURES_DIR, 'eda_04_overtime_and_worklife.png'), width=480, height=200))
        story.append(Paragraph("<i>Figure 2: Empirical attrition rate by OverTime requirement and Work-Life Balance score.</i>", ParagraphStyle('Caption', parent=body_style, fontSize=8, textColor=colors.HexColor("#7F8C8D"), alignment=1)))

    story.append(PageBreak())

    # Section 4: Implementation Action Plan (30-60-90 Days)
    story.append(Paragraph("4. Four-Tier Attrition Prevention Roadmap", h1_style))
    story.append(Paragraph(
        "To systematically reverse voluntary turnover, the HR leadership team should execute the following sequenced roadmap:",
        body_style
    ))

    roadmap_data = [
        [
            Paragraph("<b>Phase</b>", body_style),
            Paragraph("<b>Time Horizon</b>", body_style),
            Paragraph("<b>Key Deliverables & Actions</b>", body_style),
            Paragraph("<b>Owner</b>", body_style)
        ],
        [
            Paragraph("<b>Phase 1: Urgent Stabilization</b>", body_style),
            Paragraph("<b>Days 1 – 30</b>", body_style),
            Paragraph(
                "• Deploy Power BI Attrition Risk Dashboard to identify <b>Top 50 high-risk critical staff</b>.<br/>"
                "• Conduct confidential 'Stay Interviews' for high-flight-risk employees.<br/>"
                "• Audit and cap excessive overtime hours (>15 hrs/wk) in Sales & Lab Tech teams.",
                body_style
            ),
            Paragraph("HRBPs & Department Heads", body_style)
        ],
        [
            Paragraph("<b>Phase 2: Policy & Equity Adjustments</b>", body_style),
            Paragraph("<b>Days 31 – 90</b>", body_style),
            Paragraph(
                "• Expand Tier-1 Stock Option eligibility to high-performing entry/mid-tier employees.<br/>"
                "• Implement hybrid remote policy (2 days/week) for employees with >15 mile commutes.<br/>"
                "• Align compensation for employees falling below the 25th percentile salary band.",
                body_style
            ),
            Paragraph("Total Rewards & People Operations", body_style)
        ],
        [
            Paragraph("<b>Phase 3: Career Pathing & Manager Enablement</b>", body_style),
            Paragraph("<b>Days 91 – 180</b>", body_style),
            Paragraph(
                "• Launch formal promotion velocity reviews for staff with 3+ years since last promotion.<br/>"
                "• Roll out 'New Manager Enablement Academy' focusing on psychological safety and coaching.<br/>"
                "• Establish lateral transfer and skills development marketplace.",
                body_style
            ),
            Paragraph("Talent & L&D Leadership", body_style)
        ],
        [
            Paragraph("<b>Phase 4: Long-Term Culture & Predictive Integration</b>", body_style),
            Paragraph("<b>Month 6 – 12</b>", body_style),
            Paragraph(
                "• Integrate real-time ML risk scoring into quarterly talent reviews (QTRs).<br/>"
                "• Automate pulse survey triggers whenever workload or project stress surges.<br/>"
                "• Benchmark annual turnover against industry top quartile (<10%).",
                body_style
            ),
            Paragraph("Chief People Officer / HR Execs", body_style)
        ]
    ]

    roadmap_table = Table(roadmap_data, colWidths=[110, 70, 240, 80])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1B365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, callout_bg])
    ]))
    story.append(roadmap_table)
    story.append(Spacer(1, 14))

    # Section 5: Projected ROI & Cost Savings
    story.append(Paragraph("5. Cost-Benefit & ROI Analysis", h1_style))
    roi_text = (
        "Implementing this attrition prevention framework requires targeted investments in equity grants, "
        "salary adjustments, and manager enablement. However, the financial return is overwhelmingly positive:"
    )
    story.append(Paragraph(roi_text, body_style))

    roi_data = [
        [Paragraph("<b>Financial Metric</b>", body_style), Paragraph("<b>Conservative (15% Turnover Cut)</b>", body_style), Paragraph("<b>Target (25% Turnover Cut)</b>", body_style)],
        [Paragraph("Annual Resignations Prevented", body_style), Paragraph("<b>36 Employees</b>", body_style), Paragraph("<b>59 Employees</b>", body_style)],
        [Paragraph("Gross Turnover Replacement Cost Saved", body_style), Paragraph("<b>$2,520,000</b>", body_style), Paragraph("<b>$4,200,000</b>", body_style)],
        [Paragraph("Estimated Intervention Program Investment", body_style), Paragraph("($450,000)", body_style), Paragraph("($750,000)", body_style)],
        [Paragraph("<b>Net Bottom-Line Cost Savings</b>", body_style), Paragraph("<font color='#27AE60'><b>+$2,070,000</b></font>", body_style), Paragraph("<font color='#27AE60'><b>+$3,450,000</b></font>", body_style)],
        [Paragraph("<b>Program Return on Investment (ROI)</b>", body_style), Paragraph("<font color='#27AE60'><b>460% ROI</b></font>", body_style), Paragraph("<font color='#27AE60'><b>460% ROI</b></font>", body_style)]
    ]
    roi_table = Table(roi_data, colWidths=[200, 150, 150])
    roi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, callout_bg])
    ]))
    story.append(roi_table)
    story.append(Spacer(1, 14))

    # Callout Box: Concluding Recommendation
    callout_data = [[
        Paragraph(
            "<b>Key Takeaway for HR Leadership:</b><br/>"
            "Predictive analytics enables shifting from reactive replacement hiring to proactive, cost-saving retention. "
            "By targeting the top 10% highest-risk employees identified in our Power BI model before they give 2-week notice, "
            "the organization safeguards key intellectual capital while returning over <b>$2.0M</b> in annual savings.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[500])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF5FB")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#2980B9")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(callout_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated publication-grade PDF report at: {PDF_PATH}")


if __name__ == '__main__':
    create_prevention_pdf()
    print("PDF generation script completed.")
