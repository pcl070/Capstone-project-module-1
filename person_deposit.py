import sys
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm
from bar_1830 import get_personal_details

# Register the DejaVuSans and DejaVuSans-Bold fonts
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

def add_logo(canvas, logo_path):
    logo_x = 2 * cm
    logo_y = 26 * cm  # Adjust according to where you want the logo placed
    canvas.drawImage(logo_path, logo_x, logo_y, width=1.65 * cm, height=2 * cm)

def generate_invoice(details, deposit_amount=150):
    file_name = f"Invoice_{details['First name']}_{details['Last name']}.pdf"
    
    doc = SimpleDocTemplate(file_name, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        'title',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=14,
        fontName='DejaVuSans-Bold',
        alignment=1
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        fontName='DejaVuSans'
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=11,
        fontName='DejaVuSans-Bold',
        spaceAfter=14,
        alignment=1
    )

    # Add logo using canvas
    def on_first_page(canvas, doc):
        add_logo(canvas, "logo.png")  # Replace with your logo file path

    # Title
    elements.append(Paragraph("IŠANKSTINĖ SĄSKAITA", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Nr. PROFORMA/038", header_style))
    elements.append(Spacer(1, 12))

    # Dates
    today_date = datetime.today().strftime('%Y-%m-%d')
    pay_until_date = (datetime.today() + timedelta(days=7)).strftime('%Y-%m-%d')
    elements.append(Paragraph(f"Data: {today_date}", normal_style))
    elements.append(Paragraph(f"Apmokėti iki: {pay_until_date}", normal_style))
    elements.append(Spacer(1, 12))

    # Seller and Client information
    seller_info = """
    <b>Pardavėjas:</b><br/>
    Double vision, MB<br/>
    Žeimenos g. 82D-24<br/>
    Kaunas LT-49327<br/>
    Lietuva<br/>
    Telefonas: +370 636 73352<br/>
    E. paštas: info@1830baras.lt<br/>
    Interneto svetainės adresas: https://1830baras.lt<br/>
    Įmonės kodas: 306318735<br/>
    PVM mokėtojo kodas: LT100016521419<br/>
    Bankas: „Swedbank“, AB<br/>
    BIC: HABALT22<br/>
    IBAN: LT557300010180149406
    """
    client_info = f"""
    <b>Pirkėjas:</b><br/>
    {details['First name']} {details['Last name']}<br/>
    {details['Birth date']}<br/>
    Adresas: {details["Residency Address"]}<br/>
    Telefonas: {details['Phone Number']}<br/>
    E. paštas: {details['Email']}
    """

    # Creating a table to align seller and client information side by side
    info_table = Table(
        [[Paragraph(seller_info, normal_style), Paragraph(client_info, normal_style)]],
        colWidths=[10 * cm, 8 * cm]
    )
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 12))

    # Invoice details table
    data = [
        ["Aprašymas", "Kiekis", "Vnt. kaina (be PVM)", "Suma be PVM"],
        ["Užstatas mobilaus baro nuomai", "1,0", f"{deposit_amount:.2f} €", f"{deposit_amount:.2f} €"]
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Total amount
    total_amount = f"""
    Suma be PVM: {deposit_amount:.2f} €<br/>
    PVM Neapmokestinama (PVMĮ 20–33 str., 112 str. 1 ir 2 d.) 0,00 €<br/>
    Suma su PVM: {deposit_amount:.2f} €<br/><br/>
    Viso mokėti: {deposit_amount:.2f} €
    """
    elements.append(Paragraph(total_amount, normal_style))
    elements.append(Spacer(1, 12))

    doc.build(elements, onFirstPage=on_first_page)

    print(f"Invoice saved as {file_name}")
    return file_name

def test_generate_invoice():
    # Sample data for testing
    sample_details = {
        "First name": "Rita",
        "Last name": "Palsienė",
        "Birth date": "1980-01-01",
        "Residency Address": "Špokų g. 12, Kaunas",
        "Phone Number": "+37068753995",
        "Email": "r.palsiene@gmail.com"
    }
    generate_invoice(sample_details)

if __name__ == "__main__":
    # Uncomment the following line to test with random details
    # test_generate_invoice()

    # Uncomment the following lines to run with actual user input
    details = get_personal_details()
    generate_invoice(details)
