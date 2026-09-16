import os

base_dir = r"c:\Users\marrano\Desktop\Desarrollo\Firmas electronicas\firmas\PROYECTO FIRMAS\03-Dreamtec"
assets_dir = os.path.join(base_dir, "assets")
os.makedirs(assets_dir, exist_ok=True)

png_path = os.path.join(assets_dir, "barra_inferior_dreamtec.png")
if os.path.exists(png_path):
    print(f"Preservando imagen oficial enviada por usuario: {png_path}")
