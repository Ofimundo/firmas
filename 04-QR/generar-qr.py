import qrcode
from PIL import Image, ImageDraw
import pandas as pd
import os
import sys
from openpyxl import load_workbook

# =====================================================
# 1️⃣ RUTAS Y CONFIGURACIÓN DE QR
# =====================================================

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base_path = os.path.dirname(
    os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
)
proyecto_root = os.path.dirname(base_path)

ruta_datos = os.path.join(proyecto_root, "empleados.xlsx")
ruta_salida = os.path.join(base_path, "qr-generados")

# Tipo de QR: "linkedin" o "vcard" (se puede definir aquí o pasar como 2do argumento)
# Ej: python generar-qr.py DREAMTEC linkedin
tipo_qr = sys.argv[2].lower() if len(sys.argv) > 2 else "linkedin"

logo_cel = os.path.join(base_path, "logos", "logo-cel.PNG")
if not os.path.exists(logo_cel):
    logo_cel = os.path.join(base_path, "logos", "logo-cel.png")
logo_in = os.path.join(base_path, "logos", "logo-in.jfif")

if tipo_qr == "linkedin":
    ruta_logo = logo_in
    print("🔗 Modo: Generando QR de LINKEDIN (enlace directo al perfil)")
else:
    ruta_logo = logo_cel
    print("🎴 Modo: Generando QR de CONTACTO (vCard)")

os.makedirs(ruta_salida, exist_ok=True)

# =====================================================
# 2️⃣ Leer Excel
# =====================================================

# Permitir pasar la hoja como argumento o usar "DREAMTEC" por defecto
nombre_hoja = sys.argv[1] if len(sys.argv) > 1 else "DREAMTEC"
print(f"📄 Leyendo hoja: '{nombre_hoja}' desde {ruta_datos}")

empleados = pd.read_excel(ruta_datos, sheet_name=nombre_hoja)

empleados.columns = empleados.columns.str.strip().str.lower()

# Asegurarse que la columna procesado exista
if "procesado" not in empleados.columns:
    print(f"❌ La columna 'procesado' no existe en la hoja '{nombre_hoja}'.")
    sys.exit()

# Filtrar solo registros NO procesados
empleados = empleados[
    empleados["procesado"].astype(str).str.strip().str.lower() == "no"
]


if empleados.empty:
    print(f"⚠️ No hay registros pendientes por procesar en la hoja '{nombre_hoja}'.")
    sys.exit()

# =====================================================
# 3️⃣ Recorrer empleados (NO modificamos columna procesado)
# =====================================================

for index, row in empleados.iterrows():

    nombre = str(row.get("nombre_empleado", "")).strip()
    nombre2 = str(row.get("nombre_corto", "")).strip()
    if not nombre2 or nombre2.lower() == "nan":
        nombre2 = nombre.replace(" ", "_").lower()
    telefono = str(row.get("celular_empleado", "")).strip()
    email = str(row.get("correo_empleado", "")).strip()
    linkedin = str(row.get("linkedin_empleado", row.get("linkedin", ""))).strip()

    if not nombre or not email:
        print(f"⚠️ Datos incompletos en fila {index + 2}. Se omite.")
        continue

    # =====================================================
    # 4️⃣ Determinar contenido del QR
    # =====================================================

    if tipo_qr == "linkedin":
        if not linkedin or linkedin.lower() == "nan":
            print(f"⚠️ Sin URL de LinkedIn para '{nombre}' en fila {index + 2}. Se omite.")
            continue
        contenido_qr = linkedin
    else:
        # Separar nombre y apellido para vCard
        partes_nombre = nombre.split(" ")
        apellido = partes_nombre[-1]
        nombre_pila = " ".join(partes_nombre[:-1])

        contenido_qr = (
            "BEGIN:VCARD\r\n"
            "VERSION:3.0\r\n"
            f"FN:{nombre}\r\n"
            f"N:{apellido};{nombre_pila};;;\r\n"
            f"TEL;TYPE=CELL: +{telefono}\r\n"
            f"EMAIL;TYPE=WORK:{email}\r\n"
            "END:VCARD\r\n"
        )

    # =====================================================
    # 5️⃣ Crear QR
    # =====================================================

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )

    qr.add_data(contenido_qr)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # =====================================================
    # 6️⃣ Cargar y preparar logo
    # =====================================================

    logo = Image.open(ruta_logo).convert("RGBA")

    qr_width, qr_height = qr_img.size
    logo_size = qr_width // 4  # 25%

    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Máscara circular
    mask = Image.new("L", (logo_size, logo_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, logo_size, logo_size), fill=255)

    logo_circular = Image.new("RGBA", (logo_size, logo_size))
    logo_circular.paste(logo, (0, 0), mask=mask)

    # Centrar logo
    pos = (
        (qr_width - logo_size) // 2,
        (qr_height - logo_size) // 2
    )

    qr_img.paste(logo_circular, pos, logo_circular)

    # =====================================================
    # 7️⃣ Guardar con misma nomenclatura + _qr
    # =====================================================

    nombre_archivo = nombre2

    # SE MODIFICA SEGÚN SEA EL QR QUE SE ESTA GENERANDO.
    salida = os.path.join(ruta_salida, f"{nombre_archivo}.png")

    qr_img.save(salida)

    print(f"✅ QR generado: {salida}")

print("\nProceso de QR finalizado.")