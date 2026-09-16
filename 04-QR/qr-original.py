import qrcode
from PIL import Image, ImageDraw

# =========================
# 1. Datos vCard
# =========================
vcard_data = """BEGIN:VCARD
VERSION:3.0
FN:Cristian Espinoza
N:Espinoza;Cristian;;;
TEL;TYPE=CELL:+569 9093 6432
EMAIL;TYPE=WORK:jgil@ofimundo.cl
END:VCARD
"""
# =========================
# 2. Crear QR
# =========================
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=12,
    border=2,
)

qr.add_data(vcard_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# =========================
# 3. Cargar logo
# =========================
logo = Image.open("imagenes//logo.png").convert("RGBA")

# =========================
# 4. Redimensionar (máx 25%)
# =========================
qr_width, qr_height = qr_img.size
logo_size = qr_width // 4

logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# =========================
# 5. Crear máscara circular (sin borde)
# =========================
mask = Image.new("L", (logo_size, logo_size), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, logo_size, logo_size), fill=255)

logo_circular = Image.new("RGBA", (logo_size, logo_size))
logo_circular.paste(logo, (0, 0), mask=mask)

# =========================
# 6. Centrar directamente
# =========================
pos = (
    (qr_width - logo_size) // 2,
    (qr_height - logo_size) // 2
)

qr_img.paste(logo_circular, pos, logo_circular)

# =========================
# 7. Guardar
# =========================
qr_img.save("qr-cel.png")
#qr_img.save("qr-in.png")

print("QR generado correctamente sin borde.")
