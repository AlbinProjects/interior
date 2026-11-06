import urllib.request
import urllib.parse
import os
import io
import time
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np

def generate_ai_photorealistic_scene(prompt: str, width: int = 1024, height: int = 640) -> Image.Image:
    """Fetches high-quality FLUX/SDXL interior render from generative AI endpoint."""
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model=flux&nologo=true&seed=42"
    req = urllib.request.Request(url, headers={"User-Agent": "AI-Interior-Designer/2.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    return Image.open(io.BytesIO(data)).convert("RGB")

if __name__ == "__main__":
    prompt = (
        "photorealistic interior design photo, 8k, modern minimalist luxury master bedroom in dark concrete architecture room, "
        "low dark platform bed with charcoal upholstered channel headboard, plush charcoal and slate linen duvet with natural soft folds, "
        "layered double pillows, right side round dark stone pedestal nightstand with small ceramic vase and single green branch, "
        "warm overhead spotlight beams shining down on dark textured feature wall, polished dark concrete floor with soft contact shadows, "
        "architectural digest photography, ultra realistic, highly detailed, master interior design"
    )
    print("Requesting AI image generation...")
    try:
        t0 = time.time()
        img = generate_ai_photorealistic_scene(prompt, 1024, 640)
        t1 = time.time()
        print(f"Generated image in {t1 - t0:.2f}s: size={img.size}")
        img.save("scratch_ai_generated.jpg")
        print("Saved to scratch_ai_generated.jpg")
    except Exception as e:
        print(f"Generation error: {e}")
