# Installation & Setup Guide

## System Requirements

* **Python**: 3.10, 3.11, or 3.12+
* **Node.js**: 18.x, 20.x, or 22.x+
* **Package Managers**: `pip` and `npm`
* **Docker & Docker Compose** (Optional for containerized deployment)

---

## Local Setup

### 1. Clone & Environment Configuration

```bash
cp .env.example .env
```

### 2. Backend Installation

```bash
cd backend
python -m venv venv
# On Linux / macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
python -m pytest tests/test_api.py -v
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Frontend Installation

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## Production Deployment with Docker

```bash
docker-compose up --build -d
```
Services started:
* **Frontend**: `http://localhost:3000`
* **Backend API**: `http://localhost:8000`
* **PostgreSQL**: `localhost:5432`
