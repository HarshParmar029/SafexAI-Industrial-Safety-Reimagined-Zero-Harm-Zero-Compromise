from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_incident_report(zone, sensor_data, violations, agent_analysis):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                             topMargin=0.75*inch, bottomMargin=0.75*inch,
                             leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    story = []

    # Title Style
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  fontSize=20, textColor=colors.HexColor('#CC0000'),
                                  spaceAfter=6)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'],
                                    fontSize=13, textColor=colors.HexColor('#1a1a2e'),
                                    spaceBefore=12, spaceAfter=4)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'],
                                   fontSize=10, spaceAfter=4)
    critical_style = ParagraphStyle('Critical', parent=styles['Normal'],
                                     fontSize=10, textColor=colors.HexColor('#CC0000'),
                                     spaceAfter=4)

    # Header
    story.append(Paragraph("🛡️ SafexAI — Incident Report", title_style))
    story.append(Paragraph("AI-Powered Industrial Safety Intelligence Platform", styles['Normal']))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#CC0000')))
    story.append(Spacer(1, 0.2*inch))

    # Report Meta
    meta_data = [
        ["Report ID", f"SAF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"],
        ["Generated On", datetime.now().strftime("%d %B %Y, %H:%M:%S")],
        ["Plant Zone", zone],
        ["Report Type", "Compound Risk Incident Report"],
        ["Prepared By", "SafexAI Multi-Agent System"],
        ["Regulatory Framework", "OISD-105, Factory Act 1948, DGFASLI"],
    ]
    meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0,0), (0,-1), colors.white),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.2*inch))

    # Sensor Readings
    story.append(Paragraph("1. Live Sensor Readings at Time of Incident", heading_style))
    sensor_rows = [["Sensor", "Reading", "Threshold", "Status"]]
    for s in sensor_data:
        status_color = colors.HexColor('#CC0000') if s['status'] == 'CRITICAL' else colors.HexColor('#FF8C00')
        sensor_rows.append([s['sensor'], s['reading'], s['threshold'], s['status']])
    
    sensor_table = Table(sensor_rows, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    sensor_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#CC0000')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fff5f5')]),
    ]))
    story.append(sensor_table)
    story.append(Spacer(1, 0.15*inch))

    # Violations
    story.append(Paragraph("2. Regulatory Violations Detected", heading_style))
    for v in violations:
        story.append(Paragraph(f"• {v}", critical_style))
    story.append(Spacer(1, 0.15*inch))

    # AI Analysis Summary
    story.append(Paragraph("3. AI Agent Analysis Summary", heading_style))
    # Truncate if too long
    agent_analysis = agent_analysis or "Multi-agent analysis not yet run. Please run SafexAI Analysis first."
    summary_text = agent_analysis[:1500] + "..." if len(agent_analysis) > 1500 else agent_analysis
    summary_text = summary_text.replace('\n', '<br/>')
    story.append(Paragraph(summary_text, normal_style))
    story.append(Spacer(1, 0.15*inch))

    # Recommended Actions
    story.append(Paragraph("4. Immediate Recommended Actions", heading_style))
    actions = [
        "SUSPEND all Hot Work and Confined Space permits in affected zone immediately",
        "EVACUATE all non-essential personnel from Zone A",
        "ACTIVATE ventilation systems — target gas levels below threshold",
        "NOTIFY Plant Manager, Safety Officer, and Emergency Response Team",
        "PRESERVE all sensor logs and CCTV footage for DGFASLI investigation",
        "RE-TEST gas levels every 30 minutes until safe threshold achieved",
        "CONDUCT mandatory safety briefing before resuming operations",
    ]
    for i, action in enumerate(actions, 1):
        story.append(Paragraph(f"{i}. {action}", normal_style))
    story.append(Spacer(1, 0.15*inch))

    # Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "This report was automatically generated by SafexAI. "
        "All findings must be verified by a qualified Safety Officer before regulatory submission. "
        "SafexAI © 2026 | ET AI Hackathon 2026",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
