from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.ai_pipeline import process_pitch
import uvicorn

app = FastAPI(title="Pitch Visualizer AI Service")

# Clean CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    text: str
    style: str = "photorealistic"

@app.post("/generate")
async def generate_storyboard(request: GenerationRequest):
    """Integrated generation endpoint."""
    print(f"--- Received Generation Request (Style: {request.style}) ---")
    try:
        panels = await process_pitch(request.text, request.style)
        return {"success": True, "panels": panels}
    except Exception as e:
        print(f"Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
