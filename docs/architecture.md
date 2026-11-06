# System Architecture

SysInterior AI is structured around decoupled layers ensuring strict separation of concerns, provider interchangeability, and resilient scalability.

```
┌─────────────────────────────────────────────────────────────┐
│                 Next.js Frontend (App Router)               │
│  - Landing Page with Interactive Before/After Showcase      │
│  - Drag-and-Drop & WebRTC Camera Ingestion                  │
│  - Visual Room Analysis & YOLO Object Canvas                │
│  - Style Cards, Palette Swatches & Budget Sliders           │
│  - Real-time Multi-Stage Progress Monitor                   │
│  - Conversational AI Designer Panel & Version History       │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON / HTTP REST APIs
┌──────────────────────────────▼──────────────────────────────┐
│                    FastAPI Backend Gateway                  │
│  - CORS & File Size Validation Middleware                   │
│  - API Routers: /rooms, /designs, /chat, /budget, /projects │
│  - Static Storage Mount & URL Resolver                      │
└──────────────────────────────┬──────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ Room Analyzer │      │Design Planner │      │  Image &      │
│  Service      │      │  Service      │      │  Inpainting   │
└──────┬────────┘      └───────┬───────┘      └───────┬───────┘
       │                       │                      │
       ▼                       ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 Pluggable AI Provider Layer                 │
│  - BaseObjectDetector (YOLOv8 / Cloud Vision)               │
│  - BaseSegmenter (SAM 2 / Semantic Segmentation)            │
│  - BaseDepthEstimator (Depth Anything V2 / Perspective)     │
│  - BaseLLMProvider (OpenAI / Gemini / Architectural Engine) │
│  - BaseImageGenerator (ControlNet / Diffusion / Local Engine)│
│  - BaseStorageProvider (Local Filesystem / S3 / Supabase)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│               Persistence & Media Storage                   │
│  - PostgreSQL / SQLite Engine (SQLAlchemy ORM)              │
│  - Local / Cloud Bucket Asset Storage                       │
└─────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

1. **Presentation Layer (Frontend)**:
   - Built with Next.js 16 (App Router), TypeScript, and Tailwind CSS.
   - Framer Motion delivers micro-interactions across stage transitions, before/after comparisons, and object inpainting popovers.
2. **API Gateway & Routing Layer**:
   - Python FastAPI provides async non-blocking execution with Pydantic v2 data validation schemas.
3. **Domain Services**:
   - `RoomAnalyzerService`: Coordinates validation, object detection, segmentation overlays, and depth map computation.
   - `DesignPlannerService`: Enforces structured JSON design schemas.
   - `ImageGeneratorService`: Handles structure preservation parameters (`maximum`, `balanced`, `creative`).
   - `InpaintingService`: Computes object mask dilation and renders regional updates.
   - `BudgetEstimatorService`: Computes itemized bills of materials with currency formatting.
   - `ChatDesignService`: Multi-turn conversational design command parser.
4. **Abstract Provider Layer**:
   - Encapsulates third-party APIs and local ML weights behind Abstract Base Classes (`ABC`). Any provider can be replaced through `.env` configurations without modifying application routes.
