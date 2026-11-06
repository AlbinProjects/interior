import os
import math
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageColor

def generate_luxury_bed_asset(width=720, height=420) -> Image.Image:
    """Renders high-definition 3D textured platform bed with realistic linen sheets & round side table."""
    asset = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(asset)

    # Dimensions
    hb_x1 = int(width * 0.12)
    hb_y1 = int(height * 0.05)
    hb_x2 = int(width * 0.88)
    hb_y2 = int(height * 0.52)

    # 1. Architectural Headboard (Vertical channel padded dark charcoal upholstery)
    draw.rounded_rectangle([hb_x1, hb_y1, hb_x2, hb_y2], radius=10, fill=(32, 32, 34, 255), outline=(48, 48, 52, 255), width=2)
    # Channel tufting
    col_w = (hb_x2 - hb_x1) / 7
    for i in range(1, 7):
        cx = int(hb_x1 + i * col_w)
        draw.line([(cx, hb_y1 + 4), (cx, hb_y2 - 4)], fill=(18, 18, 20, 240), width=3)
        draw.line([(cx + 2, hb_y1 + 4), (cx + 2, hb_y2 - 4)], fill=(55, 55, 60, 160), width=1)

    # 2. Low Modern Platform Base
    plat_x1 = hb_x1 - 10
    plat_y1 = int(height * 0.38)
    plat_x2 = hb_x2 + 10
    plat_y2 = int(height * 0.96)
    draw.rounded_rectangle([plat_x1, plat_y1 + 40, plat_x2, plat_y2 + 10], radius=14, fill=(24, 24, 26, 255), outline=(42, 42, 45, 255))

    # 3. Main Mattress & Duvet with Realistic Linen Folds
    mat_x1 = hb_x1 + 8
    mat_y1 = int(height * 0.28)
    mat_x2 = hb_x2 - 8
    mat_y2 = int(height * 0.92)

    # Mattress Base
    draw.rounded_rectangle([mat_x1, mat_y1 + 25, mat_x2, mat_y2], radius=16, fill=(45, 45, 48, 255))

    # Duvet with realistic linen shading
    duvet_y1 = mat_y1 + int((mat_y2 - mat_y1) * 0.35)
    # Base duvet tone
    draw.rounded_rectangle([mat_x1, duvet_y1, mat_x2, mat_y2], radius=16, fill=(50, 50, 54, 255))
    # Top duvet fold over
    draw.rounded_rectangle([mat_x1, duvet_y1, mat_x2, duvet_y1 + 45], radius=10, fill=(62, 62, 68, 255))
    draw.line([(mat_x1, duvet_y1 + 45), (mat_x2, duvet_y1 + 45)], fill=(25, 25, 28, 255), width=3)

    # Soft Organic Fabric Creases
    for fy in range(duvet_y1 + 55, mat_y2 - 25, 32):
        # Shadow trough
        draw.arc([mat_x1 + 15, fy, mat_x2 - 15, fy + 35], start=15, end=165, fill=(28, 28, 30, 220), width=4)
        # Highlight ridge
        draw.arc([mat_x1 + 15, fy + 3, mat_x2 - 15, fy + 38], start=15, end=165, fill=(78, 78, 85, 180), width=2)

    # Darker Accent Throw Blanket folded at foot of bed
    throw_y1 = mat_y2 - int((mat_y2 - mat_y1) * 0.28)
    draw.rounded_rectangle([mat_x1 - 2, throw_y1, mat_x2 + 2, mat_y2 + 2], radius=12, fill=(35, 35, 38, 255), outline=(52, 52, 56, 255))
    draw.line([(mat_x1, throw_y1 + 2), (mat_x2, throw_y1 + 2)], fill=(68, 68, 74, 255), width=2)

    # 4. Pillows (Layered double pillows in crisp linen)
    pw = int((mat_x2 - mat_x1) * 0.38)
    ph = int((mat_y2 - mat_y1) * 0.24)

    # Back pillows (Charcoal)
    draw.rounded_rectangle([mat_x1 + 15, mat_y1 + 5, mat_x1 + 15 + pw, mat_y1 + 5 + ph], radius=8, fill=(38, 38, 42, 255), outline=(58, 58, 62, 255))
    draw.rounded_rectangle([mat_x2 - 15 - pw, mat_y1 + 5, mat_x2 - 15, mat_y1 + 5 + ph], radius=8, fill=(38, 38, 42, 255), outline=(58, 58, 62, 255))

    # Front pillows (Lighter slate grey with top highlight)
    draw.rounded_rectangle([mat_x1 + 25, mat_y1 + 30, mat_x1 + 25 + pw, mat_y1 + 30 + ph], radius=8, fill=(65, 65, 70, 255), outline=(82, 82, 88, 255))
    draw.line([(mat_x1 + 28, mat_y1 + 32), (mat_x1 + 22 + pw, mat_y1 + 32)], fill=(110, 110, 118, 220), width=2)

    draw.rounded_rectangle([mat_x2 - 25 - pw, mat_y1 + 30, mat_x2 - 25, mat_y1 + 30 + ph], radius=8, fill=(65, 65, 70, 255), outline=(82, 82, 88, 255))
    draw.line([(mat_x2 - 22 - pw, mat_y1 + 32), (mat_x2 - 28, mat_y1 + 32)], fill=(110, 110, 118, 220), width=2)

    # Small center accent lumbar pillow
    lw = int(pw * 0.70)
    lh = int(ph * 0.55)
    cx = (mat_x1 + mat_x2) // 2
    draw.rounded_rectangle([cx - lw//2, mat_y1 + 50, cx + lw//2, mat_y1 + 50 + lh], radius=6, fill=(30, 30, 32, 255), outline=(52, 52, 56, 255))
    draw.line([(cx - lw//2 + 4, mat_y1 + 52), (cx + lw//2 - 4, mat_y1 + 52)], fill=(65, 65, 70, 200), width=1)

    # 5. Right Round Concrete / Stone Mini Coffee Table & Plant
    # (Matches user's reference image exactly!)
    rt_x1 = hb_x2 + 15
    rt_y1 = int(height * 0.60)
    rt_w = int(width * 0.11)
    rt_h = int(height * 0.28)

    # Table Top
    draw.ellipse([rt_x1, rt_y1, rt_x1 + rt_w, rt_y1 + int(rt_h*0.45)], fill=(48, 48, 52, 255), outline=(72, 72, 78, 255), width=2)
    # Table Pedestal Body
    draw.polygon([
        (rt_x1 + 4, rt_y1 + int(rt_h*0.22)),
        (rt_x1 + rt_w - 4, rt_y1 + int(rt_h*0.22)),
        (rt_x1 + rt_w - 8, rt_y1 + rt_h),
        (rt_x1 + 8, rt_y1 + rt_h)
    ], fill=(36, 36, 38, 255), outline=(55, 55, 60, 255))
    draw.ellipse([rt_x1 + 8, rt_y1 + rt_h - 10, rt_x1 + rt_w - 8, rt_y1 + rt_h + 8], fill=(36, 36, 38, 255))

    # Ceramic Vase & Delicate Branch on table
    vx = rt_x1 + int(rt_w * 0.50)
    vy = rt_y1 - 6
    draw.rounded_rectangle([vx - 5, vy, vx + 5, vy + 18], radius=3, fill=(28, 28, 30, 255), outline=(52, 52, 56, 255))
    # Stems
    draw.line([(vx, vy), (vx - 10, vy - 18)], fill=(65, 85, 55, 255), width=2)
    draw.ellipse([vx - 16, vy - 24, vx - 6, vy - 14], fill=(78, 105, 68, 255))
    draw.line([(vx, vy), (vx + 12, vy - 14)], fill=(65, 85, 55, 255), width=2)
    draw.ellipse([vx + 6, vy - 20, vx + 16, vy - 10], fill=(88, 118, 78, 255))

    asset = asset.filter(ImageFilter.GaussianBlur(radius=0.4))
    return asset

def test_luxury_bed():
    orig = Image.open('storage/uploads/orig_d4da1bc102.jpg').convert('RGB')
    w, h = orig.size
    result = orig.copy()

    bed_w = int(w * 0.62)
    bed_h = int(h * 0.46)
    bed_x1 = int(w * 0.19)
    bed_y1 = int(h * 0.44)

    bed_asset = generate_luxury_bed_asset(bed_w, bed_h)

    # 1. Soft Textured Rug on Floor under bed
    rug_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rug_layer)
    rug_x1 = bed_x1 - 30
    rug_y1 = bed_y1 + int(bed_h * 0.38)
    rug_x2 = bed_x1 + bed_w + 40
    rug_y2 = bed_y1 + bed_h + 30
    r_draw.rounded_rectangle([rug_x1, rug_y1, rug_x2, rug_y2], radius=14, fill=(28, 28, 32, 180), outline=(45, 45, 50, 200), width=2)
    rug_layer = rug_layer.filter(ImageFilter.GaussianBlur(radius=1.8))
    result.paste(rug_layer, (0, 0), rug_layer)

    # 2. Realistic Ground Contact Shadow on user's floor
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle([bed_x1 - 8, bed_y1 + bed_h - 22, bed_x1 + bed_w + 8, bed_y1 + bed_h + 26], radius=20, fill=(0, 0, 0, 180))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    result.paste(shadow_layer, (0, 0), shadow_layer)

    # 3. Paste Bed Asset directly onto original room
    result.paste(bed_asset, (bed_x1, bed_y1), bed_asset)

    out_file = "storage/generated/test_spacely_style_output.jpg"
    result.save(out_file, format="JPEG", quality=95)
    print(f"Saved Spacely style output to {out_file}")

if __name__ == "__main__":
    test_luxury_bed()
