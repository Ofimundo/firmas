import os
import struct
import zlib

def interpolate(c1, c2, factor):
    return int(round(c1 + (c2 - c1) * factor))

def get_gradient_color(x, width):
    t = x / float(width - 1)
    
    # Stops: 0.0 -> #008EA0 (0, 142, 160)
    #        0.3 -> #00BED5 (0, 190, 213)
    #        0.65-> #2B2A5C (43, 42, 92)
    #        1.0 -> #8F1E7B (143, 30, 123)
    
    if t <= 0.3:
        factor = t / 0.3
        r = interpolate(0, 0, factor)
        g = interpolate(142, 190, factor)
        b = interpolate(160, 213, factor)
    elif t <= 0.65:
        factor = (t - 0.3) / 0.35
        r = interpolate(0, 43, factor)
        g = interpolate(190, 42, factor)
        b = interpolate(213, 92, factor)
    else:
        factor = (t - 0.65) / 0.35
        r = interpolate(43, 143, factor)
        g = interpolate(42, 30, factor)
        b = interpolate(92, 123, factor)
        
    return (r, g, b)

def make_png(width, height):
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    ihdr_data = struct.pack('!IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack('!I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('!I', ihdr_crc)
    
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # Filter type 0
        for x in range(width):
            r, g, b = get_gradient_color(x, width)
            raw_data.extend([r, g, b])
            
    compressed = zlib.compress(bytes(raw_data), 9)
    idat_crc = zlib.crc32(b'IDAT' + compressed) & 0xffffffff
    png += struct.pack('!I', len(compressed)) + b'IDAT' + compressed + struct.pack('!I', idat_crc)
    
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    png += struct.pack('!I', 0) + b'IEND' + struct.pack('!I', iend_crc)
    
    return bytes(png)

assets_dir = r"c:\Users\marrano\Desktop\Desarrollo\Firmas electronicas\03-Dreamtec\assets"
os.makedirs(assets_dir, exist_ok=True)
output_path = os.path.join(assets_dir, "degradado_dreamtec.png")

png_bytes = make_png(600, 40)
with open(output_path, "wb") as f:
    f.write(png_bytes)

print(f"Generated PNG: {output_path} ({len(png_bytes)} bytes)")
