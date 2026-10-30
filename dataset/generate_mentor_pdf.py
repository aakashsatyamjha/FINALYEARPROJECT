"""
Generate formal academic PDF documentation for mentor submission:
Packaged Food Safety & Cross-Country Regulatory Assessment Dataset Documentation
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "FOOD_REGULATORY_DATASET_DOCUMENTATION.pdf"))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "FoodGuard — Packaged Food Safety & Regulatory Dataset Documentation")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)

        # Footer
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        
        self.drawString(54, 32, "College Capstone Project — Final Year Engineering")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def build_pdf():
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
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#1e293b")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # ── TITLE SECTION ──
    story.append(Paragraph("FoodGuard — Packaged Food Safety & Regulatory Assessment System", title_style))
    story.append(Paragraph("Standardized 300-Record Food Additive, Adulteration & Multi-Country Regulatory Dataset Specification", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Project Domain:</b>", table_cell_bold), Paragraph("Food Safety, Regulatory Compliance & Computer Vision OCR", table_cell_style),
         Paragraph("<b>Dataset File:</b>", table_cell_bold), Paragraph("300_packaged_food_dataset.csv", table_cell_style)],
        [Paragraph("<b>Total Records:</b>", table_cell_bold), Paragraph("300 Standardized Product/Additive Records", table_cell_style),
         Paragraph("<b>Authorities:</b>", table_cell_bold), Paragraph("India (FSSAI), USA (FDA), EU (EFSA), Australia (FSANZ)", table_cell_style)],
        [Paragraph("<b>Architecture:</b>", table_cell_bold), Paragraph("React + FastAPI + Python Decision Engine + PaddleOCR", table_cell_style),
         Paragraph("<b>Date:</b>", table_cell_bold), Paragraph("Academic Year 2026", table_cell_style)]
    ]
    t_meta = Table(meta_data, colWidths=[90, 160, 90, 164])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # ── SECTION 1: EXECUTIVE SUMMARY ──
    story.append(Paragraph("1. Executive Summary & Project Purpose", h1_style))
    story.append(Paragraph(
        "Modern packaged food supply chains contain complex combinations of synthetic dyes, chemical preservatives, "
        "stabilizers, sweeteners, and texturizers. Crucially, permissible usage levels and legal authorizations diverge "
        "widely across international food regulatory bodies. An additive legally permitted in one country may be strictly "
        "banned or revoked in another due to emerging toxicological or carcinogenicity evidence (e.g. Titanium Dioxide INS 171, "
        "Erythrosine INS 127, Potassium Bromate INS 924a, Azodicarbonamide INS 927a).",
        body_style
    ))
    story.append(Paragraph(
        "The <b>FoodGuard 300-Record Regulatory Dataset</b> provides an empirical, structured ground-truth benchmark "
        "enabling automated cross-referencing of packaged food ingredients extracted via <b>1D/2D Barcode Scanning</b> and "
        "<b>PaddleOCR Vision Analysis</b> against statutory permissions in India, the United States, the European Union, and Australia.",
        body_style
    ))

    # ── SECTION 2: DATASET SCHEMA ──
    story.append(Paragraph("2. Standardized 15-Column Dataset Schema", h1_style))
    story.append(Paragraph(
        "The dataset is structured as a normalized CSV file (`300_packaged_food_dataset.csv`) with 15 standard attributes:",
        body_style
    ))

    schema_rows = [
        [Paragraph("Column Name", table_header_style), Paragraph("Type", table_header_style), Paragraph("Description & Example", table_header_style)],
        [Paragraph("record_id", table_cell_bold), Paragraph("Integer", table_cell_style), Paragraph("Unique sequential identifier (1 to 300).", table_cell_style)],
        [Paragraph("brand_or_manufacturer", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Target manufacturer or category brand (Parle, Britannia, Nestlé, PepsiCo, etc.).", table_cell_style)],
        [Paragraph("product_category", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Food sector (Beverage, Confectionery, Extruded Snack, Bakery, Dairy, Spices).", table_cell_style)],
        [Paragraph("product_name", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Packaged item or additive formulation name.", table_cell_style)],
        [Paragraph("common_label_name", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Consumer-facing ingredient list name (e.g. Tartrazine, Sodium Benzoate, MSG).", table_cell_style)],
        [Paragraph("scientific_chemical_name", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("IUPAC chemical nomenclature (e.g. Disodium 2,4,5,7-tetraiodofluorescein).", table_cell_style)],
        [Paragraph("codex_ins_no", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Codex Alimentarius International Numbering System code (e.g. 102, 171, 924a).", table_cell_style)],
        [Paragraph("fssai_reference_status", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Statutory status in India under FSSAI Food Additives Regulations.", table_cell_style)],
        [Paragraph("usa_reference_status", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Statutory status in USA under US FDA Title 21 Code of Federal Regulations.", table_cell_style)],
        [Paragraph("eu_reference_status", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Statutory status in European Union under Regulation (EC) No 1333/2008.", table_cell_style)],
        [Paragraph("eu_e_number", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("EU authorized E-number code (e.g. E102, E127, E171, E927a).", table_cell_style)],
        [Paragraph("us_identifier_reference", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("FDA CFR regulatory section (e.g. 21 CFR 74.705, 21 CFR 184.1733).", table_cell_style)],
        [Paragraph("australia_nz_code", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Food Standards Australia New Zealand (FSANZ) Code identifier.", table_cell_style)],
        [Paragraph("screening_note", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Toxicological reason, mandatory label warning, or category limit instruction.", table_cell_style)],
        [Paragraph("source", table_cell_bold), Paragraph("String", table_cell_style), Paragraph("Ground truth provenance citation note.", table_cell_style)]
    ]
    t_schema = Table(schema_rows, colWidths=[120, 55, 329])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_schema)

    story.append(PageBreak())

    # ── SECTION 3: COUNTRY-WISE REGULATORY COMPARISON ──
    story.append(Paragraph("3. Cross-Country Regulatory Compliance Matrix", h1_style))
    story.append(Paragraph(
        "The core functionality of FoodGuard is detecting divergent legal authorizations between global food unions. "
        "The table below illustrates sample high-impact regulatory divergences extracted directly from the dataset:",
        body_style
    ))

    comp_rows = [
        [Paragraph("INS / Name", table_header_style), Paragraph("India (FSSAI)", table_header_style), Paragraph("USA (US FDA)", table_header_style), Paragraph("EU (EFSA)", table_header_style), Paragraph("Regulatory Screening Rationale", table_header_style)],
        [Paragraph("<b>INS 171</b><br/>Titanium Dioxide", table_cell_style), Paragraph("Specified applications", table_cell_style), Paragraph("Permitted (21 CFR 73.575)", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not authorised / Banned</b></font>", table_cell_style), Paragraph("Banned across EU under Regulation (EU) 2022/63 due to DNA strand break concerns.", table_cell_style)],
        [Paragraph("<b>INS 127</b><br/>Erythrosine (Red 3)", table_cell_style), Paragraph("Permitted with limits", table_cell_style), Paragraph("<font color='#b91c1c'><b>Revoked / Phase-out</b></font>", table_cell_style), Paragraph("<font color='#b91c1c'><b>Restricted to cherries</b></font>", table_cell_style), Paragraph("FDA revoked color authorization under 21 CFR 74.303; EU restricted due to thyroid tumorigenesis.", table_cell_style)],
        [Paragraph("<b>INS 924a</b><br/>Potassium Bromate", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not permitted (Banned)</b></font>", table_cell_style), Paragraph("Permitted in bakery", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not authorised / Banned</b></font>", table_cell_style), Paragraph("Banned by FSSAI (2016) and EU as an IARC Group 2B probable human carcinogen.", table_cell_style)],
        [Paragraph("<b>INS 927a</b><br/>Azodicarbonamide", table_cell_style), Paragraph("Specified flour uses", table_cell_style), Paragraph("Permitted (21 CFR 172.806)", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not authorised / Banned</b></font>", table_cell_style), Paragraph("Banned in Europe and UK due to respiratory sensitization and semicarbazide breakdown.", table_cell_style)],
        [Paragraph("<b>BVO</b><br/>Brominated Veg. Oil", table_cell_style), Paragraph("Category verification", table_cell_style), Paragraph("<font color='#b91c1c'><b>Revoked / Banned</b></font>", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not authorised / Banned</b></font>", table_cell_style), Paragraph("FDA finalized rule revoking BVO authorization in 2024 following bioaccumulation studies.", table_cell_style)],
        [Paragraph("<b>INS 143</b><br/>Fast Green FCF", table_cell_style), Paragraph("Specified uses", table_cell_style), Paragraph("Permitted", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not authorised in EU</b></font>", table_cell_style), Paragraph("Not approved under EU food additive registry; permitted in US with batch certification.", table_cell_style)],
        [Paragraph("<b>INS 952</b><br/>Cyclamate", table_cell_style), Paragraph("Category verification", table_cell_style), Paragraph("<font color='#b91c1c'><b>Not permitted (Banned)</b></font>", table_cell_style), Paragraph("Permitted with limits", table_cell_style), Paragraph("Strictly prohibited as food sweetener in US since 1970; widely permitted in EU and UK.", table_cell_style)],
        [Paragraph("<b>INS 102</b><br/>Tartrazine (Yellow 5)", table_cell_style), Paragraph("Permitted with limits", table_cell_style), Paragraph("Permitted (21 CFR 74.705)", table_cell_style), Paragraph("Warning label required", table_cell_style), Paragraph("Mandatory EU warning: 'May have an adverse effect on activity and attention in children'.", table_cell_style)]
    ]
    t_comp = Table(comp_rows, colWidths=[90, 85, 95, 95, 139])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 12))

    # ── SECTION 4: MATCHING ALGORITHM ──
    story.append(Paragraph("4. Algorithmic Matching & Regulatory Audit Flow", h1_style))
    story.append(Paragraph(
        "When an input is received (via 1D Barcode scanning, manual barcode entry, or PaddleOCR label photo extraction), "
        "the FoodGuard decision engine executes the following verification pipeline:",
        body_style
    ))
    story.append(Paragraph("• <b>Step 1 — Entity Normalization:</b> Isolates additive names and Codex INS codes using regular expressions (`r'\\bins\\s*(\\d+)'`, `r'\\be\\s*(\\d+)'`).", bullet_style))
    story.append(Paragraph("• <b>Step 2 — Dataset Cross-Referencing:</b> Matches extracted tokens against indexed dataset records in `300_packaged_food_dataset.csv`.", bullet_style))
    story.append(Paragraph("• <b>Step 3 — Multi-Country Permission Check:</b> Queries statutory compliance across India (FSSAI), USA (FDA), EU (EFSA), and Australia (FSANZ).", bullet_style))
    story.append(Paragraph("• <b>Step 4 — Decision Synthesis:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;a) If <i>all</i> permissions are Permitted: System displays clean status (<b>✓ All Permissions OK — Low Risk</b>).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;b) If <i>any</i> authority revokes or bans the ingredient: System generates an explicit alert specifying the <b>INS Number</b>, <b>Item Name</b>, <b>Banning Authority</b>, and <b>Toxicological Rationale</b>.", bullet_style))

    # ── SECTION 5: STATISTICAL BREAKDOWN ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Dataset Statistical Distribution", h1_style))
    stats_data = [
        [Paragraph("Category / Segment", table_header_style), Paragraph("Count", table_header_style), Paragraph("Representative Substance Examples", table_header_style)],
        [Paragraph("Food Colours & Pigments", table_cell_bold), Paragraph("68", table_cell_style), Paragraph("Tartrazine, Sunset Yellow, Allura Red, Brilliant Blue, Erythrosine, Titanium Dioxide", table_cell_style)],
        [Paragraph("Preservatives & Antioxidants", table_cell_bold), Paragraph("74", table_cell_style), Paragraph("Sodium Benzoate, Potassium Sorbate, BHA, BHT, TBHQ, Sodium Metabisulphite", table_cell_style)],
        [Paragraph("Emulsifiers, Stabilizers & Gums", table_cell_bold), Paragraph("52", table_cell_style), Paragraph("Lecithin, PGPR, Guar Gum, Xanthan Gum, DATEM, Mono- and Diglycerides", table_cell_style)],
        [Paragraph("Artificial & Natural Sweeteners", table_cell_bold), Paragraph("38", table_cell_style), Paragraph("Aspartame, Acesulfame-K, Sucralose, Saccharin, Cyclamate, Stevia, Xylitol", table_cell_style)],
        [Paragraph("Flavour Enhancers & Acidulants", table_cell_bold), Paragraph("36", table_cell_style), Paragraph("MSG (INS 621), Disodium Inosinate (INS 631), Guanylate (INS 627), Citric Acid", table_cell_style)],
        [Paragraph("Banned Chemical Adulterants", table_cell_bold), Paragraph("32", table_cell_style), Paragraph("Metanil Yellow, Lead Chromate, Rhodamine B, Sudan Dyes, Melamine, Formalin", table_cell_style)],
        [Paragraph("<b>Total Standardized Records</b>", table_cell_bold), Paragraph("<b>300</b>", table_cell_bold), Paragraph("<b>Full empirical coverage across 10 packaged food FMCG sectors</b>", table_cell_bold)]
    ]
    t_stats = Table(stats_data, colWidths=[140, 45, 319])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_stats)

    story.append(Spacer(1, 14))
    story.append(Paragraph("6. Academic Verification & Project Mentor Sign-Off", h1_style))
    story.append(Paragraph(
        "This dataset and verification system have been designed and validated in accordance with the regulatory statutes "
        "of the Food Safety and Standards Authority of India (FSSAI), the United States Code of Federal Regulations (21 CFR), "
        "and the European Food Safety Authority (EFSA Regulation 1333/2008).",
        body_style
    ))
    
    sign_data = [
        [Paragraph("<b>Submitted by:</b>", table_cell_bold), Paragraph("Project Student / Team", table_cell_style),
         Paragraph("<b>Date of Submission:</b>", table_cell_bold), Paragraph("October 2026", table_cell_style)],
        [Paragraph("<b>Verified by:</b>", table_cell_bold), Paragraph("Project Mentor / Guide", table_cell_style),
         Paragraph("<b>Mentor Signature:</b>", table_cell_bold), Paragraph("___________________________", table_cell_style)]
    ]
    t_sign = Table(sign_data, colWidths=[100, 160, 100, 144])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated mentor PDF at {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
