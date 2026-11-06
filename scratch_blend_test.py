import os
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

def blend_ai_into_original_room(orig_path: str, ai_path: str, output_path: str):
    orig = Image.open(orig_path).convert("RGB")
    ai_gen = Image.open(ai_path).convert("RGB")
    
    # Resize AI generation to match original exactly
    w, h = orig.size
    ai_gen = ai_gen.resize((w, h), Image.Resampling.LANCZOS)
    
    # Match color temperature & histogram of the original room
    orig_np = np.array(orig).astype(np.float32)
    ai_np = np.array(ai_gen).astype(np.float32)
    
    # Create precision structure mask:
    # Wall/Ceiling (top ~42%) and far edges (right window, left wall) are preserved 100% from original photo
    # Editing zone is the floor & central furniture area (y: 0.38h to 0.90h, x: 0.14w to 0.88w)
    mask = np.zeros((h, w), dtype=np.float32)
    
    # Define furniture placement polygon
    cv2.fillPoly(mask, [np.array([
        [int(w * 0.16), int(h * 0.38)],
        [int(w * 0.84), int(h * 0.38)],
        [int(w * 0.88), int(h * 0.88)],
        [int(w * 0.12), int(h * 0.88)]
    ], dtype=np.int32)], 1.0)
    
    # Gaussian blur mask for seamless feathering
    mask = cv2.GaussianBlur(mask, (31, 31), 11.0)
    mask_3ch = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
    
    # Blend
    composite = orig_np * (1.0 - mask_3ch) + ai_np * mask_3ch
    composite = np.clip(composite, 0, 255).astype(np.uint8)
    
    result_img = Image.fromarray(composite)
    result_img.save(output_path, quality=95)
    print(f"Composite saved to {output_path}")

if __name__ == "__main__":
    blend_ai_into_original_room(
        "storage/uploads/orig_d4da1bc102.jpg",
        "scratch_ai_generated.jpg",
        "scratch_composite_spacely_result.jpg"
    )
