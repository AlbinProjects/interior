# SysInterior AI — Structure-Preserving AI Interior Design & Room Redesign

A complete, production-grade AI-powered interior design and room redesign web application.

Unlike generic text-to-image generators that hallucinate random perspectives, SysInterior AI employs a **Structure-Preserving AI Vision Pipeline** that strictly preserves original camera viewpoints, walls, windows, doors, floor boundaries, and overall architectural geometry while intelligently restyling furniture, color palettes, lighting temperature, and materials.

---

## Key Features

1. **Camera & Geometry Preservation**: Enforces strict structural preservation using Depth Anything V2 depth estimation and SAM 2 semantic masks.
2. **AI Room Analyzer**: Detects room objects (sofas, tables, lamps, plants, artwork) via YOLOv8, analyzes horizon angles, and constructs a structured Room Graph JSON.
3. **Structured LLM Design Planner**: Leverages structured JSON schemas to plan style harmonization, color palettes, materials, and lighting without uncontrolled hallucination.
4. **Interactive Object-Level Inpaint Studio**: Click any detected room object to replace, recolor, remove, or restyle it with mask-guided inpainting.
5. **Conversational AI Designer Panel**: Refine designs naturally (e.g., *"Make the sofa beige"*, *"Add indoor plants"*, *"Make lighting warmer"*) while branching version histories.
6. **High-Definition Before/After Comparison**: Draggable split-slider, side-by-side view, zoom/pan controls, and fullscreen presentation.
7. **Itemized Furniture & Material Budgeting**: Automatically calculates Bills of Materials with price range estimates in INR/USD and category breakdowns.
8. **Pluggable AI & Storage Abstraction Layer**: Zero-lock-in architecture supporting local models, OpenAI, Gemini, Replicate ControlNet, AWS S3, and Supabase.

---

## Technology Stack

* **Frontend**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Framer Motion, Lucide React.
* **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic v2, Pillow, OpenCV, NumPy.
* **Database**: PostgreSQL (Production) / SQLite (Zero-config local development).
* **AI & Computer Vision**: YOLOv8, Segment Anything (SAM 2), Depth Anything V2, Structure-Preserving Synthesis & ControlNet Inpainting.
* **DevOps**: Docker, Docker Compose.

---

## Application Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point & CORS
│   │   ├── config.py                # Environment settings
│   │   ├── api/                     # REST API routers (rooms, designs, chat, budget, projects, auth)
│   │   ├── models/                  # SQLAlchemy models
│   │   ├── schemas/                 # Pydantic schemas
│   │   ├── services/                # RoomAnalyzer, DesignPlanner, BudgetEstimator, Inpainting
│   │   ├── ai/                      # Pluggable BaseDetector, BaseSegmenter, BaseDepth, BaseLLM, BaseGen
│   │   └── database/                # Database engine & session maker
│   ├── tests/                       # Automated pytest suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js App Router pages
│   │   │   ├── page.tsx             # Landing page with Before/After showcase
│   │   │   ├── design/              # Room image upload & live camera capture
│   │   │   ├── analyze/             # Spatial analysis & YOLO overlay viewer
│   │   │   ├── configure/           # Visual style cards, palette swatches & budget
│   │   │   ├── generate/            # 8-stage progress tracker
│   │   │   ├── result/[id]/         # Redesign showcase & Before/After slider
│   │   │   ├── editor/[id]/         # Object-level inpainting studio
│   │   │   ├── projects/            # Saved projects gallery & version details
│   │   │   └── settings/            # AI provider switching & API keys
│   │   ├── components/              # BeforeAfterSlider, ObjectOverlayCanvas, StyleSelector, etc.
│   │   ├── services/                # API client
│   │   └── types/                   # TypeScript interfaces
│   └── package.json
├── docker/                          # Dockerfiles for frontend & backend
├── docs/                            # In-depth architectural & AI documentation
└── docker-compose.yml
```

---

## Quickstart & Local Development

### 1. Backend Setup

```bash
# Navigate to backend and create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run automated tests
python -m pytest tests/test_api.py -v

# Start FastAPI server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
* Backend API documentation will be live at: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install packages
npm install

# Start Next.js development server
npm run dev
```
* Web application will be live at: `http://localhost:3000`

---

## Running with Docker Compose

To launch the full stack (PostgreSQL, FastAPI Backend, Next.js Frontend) in containers:

```bash
docker-compose up --build
```

---

## User Workflow

```
1. Landing Page → "Start Designing"
2. Upload / Camera → Upload room photo or capture via device camera
3. Spatial Analysis → View YOLO furniture detections, SAM 2 masks, and depth map
4. Configuration → Select Style (e.g. Modern, Japandi, Scandinavian), Palette, Budget & Preservation level
5. Generation → Watch real-time 8-stage progress tracking
6. Result View → Drag the Before/After slider, explore budget breakdown & shopping list
7. Inpaint & Chat → Click objects to modify or converse with the AI designer ("Make the sofa beige")
8. Version History → Navigate across iterations and export high-res deliverables
```

---

## Documentation Links

* [Architecture Guide](docs/architecture.md)
* [AI Pipeline & Structure Preservation](docs/ai-pipeline.md)
* [REST API Reference](docs/api.md)
* [Installation & Production Setup](docs/setup.md)
