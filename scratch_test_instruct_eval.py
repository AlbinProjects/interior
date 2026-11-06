import os
import time
import json
import torch
from pathlib import Path
from PIL import Image
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

os.makedirs("../NextjsReact/ai-room-redesign/ml/evaluation/comparisons", exist_ok=True)

print("Loading cached timbrooks/instruct-pix2pix pipeline...")
t0 = time.time()
pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(
    "timbrooks/instruct-pix2pix",
    dtype=torch.float32,
    safety_checker=None
)
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
print(f"Loaded in {time.time() - t0:.2f}s")

test_cases = [
    {
        "id": "test_01_empty_room",
        "name": "Empty Room Redesign",
        "image_path": "storage/uploads/orig_d4da1bc102.jpg",
        "prompt": "Transform this empty room into a modern Scandinavian living room with a comfortable fabric sofa, oak coffee table, and warm ambient floor lamp. Preserve the walls, windows, and ceiling.",
        "room_type": "living room",
        "design_style": "Scandinavian"
    },
    {
        "id": "test_02_furnished_living_room",
        "name": "Furnished Living Room Redesign",
        "image_path": "../NextjsReact/ai-room-redesign/public/styles/modern.jpg",
        "prompt": "Restyle this furnished room into an industrial modern living room with microcement textures, distressed leather seating, matte black metal accents, and warm track lighting. Preserve original walls, windows, and floor boundaries.",
        "room_type": "living room",
        "design_style": "industrial"
    },
    {
        "id": "test_03_bedroom_replacement",
        "name": "Bedroom Furniture Replacement",
        "image_path": "../NextjsReact/ai-room-redesign/public/styles/minimalist.jpg",
        "prompt": "Redesign this bedroom with a contemporary luxury low platform bed, charcoal linen duvet with soft fabric folds, plush double pillows, and minimal round nightstands. Preserve the original windows, walls, and perspective.",
        "room_type": "bedroom",
        "design_style": "contemporary luxury"
    }
]

results = []

for case in test_cases:
    print(f"\n--- Testing {case['name']} ({case['id']}) ---")
    img_path = case["image_path"]
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found!")
        continue
    
    orig_img = Image.open(img_path).convert("RGB")
    w, h = orig_img.size
    input_512 = orig_img.resize((512, 512), Image.Resampling.BICUBIC)
    
    # Save source copy
    src_out_path = f"../NextjsReact/ai-room-redesign/ml/evaluation/comparisons/{case['id']}_source.jpg"
    orig_img.save(src_out_path, quality=92)
    
    # Test setting: steps=15 (to balance CPU time and quality), image_guidance=1.5, guidance=7.5
    steps = 15
    g_scale = 7.5
    img_g_scale = 1.5
    
    print(f"Running inference (steps={steps}, guidance={g_scale}, img_guidance={img_g_scale})...")
    t_start = time.time()
    with torch.inference_mode():
        output = pipe(
            prompt=case["prompt"],
            image=input_512,
            num_inference_steps=steps,
            guidance_scale=g_scale,
            image_guidance_scale=img_g_scale
        )
    gen_duration = time.time() - t_start
    gen_img_512 = output.images[0]
    gen_img = gen_img_512.resize((w, h), Image.Resampling.LANCZOS)
    
    out_path = f"../NextjsReact/ai-room-redesign/ml/evaluation/comparisons/{case['id']}_instructpix2pix.jpg"
    gen_img.save(out_path, quality=92)
    print(f"Finished in {gen_duration:.2f}s, saved to {out_path}")
    
    results.append({
        "case_id": case["id"],
        "name": case["name"],
        "duration_seconds": round(gen_duration, 2),
        "steps": steps,
        "guidance_scale": g_scale,
        "image_guidance_scale": img_g_scale,
        "source_path": src_out_path,
        "output_path": out_path
    })

report_path = "../NextjsReact/ai-room-redesign/ml/evaluation/comparisons/instruct_pix2pix_test_results.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nEvaluation completed. Results saved to:", report_path)
