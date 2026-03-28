import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ai_pipeline import process_pitch
import uvicorn

app = FastAPI(title="The Pitch Visualizer AI Service")

# Allow CORS for the Node.js backend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PitchRequest(BaseModel):
    text: str
    style: str = "photorealistic"

@app.post("/generate")
async def generate_storyboard(request: PitchRequest):
    try:
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text is too short.")
            
        panels = await process_pitch(request.text, request.style)
        return {"panels": panels}
    except Exception as e:
        print(f"Error generating storyboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
