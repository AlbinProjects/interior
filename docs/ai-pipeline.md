# AI & Computer Vision Pipeline

## Structure-Preserving Pipeline Overview

Traditional text-to-image generators generate arbitrary compositions from textual prompts. SysInterior AI enforces spatial conditioning across all stages.

```
Original Image
  │
  ├─► 1. Validation & Orientation Check (Pillow / OpenCV)
  │
  ├─► 2. Object Detection (YOLOv8)
  │      └─ Extracted: Sofas, Chairs, Tables, Beds, Plants, Lighting, Art
  │
  ├─► 3. Semantic Segmentation (SAM 2)
  │      └─ Masks: Boundaries for furniture, walls, floor, and ceiling
  │
  ├─► 4. Perspective Depth Estimation (Depth Anything V2)
  │      └─ Map: Continuous monocular depth matrix & perspective gradient
  │
  ├─► 5. Structured Design Planning (LLM / Architectural Planner)
  │      └─ Output: Pydantic validated JSON (Style, Palette, Changes, Materials)
  │
  ├─► 6. Structure-Preserving Synthesis
  │      └─ Conditioning: Depth map + Structural Preservation Presets
  │
  └─► 7. Object-Level Inpainting (SAM 2 Mask Dilation + Context Inpaint)
         └─ Triggers: User clicks object or sends natural language chat command
```

## Structure Preservation Levels

* **Maximum (Weight: 0.85)**: Ideal for strict architectural preservation where wall shapes, window mullions, and floor boundaries must match 1:1.
* **Balanced (Weight: 0.70 - Default)**: Standard interior redesign setting. Preserves room dimensions, perspective, and architectural envelopes while rearranging and restyling furniture.
* **Creative (Weight: 0.50)**: Gives the generative model higher stylistic freedom for decorative flourishes while keeping the primary camera orientation.

## Object-Level Inpainting Mechanism

When an object is modified:
1. The target bounding box coordinates $(x_{\min}, y_{\min}, x_{\max}, y_{\max})$ or SAM mask are retrieved.
2. A safety boundary dilation (10-15px) is applied to ensure seamless edge blending.
3. Inpainting is executed only within the masked ROI (Region of Interest).
4. Unmasked pixels are 100% bitwise preserved from the parent design version.
5. A new `DesignVersion` record is persisted in the project version tree.
