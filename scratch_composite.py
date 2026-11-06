import os
import io
import urllib.request
import urllib.parse
import ssl
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw

def fetch_isolated_flux_asset(prompt: str, width: int = 1024, height: int = 640) -> Image.Image:
    full_prompt = f"{prompt}, studio lighting on pure plain solid white background, isolated on pure solid white background, 8k product render, architectural digest, centered front perspective view"
    encoded = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model=flux&nologo=true&seed=42"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, timeout=40, context=ctx) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")

def extract_alpha_mask(asset_img: Image.Image) -> Image.Image:
    """Extracts high quality alpha mask from white studio background."""
    arr = np.array(asset_img).astype(np.float32)
    # Distance from white (255, 255, 255)
    dist = np.sqrt(np.sum((255.0 - arr) ** 2, axis=2))
    # Threshold & smooth
    # Pixels where dist < 25 are background (white), dist > 55 are solid foreground
    alpha = np.clip((dist - 20.0) / 40.0 * 255.0, 0, 255).astype(np.uint8)
    mask = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=0.8))
    return mask

def composite_asset_on_room(orig_img: Image.Image, asset_img: Image.Image, mask: Image.Image, target_bbox=None) -> Image.Image:
    w, h = orig_img.size
    result = orig_img.copy()

    # If target_bbox given, resize asset & mask
    if target_bbox:
        bx1, by1, bx2, by2 = target_bbox
        bw = bx2 - bx1
        bh = by2 - by1
        scaled_asset = asset_img.resize((bw, bh), Image.Resampling.LANCZOS)
        scaled_mask = mask.resize((bw, bh), Image.Resampling.LANCZOS)
    else:
        bx1, by1 = 0, 0
        scaled_asset = asset_img.resize((w, h), Image.Resampling.LANCZOS)
        scaled_mask = mask.resize((w, h), Image.Resampling.LANCZOS)

    # 1. Create realistic ground drop shadow on user's floor
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    if target_bbox:
        s_draw.ellipse([bx1 - 20, by2 - 25, bx2 + 20, by2 + 35], fill=(0, 0, 0, 140))
        s_draw.ellipse([bx1 + 10, by2 - 15, bx2 - 10, by2 + 20], fill=(0, 0, 0, 180))
    else:
        s_draw.ellipse([int(w*0.2), int(h*0.75), int(w*0.8), int(h*0.95)], fill=(0, 0, 0, 150))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=14))
    result.paste(shadow_layer, (0, 0), shadow_layer)

    # 2. Paste asset with alpha mask
    asset_rgba = scaled_asset.convert("RGBA")
    asset_rgba.putalpha(scaled_mask)
    
    # Harmonize ambient lighting: slightly tint asset to match dark concrete room if room is dark
    orig_np = np.array(orig_img)
    mean_val = float(np.mean(orig_np))
    if mean_val < 90: # Dark room
        enhancer = ImageEnhance.Brightness(asset_rgba)
        asset_rgba = enhancer.enhance(0.88)
        enhancer = ImageEnhance.Contrast(asset_rgba)
        asset_rgba = enhancer.enhance(1.08)

    result.paste(asset_rgba, (bx1, by1), asset_rgba)
    return result

def test_bed_composite():
    orig_path = "storage/uploads/orig_d4da1bc102.jpg"
    orig = Image.open(orig_path).convert("RGB")
    w, h = orig.size
    print(f"Original room size: {w}x{h}")

    prompt = "modern luxury dark charcoal upholstered platform bed with grey linen bedding pillows and small round black stone side table"
    print("Fetching isolated FLUX asset...")
    asset = fetch_isolated_flux_asset(prompt, width=1024, height=640)
    mask = extract_alpha_mask(asset)

    # Place bed centered on user's room floor against back wall
    bed_x1 = int(w * 0.24)
    bed_y1 = int(h * 0.40)
    bed_x2 = int(w * 0.78)
    bed_y2 = int(h * 0.88)
    
    output = composite_asset_on_room(orig, asset, mask, target_bbox=(bed_x1, bed_y1, bed_x2, bed_y2))
    os.makedirs("storage/generated", exist_ok=True)
    out_file = "storage/generated/test_exact_room_bed.jpg"
    output.save(out_file, format="JPEG", quality=95)
    print(f"Saved exact room composite to {out_file}")

if __name__ == "__main__":
    test_bed_composite()
