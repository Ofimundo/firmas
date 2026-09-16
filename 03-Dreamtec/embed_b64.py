import base64
import os

base_dir = r"c:\Users\marrano\Desktop\Desarrollo\Firmas electronicas\firmas\PROYECTO FIRMAS\03-Dreamtec"
png_path = os.path.join(base_dir, "assets", "barra_inferior_dreamtec.png")

with open(png_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

b64_src = f"data:image/png;base64,{b64}"

html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="light dark">
<title>Firma Dreamtec</title>
<style>
/* Solo para previsualizar en navegador: Gmail/Outlook ignoran esto sin romper la firma */
.qr-btn img{transition:transform .18s ease,box-shadow .18s ease;}
.qr-btn:hover img{transform:translateY(-2px);box-shadow:0 4px 10px rgba(17,24,32,.15);}
</style>
</head>
<body style="margin:0;padding:24px;background:#f5f6f7;">
<!-- FIRMA: selecciona desde aquí hasta el final de la tabla, copia (Ctrl/Cmd+C) y pega en Gmail → Configuración → Firma, o en Outlook → Firmas. -->
<!-- IMPORTANTE: antes de usarla, sube los archivos de assets/ (GIF, logo Ofimundo y los 2 QR png) a tu sitio (ej: https://www.dreamtec.cl/firma/) y reemplaza las rutas "assets/..." por las URLs https completas. -->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="720" style="width:720px;max-width:720px;background:#ffffff;border:1px solid #e8ebee;border-radius:8px;border-collapse:collapse;overflow:hidden;font-family:'Segoe UI',Calibri,'Helvetica Neue',Helvetica,Arial,sans-serif;">
  <tr>
    <!-- Logo animado con línea divisoria cian a la derecha -->
    <td width="151" valign="middle" style="width:151px;padding:16px 0 14px 16px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td valign="middle" align="center" style="padding-right:12px;">
            <a href="https://www.dreamtec.cl" style="text-decoration:none;">
              <img src="https://d3d57fbyf4vdnc.cloudfront.net/firma_dreamtec/02-elementos/dreamtec-logo-animado.gif" alt="Dreamtec" width="125" style="display:block;width:125px;height:auto;border:0;">
            </a>
          </td>
          <td width="2" valign="middle" align="center" style="width:2px;padding:0;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" height="95" style="height:95px;border-collapse:collapse;">
              <tr>
                <td width="2" height="95" style="width:2px;height:95px;font-size:1px;line-height:1px;background-color:#00BED5;border-right:2px solid #00BED5;padding:0;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
    <!-- Foto de perfil -->
    <td width="161" valign="middle" align="center" style="width:161px;padding:16px 8px 14px 8px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto;">
        <tr>
          <td style="padding:0;line-height:0;font-size:0;">
            <img src="{{foto_empleado}}" alt="Foto de perfil" width="125" height="125" style="display:block;width:125px;max-width:125px;height:125px;max-height:125px;border-radius:50%;object-fit:cover;border:0;">
          </td>
        </tr>
      </table>
    </td>
    <!-- Datos -->
    <td width="248" valign="middle" style="width:248px;padding:16px 8px 14px 8px;overflow:hidden;">
      <div style="font-size:20px;line-height:24px;font-weight:bold;color:#000000;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;mso-line-height-rule:exactly;">{{nombre_empleado}}</div>
      <div style="font-size:14px;line-height:18px;font-weight:bold;color:#00BED5;padding-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;mso-line-height-rule:exactly;">{{cargo_empleado}} · Dreamtec</div>
      <div style="font-size:13px;line-height:18px;color:#000000;padding-top:5px;mso-line-height-rule:exactly;">
        <a href="tel:+{{celular_empleado}}" style="color:#000000;text-decoration:none;">+{{celular_empleado}}</a><br>
        <a href="mailto:{{correo_empleado}}" style="color:#000000;text-decoration:none;">{{correo_empleado}}</a><br>
        <a href="https://www.dreamtec.cl" style="color:#00BED5;font-weight:bold;text-decoration:none;">www.dreamtec.cl</a>
      </div>
    </td>
    <!-- QRs -->
    <td width="160" valign="middle" style="width:160px;padding:16px 16px 14px 0;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="2" valign="middle" align="center" style="width:2px;padding:0;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" height="95" style="height:95px;border-collapse:collapse;">
              <tr>
                <td width="2" height="95" style="width:2px;height:95px;font-size:1px;line-height:1px;background-color:#00BED5;border-right:2px solid #00BED5;padding:0;">&nbsp;</td>
              </tr>
            </table>
          </td>
          <td valign="middle" align="center" style="padding-left:10px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td align="center" style="padding-right:6px;">
                  <a class="qr-btn" href="https://wa.me/{{celular_empleado}}" style="text-decoration:none;">
                    <img src="{{qr_wsp}}" alt="QR WhatsApp" width="56" height="56" style="display:block;width:56px;max-width:56px;height:56px;max-height:56px;border:1.5px solid #00BED5;border-radius:8px;padding:3px;">
                    <span style="display:block;font-size:9px;font-weight:bold;letter-spacing:0.5px;color:#00BED5;padding-top:4px;text-align:center;">WHATSAPP</span>
                  </a>
                </td>
                <td align="center">
                  <a class="qr-btn" href="{{linkedin}}" style="text-decoration:none;">
                    <img src="{{qr_linkedin}}" alt="QR LinkedIn" width="56" height="56" style="display:block;width:56px;max-width:56px;height:56px;max-height:56px;border:1.5px solid #00BED5;border-radius:8px;padding:3px;">
                    <span style="display:block;font-size:9px;font-weight:bold;letter-spacing:0.5px;color:#00BED5;padding-top:4px;text-align:center;">LINKEDIN</span>
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  <!-- Franja del grupo con degradado -->
  <tr>
    <td colspan="4" width="720" style="width:720px;padding:0;margin:0;line-height:0;font-size:0;height:36px;">
      <a href="https://www.ofimundo.cl" style="text-decoration:none;display:block;"><img src="BAN_B64" alt="DREAMTEC · PARTE DEL GRUPO OFIMUNDO" width="720" height="36" style="display:block;width:720px;max-width:720px;height:36px;border:0;border-radius:0 0 8px 8px;outline:none;"></a>
    </td>
  </tr>
</table>
</body>
</html>
'''.replace("BAN_B64", b64_src)

html_path = os.path.join(base_dir, "diseño_dreamtec.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("[OK] diseño_dreamtec.html actualizado con placeholders {{...}} y líneas TD compatibles con Outlook.")
