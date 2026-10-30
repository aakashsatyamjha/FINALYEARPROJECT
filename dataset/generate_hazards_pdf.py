"""
Generates academic PDF documentation for the Restricted Substances Health Hazards Dataset.
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import pandas as pd

def generate_pdf():
    pdf_filename = "dataset/RESTRICTED_SUBSTANCES_HAZARDS_DOCUMENTATION.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("FoodGuard — Restricted Substances & Health Hazards Dataset", title_style))
    story.append(Paragraph("Clinical Toxicology, Target Organ Pathologies & Multi-Jurisdictional Regulatory Reference Matrix", subtitle_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Executive Overview & Problem Statement", h2_style))
    story.append(Paragraph(
        "Modern packaged food and agricultural supply chains frequently encounter chemical substances that have faced "
        "stringent legal bans or statutory restrictions across major international food safety authorities (FSSAI India, US FDA, EFSA EU). "
        "This dataset codifies the precise physiological and toxicological problems faced by each restricted substance, "
        "including cellular DNA fragmentation, endocrine disruption, organ-specific carcinogenesis, and severe pediatric behavioral effects.",
        body_style
    ))

    # Load CSV
    df = pd.read_csv("dataset/restricted_substances_hazards_dataset.csv")

    story.append(Paragraph("2. Health Problems & Toxicological Profiles Table", h2_style))

    table_data = [[
        Paragraph("Code", table_header),
        Paragraph("Substance", table_header),
        Paragraph("Primary Organ", table_header),
        Paragraph("Problems Faced (Clinical Hazards)", table_header),
        Paragraph("Banning / Restriction Status", table_header)
    ]]

    for _, row in df.iterrows():
        table_data.append([
            Paragraph(f"<b>{row['ins_code']}</b>", table_cell),
            Paragraph(f"<b>{row['common_name']}</b><br/><font color='#64748B'>{row['scientific_chemical_name'][:35]}...</font>", table_cell),
            Paragraph(f"<b>{row['primary_organ_affected']}</b>", table_cell),
            Paragraph(str(row['health_problems_faced']), table_cell),
            Paragraph(f"<font color='#B91C1C'>{row['restriction_status']}</font>", table_cell)
        ])

    t = Table(table_data, colWidths=[50, 110, 85, 175, 120])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 14))

    # Academic Project Sign-Off
    story.append(Paragraph("3. Academic Project Evaluation & Sign-off", h2_style))
    signoff_data = [
        [Paragraph("<b>Student Name / Roll:</b> Final Year Engineering Team", body_style), Paragraph("<b>Department:</b> Computer Science & Engineering", body_style)],
        [Paragraph("<b>Dataset Records:</b> 20 Core Toxicological Profiles", body_style), Paragraph("<b>Academic Year:</b> 2026", body_style)],
        [Paragraph("<b>Project Mentor:</b> ___________________________", body_style), Paragraph("<b>Signature / Approval:</b> ___________________________", body_style)]
    ]
    st = Table(signoff_data, colWidths=[270, 270])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(st)

    doc.build(story)
    print(f"Generated hazards documentation PDF: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
