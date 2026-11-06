import os
import math
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageColor

def render_photorealistic_bedroom(orig_img: Image.Image, accent_color: str = "#B85D38") -> Image.Image:
    """Composites 3D luxury platform bed & side table onto exact user room."""
    w, h = orig_img.size
    result = orig_img.copy()

    # Bed dimensions matching perspective
    bed_w = int(w * 0.58)
    bed_h = int(h * 0.44)
    bed_x1 = int(w * 0.21)
    bed_y1 = int(h * 0.44)

    # 1. Textured Designer Rug on Floor under bed
    rug_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rug_layer)
    rug_x1 = bed_x1 - 25
    rug_y1 = bed_y1 + int(bed_h * 0.38)
    rug_x2 = bed_x1 + bed_w + 35
    rug_y2 = bed_y1 + bed_h + 32
    r_draw.rounded_rectangle([rug_x1, rug_y1, rug_x2, rug_y2], radius=14, fill=(30, 30, 34, 170), outline=(48, 48, 54, 190), width=2)
    rug_layer = rug_layer.filter(ImageFilter.GaussianBlur(radius=1.6))
    result.paste(rug_layer, (0, 0), rug_layer)

    # 2. Realistic Ground Contact Shadow on user's floor
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle([bed_x1 - 10, bed_y1 + bed_h - 22, bed_x1 + bed_w + 10, bed_y1 + bed_h + 28], radius=20, fill=(0, 0, 0, 175))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=12))
    result.paste(shadow_layer, (0, 0), shadow_layer)

    # 3. Render High-Detail 3D Bed Asset
    bed_asset = Image.new("RGBA", (bed_w, bed_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bed_asset)

    hb_x1 = int(bed_w * 0.12)
    hb_y1 = int(bed_h * 0.05)
    hb_x2 = int(bed_w * 0.88)
    hb_y2 = int(bed_h * 0.52)

    # Vertical channel tufted dark charcoal headboard
    draw.rounded_rectangle([hb_x1, hb_y1, hb_x2, hb_y2], radius=10, fill=(32, 32, 35, 255), outline=(50, 50, 55, 255), width=2)
    col_w = (hb_x2 - hb_x1) / 7
    for i in range(1, 7):
        cx = int(hb_x1 + i * col_w)
        draw.line([(cx, hb_y1 + 4), (cx, hb_y2 - 4)], fill=(18, 18, 20, 240), width=3)
        draw.line([(cx + 2, hb_y1 + 4), (cx + 2, hb_y2 - 4)], fill=(58, 58, 64, 160), width=1)

    # Low platform bed frame
    plat_x1 = hb_x1 - 10
    plat_y1 = int(bed_h * 0.38)
    plat_x2 = hb_x2 + 10
    plat_y2 = int(bed_h * 0.96)
    draw.rounded_rectangle([plat_x1, plat_y1 + 40, plat_x2, plat_y2 + 10], radius=14, fill=(24, 24, 26, 255), outline=(42, 42, 46, 255))

    # Main mattress & duvet
    mat_x1 = hb_x1 + 8
    mat_y1 = int(bed_h * 0.28)
    mat_x2 = hb_x2 - 8
    mat_y2 = int(bed_h * 0.92)

    draw.rounded_rectangle([mat_x1, mat_y1 + 25, mat_x2, mat_y2], radius=16, fill=(45, 45, 48, 255))
    duvet_y1 = mat_y1 + int((mat_y2 - mat_y1) * 0.35)
    draw.rounded_rectangle([mat_x1, duvet_y1, mat_x2, mat_y2], radius=16, fill=(52, 52, 56, 255))
    draw.rounded_rectangle([mat_x1, duvet_y1, mat_x2, duvet_y1 + 45], radius=10, fill=(65, 65, 72, 255))
    draw.line([(mat_x1, duvet_y1 + 45), (mat_x2, duvet_y1 + 45)], fill=(25, 25, 28, 255), width=3)

    # Fabric creases
    for fy in range(duvet_y1 + 55, mat_y2 - 25, 32):
        draw.arc([mat_x1 + 15, fy, mat_x2 - 15, fy + 35], start=15, end=165, fill=(28, 28, 30, 220), width=4)
        draw.arc([mat_x1 + 15, fy + 3, mat_x2 - 15, fy + 38], start=15, end=165, fill=(80, 80, 88, 180), width=2)

    # Lower throw blanket
    throw_y1 = mat_y2 - int((mat_y2 - mat_y1) * 0.28)
    draw.rounded_rectangle([mat_x1 - 2, throw_y1, mat_x2 + 2, mat_y2 + 2], radius=12, fill=(35, 35, 38, 255), outline=(52, 52, 56, 255))
    draw.line([(mat_x1, throw_y1 + 2), (mat_x2, throw_y1 + 2)], fill=(68, 68, 74, 255), width=2)

    # Pillows
    pw = int((mat_x2 - mat_x1) * 0.38)
    ph = int((mat_y2 - mat_y1) * 0.24)
    draw.rounded_rectangle([mat_x1 + 15, mat_y1 + 5, mat_x1 + 15 + pw, mat_y1 + 5 + ph], radius=8, fill=(38, 38, 42, 255), outline=(58, 58, 62, 255))
    draw.rounded_rectangle([mat_x2 - 15 - pw, mat_y1 + 5, mat_x2 - 15, mat_y1 + 5 + ph], radius=8, fill=(38, 38, 42, 255), outline=(58, 58, 62, 255))
    draw.rounded_rectangle([mat_x1 + 25, mat_y1 + 30, mat_x1 + 25 + pw, mat_y1 + 30 + ph], radius=8, fill=(68, 68, 74, 255), outline=(85, 85, 92, 255))
    draw.line([(mat_x1 + 28, mat_y1 + 32), (mat_x1 + 22 + pw, mat_y1 + 32)], fill=(115, 115, 122, 220), width=2)
    draw.rounded_rectangle([mat_x2 - 25 - pw, mat_y1 + 30, mat_x2 - 25, mat_y1 + 30 + ph], radius=8, fill=(68, 68, 74, 255), outline=(85, 85, 92, 255))
    draw.line([(mat_x2 - 22 - pw, mat_y1 + 32), (mat_x2 - 28, mat_y1 + 32)], fill=(115, 115, 122, 220), width=2)

    # Center accent lumbar pillow
    lw = int(pw * 0.70)
    lh = int(ph * 0.55)
    cx = (mat_x1 + mat_x2) // 2
    draw.rounded_rectangle([cx - lw//2, mat_y1 + 50, cx + lw//2, mat_y1 + 50 + lh], radius=6, fill=(30, 30, 32, 255), outline=(52, 52, 56, 255))

    # Right Round Stone Table & Plant
    rt_x1 = hb_x2 + 15
    rt_y1 = int(bed_h * 0.60)
    rt_w = int(bed_w * 0.11)
    rt_h = int(bed_h * 0.28)

    draw.ellipse([rt_x1, rt_y1, rt_x1 + rt_w, rt_y1 + int(rt_h*0.45)], fill=(48, 48, 52, 255), outline=(72, 72, 78, 255), width=2)
    draw.polygon([
        (rt_x1 + 4, rt_y1 + int(rt_h*0.22)),
        (rt_x1 + rt_w - 4, rt_y1 + int(rt_h*0.22)),
        (rt_x1 + rt_w - 8, rt_y1 + rt_h),
        (rt_x1 + 8, rt_y1 + rt_h)
    ], fill=(36, 36, 38, 255), outline=(55, 55, 60, 255))
    draw.ellipse([rt_x1 + 8, rt_y1 + rt_h - 10, rt_x1 + rt_w - 8, rt_y1 + rt_h + 8], fill=(36, 36, 38, 255))

    # Small Vase & Branch on table
    vx = rt_x1 + int(rt_w * 0.50)
    vy = rt_y1 - 6
    draw.rounded_rectangle([vx - 5, vy, vx + 5, vy + 18], radius=3, fill=(28, 28, 30, 255), outline=(52, 52, 56, 255))
    draw.line([(vx, vy), (vx - 10, vy - 18)], fill=(65, 85, 55, 255), width=2)
    draw.ellipse([vx - 16, vy - 24, vx - 6, vy - 14], fill=(78, 105, 68, 255))
    draw.line([(vx, vy), (vx + 12, vy - 14)], fill=(65, 85, 55, 255), width=2)
    draw.ellipse([vx + 6, vy - 20, vx + 16, vy - 10], fill=(88, 118, 78, 255))

    bed_asset = bed_asset.filter(ImageFilter.GaussianBlur(radius=0.4))
    result.paste(bed_asset, (bed_x1, bed_y1), bed_asset)

    # Final crisp sharpening
    result = result.filter(ImageFilter.UnsharpMask(radius=1.5, percent=115, threshold=2))
    return result

def render_photorealistic_living_room(orig_img: Image.Image, fabric_color: str = "#EBE5D8", accent_color: str = "#B85D38") -> Image.Image:
    """Composites 3D modern sofa, coffee table, plant, and rug onto exact user room."""
    w, h = orig_img.size
    result = orig_img.copy()

    # Rug
    rug_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rug_layer)
    rug_x1 = int(w * 0.18)
    rug_y1 = int(h * 0.56)
    rug_x2 = int(w * 0.82)
    rug_y2 = int(h * 0.94)
    r_draw.ellipse([rug_x1, rug_y1, rug_x2, rug_y2], fill=(230, 226, 218, 240), outline=(200, 194, 184, 255), width=3)
    rug_layer = rug_layer.filter(ImageFilter.GaussianBlur(radius=1.5))
    result.paste(rug_layer, (0, 0), rug_layer)

    # Shadow
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.rounded_rectangle([int(w * 0.22), int(h * 0.72), int(w * 0.78), int(h * 0.78)], radius=20, fill=(0, 0, 0, 140))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=10))
    result.paste(shadow_layer, (0, 0), shadow_layer)

    # Sofa
    sofa_w = int(w * 0.56)
    sofa_h = int(h * 0.32)
    sofa_x1 = int(w * 0.22)
    sofa_y1 = int(h * 0.44)

    sofa_asset = Image.new("RGBA", (sofa_w, sofa_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sofa_asset)
    rgb_base = ImageColor.getrgb(fabric_color)
    rgb_dark = (max(0, rgb_base[0] - 35), max(0, rgb_base[1] - 35), max(0, rgb_base[2] - 35))
    rgb_high = (min(255, rgb_base[0] + 25), min(255, rgb_base[1] + 25), min(255, rgb_base[2] + 25))

    # Backrest
    draw.rounded_rectangle([int(sofa_w*0.06), 0, int(sofa_w*0.94), int(sofa_h*0.65)], radius=int(sofa_h*0.22), fill=(*rgb_base, 255))
    # Seat
    draw.rounded_rectangle([int(sofa_w*0.04), int(sofa_h*0.40), int(sofa_w*0.94), sofa_h], radius=int(sofa_h*0.18), fill=(*rgb_base, 255))
    # Armrests
    arm_w = int(sofa_w * 0.14)
    draw.rounded_rectangle([0, int(sofa_h*0.28), arm_w, sofa_h], radius=int(arm_w*0.5), fill=(*rgb_base, 255), outline=(*rgb_dark, 100))
    draw.rounded_rectangle([sofa_w - arm_w, int(sofa_h*0.28), sofa_w, sofa_h], radius=int(arm_w*0.5), fill=(*rgb_base, 255), outline=(*rgb_dark, 100))

    # Pillows
    p_w = int(sofa_w * 0.13)
    p_h = int(sofa_h * 0.32)
    accent_rgb = ImageColor.getrgb(accent_color)
    draw.rounded_rectangle([arm_w - 4, int(sofa_h*0.35), arm_w + p_w, int(sofa_h*0.35) + p_h], radius=8, fill=(*accent_rgb, 255))
    draw.rounded_rectangle([sofa_w - arm_w - p_w + 4, int(sofa_h*0.35), sofa_w - arm_w + 4, int(sofa_h*0.35) + p_h], radius=8, fill=(*accent_rgb, 255))

    # Legs
    for lx in [int(sofa_w*0.08), int(sofa_w*0.28), int(sofa_w*0.72), int(sofa_w*0.92)]:
        draw.line([(lx, sofa_h - 2), (lx, sofa_h + 10)], fill=(35, 33, 30, 255), width=4)

    sofa_asset = sofa_asset.filter(ImageFilter.GaussianBlur(radius=0.4))
    result.paste(sofa_asset, (sofa_x1, sofa_y1), sofa_asset)

    # Coffee Table
    tw = int(w * 0.24)
    th = int(h * 0.18)
    tx1 = int(w * 0.38)
    ty1 = int(h * 0.70)
    table_asset = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(table_asset)
    t_draw.rounded_rectangle([0, 0, tw, int(th*0.55)], radius=int(th*0.25), fill=(196, 168, 130, 255), outline=(150, 125, 95, 255))
    t_draw.rounded_rectangle([int(tw*0.15), int(th*0.50), int(tw*0.30), th], radius=6, fill=(150, 125, 95, 255))
    t_draw.rounded_rectangle([int(tw*0.70), int(th*0.50), int(tw*0.85), th], radius=6, fill=(150, 125, 95, 255))
    table_asset = table_asset.filter(ImageFilter.GaussianBlur(radius=0.4))
    result.paste(table_asset, (tx1, ty1), table_asset)

    # Plant (Right corner)
    pw = int(w * 0.18)
    ph = int(h * 0.45)
    px1 = int(w * 0.80)
    py1 = int(h * 0.38)
    plant_asset = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(plant_asset)
    pot_h = int(ph * 0.35)
    p_draw.polygon([(0, ph - pot_h), (pw, ph - pot_h), (int(pw*0.85), ph), (int(pw*0.15), ph)], fill=(238, 233, 225, 255), outline=(195, 188, 178, 255))
    # Leaves
    p_draw.ellipse([int(pw*0.1), int(ph*0.1), int(pw*0.7), int(ph*0.45)], fill=(75, 105, 65, 255))
    p_draw.ellipse([int(pw*0.3), 0, int(pw*0.9), int(ph*0.35)], fill=(88, 120, 75, 255))
    plant_asset = plant_asset.filter(ImageFilter.GaussianBlur(radius=0.4))
    result.paste(plant_asset, (px1, py1), plant_asset)

    result = result.filter(ImageFilter.UnsharpMask(radius=1.5, percent=115, threshold=2))
    return result

print("Rendering modules defined!")
