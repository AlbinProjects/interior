@echo off
title SysInterior AI - Starting Backend and Frontend
echo ========================================================
echo Starting SysInterior AI Services...
echo ========================================================

echo Starting FastAPI Backend on http://localhost:8000...
start "SysInterior Backend (FastAPI)" cmd /k "backend\venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Next.js Frontend on http://localhost:3000...
start "SysInterior Frontend (Next.js)" cmd /k "cd frontend && npm run dev"

echo ========================================================
echo Both servers have been launched in separate windows!
echo - Frontend: http://localhost:3000
echo - Backend API Docs: http://localhost:8000/docs
echo ========================================================
pause
