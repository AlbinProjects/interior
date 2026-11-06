import os
import io
import math
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageColor

def generate_photorealistic_bed_asset(width=800, height=500, color="charcoal") -> Image.Image:
    """Renders high-detail 3D textured platform bed matching modern luxury dark minimalist aesthetics."""
    asset = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(asset)

    # 1. Dark Upholstered Headboard (Wide architectural padded headboard)
    hb_x1 = int(width * 0.08)
    hb_y1 = int(height * 0.10)
    hb_x2 = int(width * 0.92)
    hb_y2 = int(height * 0.58)

    # Headboard base
    draw.rounded_rectangle([hb_x1, hb_y1, hb_x2, hb_y2], radius=12, fill=(38, 38, 40, 255), outline=(50, 50, 52, 255), width=2)
    # Headboard fabric texture lines (vertical channel tufting)
    for tx in range(hb_x1 + 40, hb_x2 - 30, 60):
        draw.line([(tx, hb_y1 + 5), (tx, hb_y2 - 5)], fill=(28, 28, 30, 220), width=2)
        draw.line([(tx + 2, hb_y1 + 5), (tx + 2, hb_y2 - 5)], fill=(58, 58, 62, 180), width=1)

    # 2. Side Nightstands (Left & Right dark minimalist stone tables)
    ns_w = int(width * 0.14)
    ns_h = int(height * 0.26)
    # Left nightstand
    draw.rounded_rectangle([hb_x1 - int(ns_w*0.85), hb_y2 - ns_h, hb_x1 - 5, hb_y2 + 20], radius=8, fill=(30, 30, 32, 255), outline=(48, 48, 50, 255))
    # Right nightstand (round stone table like in user reference image)
    draw.ellipse([hb_x2 + 10, hb_y2 - 20, hb_x2 + int(ns_w*0.9), hb_y2 + 35], fill=(32, 32, 34, 255), outline=(55, 55, 58, 255), width=2)
    # Small plant / vase on right nightstand
    vx = hb_x2 + int(ns_w*0.45)
    vy = hb_y2 - 35
    draw.ellipse([vx-6, vy, vx+6, vy+16], fill=(22, 22, 24, 255))
    draw.line([(vx, vy), (vx-8, vy-18)], fill=(65, 85, 55, 255), width=2)
    draw.ellipse([vx-14, vy-24, vx-4, vy-14], fill=(75, 100, 65, 255))
    draw.line([(vx, vy), (vx+10, vy-14)], fill=(65, 85, 55, 255), width=2)
    draw.ellipse([vx+4, vy-20, vx+14, vy-10], fill=(85, 115, 75, 255))

    # 3. Main Mattress & Layered Linen Duvet
    mat_x1 = int(width * 0.15)
    mat_y1 = int(height * 0.32)
    mat_x2 = int(width * 0.85)
    mat_y2 = int(height * 0.94)

    # Low Platform Bed Frame
    draw.rounded_rectangle([mat_x1 - 10, mat_y1 + 40, mat_x2 + 10, mat_y2 + 15], radius=16, fill=(28, 28, 30, 255), outline=(45, 45, 48, 255))

    # Plush Mattress Base with soft lighting gradient
    draw.rounded_rectangle([mat_x1, mat_y1 + 30, mat_x2, mat_y2], radius=18, fill=(48, 48, 52, 255))
    
    # Layered Duvet / Comforter (Charcoal linen fabric with realistic soft folds)
    duvet_y1 = mat_y1 + int((mat_y2 - mat_y1) * 0.38)
    draw.rounded_rectangle([mat_x1, duvet_y1, mat_x2, mat_y2], radius=16, fill=(42, 42, 45, 255))

    # Organic Duvet Folds & Creases (simulated depth shading)
    for fold_y in range(duvet_y1 + 30, mat_y2 - 20, 35):
        # Shadow crease
        draw.arc([mat_x1 + 20, fold_y, mat_x2 - 20, fold_y + 40], start=10, end=170, fill=(24, 24, 26, 200), width=3)
        # Highlight rim
        draw.arc([mat_x1 + 20, fold_y + 3, mat_x2 - 20, fold_y + 43], start=10, end=170, fill=(62, 62, 68, 180), width=2)

    # Accent Throw Blanket folded across lower foot of bed
    throw_y1 = mat_y2 - int((mat_y2 - mat_y1) * 0.28)
    draw.rounded_rectangle([mat_x1 - 2, throw_y1, mat_x2 + 2, mat_y2 + 2], radius=12, fill=(34, 34, 36, 255))
    draw.line([(mat_x1, throw_y1 + 2), (mat_x2, throw_y1 + 2)], fill=(58, 58, 62, 220), width=2)

    # 4. Pillows (Plush double layer pillows in charcoal / slate grey)
    pil_w = int((mat_x2 - mat_x1) * 0.36)
    pil_h = int((mat_y2 - mat_y1) * 0.24)
    
    # Back pillows
    draw.rounded_rectangle([mat_x1 + 20, mat_y1 + 10, mat_x1 + 20 + pil_w, mat_y1 + 10 + pil_h], radius=10, fill=(35, 35, 38, 255), outline=(52, 52, 56, 255))
    draw.rounded_rectangle([mat_x2 - 20 - pil_w, mat_y1 + 10, mat_x2 - 20, mat_y1 + 10 + pil_h], radius=10, fill=(35, 35, 38, 255), outline=(52, 52, 56, 255))

    # Front pillows (Slightly lighter textured grey)
    draw.rounded_rectangle([mat_x1 + 30, mat_y1 + 35, mat_x1 + 30 + pil_w, mat_y1 + 35 + pil_h], radius=10, fill=(52, 52, 56, 255), outline=(68, 68, 72, 255))
    draw.rounded_rectangle([mat_x2 - 30 - pil_w, mat_y1 + 35, mat_x2 - 30, mat_y1 + 35 + pil_h], radius=10, fill=(52, 52, 56, 255), outline=(68, 68, 72, 255))

    # Small center accent lumbar pillow
    lumb_w = int(pil_w * 0.7)
    lumb_h = int(pil_h * 0.6)
    cx = (mat_x1 + mat_x2) // 2
    draw.rounded_rectangle([cx - lumb_w//2, mat_y1 + 55, cx + lumb_w//2, mat_y1 + 55 + lumb_h], radius=8, fill=(30, 30, 32, 255), outline=(50, 50, 54, 255))

    asset = asset.filter(ImageFilter.GaussianBlur(radius=0.4))
    return asset

def test_render():
    orig = Image.open('storage/uploads/orig_d4da1bc102.jpg').convert('RGB')
    w, h = orig.size
    result = orig.copy()

    # Place bed centered on floor against back wall
    bed_w = int(w * 0.64)
    bed_h = int(h * 0.48)
    bed_x1 = int(w * 0.18)
    bed_y1 = int(h * 0.42)

    bed_asset = generate_photorealistic_bed_asset(bed_w, bed_h)

    # 1. Soft Textured Rug underneath bed
    rug_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rug_layer)
    rug_x1 = bed_x1 - 35
    rug_y1 = bed_y1 + int(bed_h * 0.35)
    rug_x2 = bed_x1 + bed_w + 55
    rug_y2 = bed_y1 + bed_h + 35
    r_draw.rounded_rectangle([rug_x1, rug_y1, rug_x2, rug_y2], radius=16, fill=(32, 32, 35, 160), outline=(48, 48, 52, 180), width=2)
    rug_layer = rug_layer.filter(ImageFilter.GaussianBlur(radius=1.5))
    result.paste(rug_layer, (0, 0), rug_layer)

    # 2. Contact Drop Shadow under bed on user's floor
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle([bed_x1 - 10, bed_y1 + bed_h - 25, bed_x1 + bed_w + 10, bed_y1 + bed_h + 30], radius=20, fill=(0, 0, 0, 160))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    result.paste(shadow_layer, (0, 0), shadow_layer)

    # 3. Paste Bed Asset directly onto original room
    result.paste(bed_asset, (bed_x1, bed_y1), bed_asset)

    out_file = "storage/generated/test_exact_room_output.jpg"
    result.save(out_file, format="JPEG", quality=95)
    print(f"Rendered exact room output to {out_file}")

if __name__ == "__main__":
    test_render()
