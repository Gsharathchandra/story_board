@echo off
echo Starting Python Service...
start cmd /k "cd python_service && .\venv\Scripts\activate && uvicorn main:app --reload"

echo Starting Node Backend...
start cmd /k "cd backend && node server.js"

echo Starting React Frontend...
start cmd /k "cd frontend && npm run dev"

echo All servers starting in new windows!
