from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

def generate_pdf(template: str, data: dict) -> bytes:
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
    elements.append(Paragraph(data.name, styles['Title']))
    contact_info = f"{data.email} | {data.phone} | {data.location}"
    elements.append(Paragraph(contact_info, styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Professional Summary
    elements.append(Paragraph("Professional Summary", styles['CustomHeading']))
    elements.append(Paragraph(data.summary, styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Professional Experience
    elements.append(Paragraph("Professional Experience", styles['CustomHeading']))
    
    # Get all experiences
    experiences = []
    i = 0
    while f'company_{i}' in data:
        if data[f'company_{i}']:
            exp_data = [
                [Paragraph(f"<b>{data[f'position_{i}']}</b>", styles['Normal']),
                 Paragraph(f"{data[f'start_date_{i}']} - {data[f'end_date_{i}']}", styles['Normal'])],
                [Paragraph(data[f'company_{i}'], styles['Normal']), ""],
                [Paragraph(data[f'experience_{i}'], styles['Normal']), ""]
            ]
            experiences.append(exp_data)
        i += 1
    
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
    elements.append(Paragraph("Education", styles['CustomHeading']))
    edu_data = [
        [Paragraph(f"<b>{data.degree}</b>", styles['Normal']),
         Paragraph(data.grad_year, styles['Normal'])],
        [Paragraph(data.institution, styles['Normal']),
         Paragraph(f"GPA: {data.gpa}" if data.gpa else "", styles['Normal'])]
    ]
    t = Table(edu_data, colWidths=[5*inch, 2*inch])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    # Skills
    elements.append(Paragraph("Skills", styles['CustomHeading']))
    elements.append(Paragraph(data.skills, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
