from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from .user_repository import User

def format_date_of_birth(user: User):
    return f"{user.place_of_birth}, {user.date_of_birth.strftime("%d %B %Y")}"

def normalize_name(name: str):
    return '_'.join(name.split(' ')).lower()

def create_skck(user: User):
    filename = f"./documents/{normalize_name(user.name)}_skck.pdf"

    # Setup canvas
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Set title and headers
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 2 * cm, "PEMERINTAH KABUPATEN BIREUEN")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 3 * cm, "GAMPONG SEULEUMBAH")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 3.5 * cm, "KECAMATAN JEUMPA")
    
    # Line under the header
    c.line(2 * cm, height - 4 * cm, width - 2 * cm, height - 4 * cm)

    # Document title
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, height - 5 * cm, "SURAT KETERANGAN BERKELAKUAN BAIK")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 5.5 * cm, "No: 55/2035/BTM/SKBB/VI/2021")

    # Body text
    text = [
        "Keuchik Gampong Seuleumbah Kecamatan Jeumpa Kabupaten Bireuen,",
        "dengan ini menerangkan bahwa :"
    ]
    text_start_y = height - 6.5 * cm
    c.setFont("Helvetica", 10)
    for line in text:
        c.drawString(2 * cm, text_start_y, line)
        text_start_y -= 0.5 * cm

    # Table for personal details
    data = [
        ["Nama: ", user.name],
        ["Tempat / Tgl Lahir: ", format_date_of_birth(user)],
        ["Status Perkawinan: ", " Kawin"],
        ["Pekerjaan: ", user.profession],
        ["Alamat: ", user.address]
    ]
    
    # Create table
    table = Table(data, colWidths=[4 * cm, 11 * cm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 2 * cm, text_start_y - len(data) * 0.75 * cm)

    # List of conditions
    conditions = [
        "1. Berkelakuan Baik, tidak pernah melakukan tindakan/ perbuatan yang",
        "   menyimpang atau norma sosial yang berlaku,",
        "2. Tidak bersangkut paut Perkara Kriminal",
        "3. Tidak dalam status tahanan yang berwajib",
        "4. Tidak terlibat dalam penggunaan Narkoba"
    ]
    y_pos = text_start_y - (len(data) * 0.5 * cm) - 3 * cm
    for condition in conditions:
        c.drawString(2 * cm, y_pos, condition)
        y_pos -= 0.5 * cm

    # Footer text
    footer_text = [
        "Surat Keterangan ini diberikan kepada yang bersangkutan untuk Kelengkapan",
        "administrasi pengurusan SKCK.",
        "",
        "Demikian surat keterangan Berkelakuan Baik ini dikeluarkan dengan",
        "sebenarnya untuk dapat dipergunakan seperlunya.",
        "",
        "Seuleumbah, 22 Juni 2020",
        "Keuchik Seuleumbah"
    ]
    y_pos -= 1 * cm
    for line in footer_text:
        c.drawString(2 * cm, y_pos, line)
        y_pos -= 0.5 * cm

    # Signature line
    c.drawString(13 * cm, y_pos - 1.5 * cm, "( M HASAN USMAN )")

    # Save the PDF
    c.save()

    return filename

def create_resident_certificate(user: User):
    # Create a canvas and set the page size
    pdf_file  = f"./documents/{normalize_name(user.name)}_surat_domisili.pdf"
    
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4

    # Define starting coordinates
    x_margin = 2 * cm
    y = height - 2 * cm

    # Title
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, y, "SURAT KETERANGAN DOMISILI")
    y -= 1 * cm

    # Sub-title (number)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, "Nomor : 102/2020/GLP/XI/2020")
    y -= 1.5 * cm

    # Introductory text
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, "Yang bertanda tangan dibawah ini, Kepala Desa")
    c.drawString(x_margin + 250, y, "Langkapura")
    y -= 0.5 * cm
    c.drawString(x_margin, y, "Kecamatan Langkapura, Kabupaten Lampung Selatan, menerangkan dengan sebenarnya bahwa :")
    y -= 1 * cm

    # Information table
    data = {
        "Nama": user.name,
        "NIK": user.nik,
        "Jenis Kelamin": user.sex,
        "Tempat/ Tanggal Lahir": format_date_of_birth(user),
        "Agama": user.religion,
        "Kewarganegaraan": "Indonesia",
        "Pekerjaan": user.profession,
        "Alamat Domisili": user.address
    }

    for key, value in data.items():
        c.drawString(x_margin, y, f"{key} : ")
        c.drawString(x_margin + 150, y, value)
        y -= 0.5 * cm

    # Closing text
    y -= 1 * cm
    c.drawString(x_margin, y, "Adalah benar penduduk Desa Langkapura, Kecamatan Langkapura dan saat ini berdomisili di")
    y -= 0.5 * cm
    c.drawString(x_margin, y, "Desa Langkapura, Kecamatan Langkapura, Kabupaten Lampung Selatan.")
    y -= 1 * cm
    c.drawString(x_margin, y, "Demikian surat keterangan ini kami buat dengan sebenarnya agar dapat dipergunakan")
    y -= 0.5 * cm
    c.drawString(x_margin, y, "seperlunya.")

    # Footer and signature
    y -= 2 * cm
    c.drawString(width - 8 * cm, y, "Langkapura, 08 November 2020")
    y -= 0.5 * cm
    c.drawString(width - 8 * cm, y, "Kepala Desa Langkapura")
    y -= 2 * cm
    c.drawString(width - 8 * cm, y, "( Agus Widodo )")

    # Save PDF
    c.save()

    return pdf_file
