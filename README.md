# 🎬 The Pitch Visualizer

**Transform your narratives into compelling, multi-panel visual storyboards instantly.**

The Pitch Visualizer is a hybrid AI-powered platform that takes raw sales pitches or customer success stories, segments them into logical narrative beats, and uses a triple-layered AI pipeline to generate high-quality visual storyboards.

---

## 🚀 Key Features

- **🧠 Smart Narrative Segmentation**: Automatically deconstructs long text into key storyboard moments using NLTK.
- **✨ AI Prompt Refinement**: Uses Google Gemini to transform simple sentences into highly descriptive, visually stunning art prompts.
- **🛡️ Bulletproof Image Pipeline**:
  - **Hugging Face Router**: Accesses the latest Stable Diffusion 3.5 & Flux models.
  - **Pollinations.ai**: Secondary free AI generation tier.
  - **Picsum Aesthetic Fallback**: Zero-failure system that ensures your storyboard always looks professional even if AI providers are busy.
- **📊 Real-time Carousel**: Interactive frontend to navigate through your generated storyboards.
- **🗂️ Story History**: Persistence layer using MongoDB to save and review past visual pitches.

---

## 🛠️ Tech Stack

### Frontend
- **React 18** (Vite-powered)
- **Tailwind CSS** & Modern UI/UX components
- **Axios** for API communication

### Backend
- **Node.js & Express**
- **MongoDB** (Local instance for maximum speed)
- **Mongoose** (ODM)

### AI Service (Python)
- **FastAPI** (Async performance)
- **Google Generative AI SDK** (Gemini Pro/Flash)
- **NLTK** (Natural Language Toolkit)
- **Requests & Base64** (Image processing)

---

## ⚙️ Installation & Setup

### 1. Requirements
- Node.js (v18+)
- Python (v3.10+)
- MongoDB (Running locally on port 27017)

### 2. Environment Configuration
Create a `.env` in the `python_service/` directory:
```env
GEMINI_API_KEY=your_key_here
HF_API_KEY=your_key_here
```

Create a `.env` in the `backend/` directory:
```env
PORT=5001
MONGODB_URI=mongodb://127.0.0.1:27017/pitch_visualizer
PYTHON_API_URL=http://localhost:8001
```

### 3. Running the Project
**Start the Python AI Service:**
```powershell
cd python_service
.\venv\Scripts\activate
uvicorn main:app --port 8001 --reload
```

**Start the Node Backend:**
```powershell
cd backend
node server.js
```

**Start the React Frontend:**
```powershell
cd frontend
npm run dev
```

---

## 📜 License
MIT License - Created for "The Pitch Visualizer" Challenge. ⚡
