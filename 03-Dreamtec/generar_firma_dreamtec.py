import pandas as pd
import os
import sys
import shutil
from openpyxl import load_workbook

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Obtener ruta base del script y raíz del proyecto
base_path = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
proyecto_root = os.path.dirname(base_path)

# === Rutas ===
ruta_template = os.path.join(base_path, "diseño_dreamtec.html")
ruta_datos = os.path.join(proyecto_root, "empleados.xlsx")
ruta_salida = os.path.join(proyecto_root, "05-firmas-generadas", "03-Dreamtec")

os.makedirs(ruta_salida, exist_ok=True)

# Copiar carpeta assets a la carpeta de salida para que las imágenes locales carguen correctamente
assets_origen = os.path.join(base_path, "assets")
assets_destino = os.path.join(ruta_salida, "assets")
if os.path.exists(assets_origen):
    os.makedirs(assets_destino, exist_ok=True)
    for item in os.listdir(assets_origen):
        s = os.path.join(assets_origen, item)
        d = os.path.join(assets_destino, item)
        if os.path.isfile(s):
            shutil.copy2(s, d)

# Leer plantilla HTML
with open(ruta_template, "r", encoding="utf-8") as f:
    template = f.read()

# Leer datos con pandas (solo para lógica)
empleados = pd.read_excel(
    ruta_datos,
    sheet_name="DREAMTEC",
    dtype={
        "celular_empleado": str
    }
)

if "procesado" not in empleados.columns:
    raise ValueError("La columna 'procesado' no existe en empleados.xlsx")

empleados["procesado"] = empleados["procesado"].astype(str).str.strip()

# Abrir workbook original (preserva formato)
wb = load_workbook(ruta_datos)
ws = wb["DREAMTEC"] # si necesitas una hoja específica

# Obtener número de columna "procesado"
col_procesado_excel = empleados.columns.get_loc("procesado") + 1  # +1 porque Excel empieza en 1

firmas_generadas = 0

for index, row in empleados.iterrows():

    # Ignorar filas vacías
    if pd.isna(row.get("nombre_empleado")) or not str(row["nombre_empleado"]).strip() or str(row["nombre_empleado"]).strip().lower() == "nan":
        continue

    firmas_generadas += 1

    html_personal = template
    row_data = row.to_dict()

    # Obtener nombre corto para el nombre del archivo y URLs de QR
    nombre_corto = str(row.get("nombre_corto", "")).strip()
    if not nombre_corto or nombre_corto == "nan":
        nombre_corto = str(row["nombre_empleado"]).replace(" ", "_").lower()

    # Si la URL del QR viene solo como carpeta en el Excel, autocompletar la ruta completa
    for qr_col in ["qr_wsp", "qr_linkedin"]:
        val = str(row_data.get(qr_col, "")).strip()
        if val and val != "nan" and not val.endswith((".png", ".jpg", ".jpeg", ".gif")):
            row_data[qr_col] = f"{val}/{nombre_corto}.png"

    for col, val in row_data.items():
        val_str = str(val).strip(' "\'\t\r\n') if pd.notna(val) else ""
        html_personal = html_personal.replace(f"{{{{{col}}}}}", val_str)

    salida = os.path.join(ruta_salida, f"{nombre_corto}.html")

    with open(salida, "w", encoding="utf-8") as f:
        f.write(html_personal)

    print(f"[OK] Firma generada: {salida}")

    # === Actualizar SOLO la celda correspondiente ===
    fila_excel = index + 2  # +2 porque pandas empieza en 0 y Excel tiene encabezado en fila 1
    ws.cell(row=fila_excel, column=col_procesado_excel, value="Si")

    try:
        wb.save(ruta_datos)  # guarda sin destruir formato
    except PermissionError:
        print("[WARNING] No se pudo actualizar el Excel 'empleados.xlsx' porque esta abierto.")

if firmas_generadas == 0:
    print("[INFO] No se genero ninguna firma porque todas las filas en el Excel tienen 'procesado' = 'Si'.")
    print(" -> Cambia a 'No' en la columna 'procesado' del Excel para la firma que quieras generar.")

print("\nProceso finalizado.")