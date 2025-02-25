from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
from typing import Dict, Any

def generate_pdf(template: str, data: Dict[str, Any]) -> bytes:
    """
    Generate a PDF resume based on the selected template and user data.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=72)

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomHeading',
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#0066cc')
    ))

    # Content elements
    elements = []

    # Header
    elements.append(Paragraph(data.get('name', ''), styles['Title']))
    contact_info = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('location', '')}"
    elements.append(Paragraph(contact_info, styles['Normal']))
    elements.append(Spacer(1, 20))

    # Professional Summary
    if data.get('summary'):
        elements.append(Paragraph("Professional Summary", styles['CustomHeading']))
        elements.append(Paragraph(data.get('summary', ''), styles['Normal']))
        elements.append(Spacer(1, 20))

    # Professional Experience
    experience_exists = False
    experiences = []
    i = 0
    while f'company_{i}' in data:
        company = data.get(f'company_{i}')
        if company:
            experience_exists = True
            exp_data = [
                [Paragraph(f"<b>{data.get(f'position_{i}', '')}</b>", styles['Normal']),
                 Paragraph(f"{data.get(f'start_date_{i}', '')} - {data.get(f'end_date_{i}', '')}", styles['Normal'])],
                [Paragraph(company, styles['Normal']), ""],
                [Paragraph(data.get(f'experience_{i}', ''), styles['Normal']), ""]
            ]
            experiences.append(exp_data)
        i += 1

    if experience_exists:
        elements.append(Paragraph("Professional Experience", styles['CustomHeading']))
        for exp in experiences:
            t = Table(exp, colWidths=[5*inch, 2*inch])
            t.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))

    # Education
    if data.get('degree') or data.get('institution'):
        elements.append(Paragraph("Education", styles['CustomHeading']))
        edu_data = [
            [Paragraph(f"<b>{data.get('degree', '')}</b>", styles['Normal']),
             Paragraph(data.get('grad_year', ''), styles['Normal'])],
            [Paragraph(data.get('institution', ''), styles['Normal']),
             Paragraph(f"GPA: {data.get('gpa', '')}" if data.get('gpa') else "", styles['Normal'])]
        ]
        t = Table(edu_data, colWidths=[5*inch, 2*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 20))

    # Skills
    if data.get('skills'):
        elements.append(Paragraph("Skills", styles['CustomHeading']))
        elements.append(Paragraph(data.get('skills', ''), styles['Normal']))

    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes