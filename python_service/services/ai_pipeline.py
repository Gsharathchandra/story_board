import os
from dotenv import load_dotenv

# Force absolute path loading for .env to bypass OneDrive sync issues
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path, override=True)

import nltk
from nltk.tokenize import sent_tokenize
import google.generativeai as genai
import requests
import base64
import asyncio

# Setup NLTK
try:
    nltk.download('punkt_tab')
    nltk.download('punkt')
except Exception as e:
    print(f"Error downloading NLTK datasets: {e}")

# Load environment keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Function to get the best model dynamically
def get_best_model():
    try:
        available_models = [m.name for m in genai.list_models()]
        # Prefer flash for speed, then pro
        for model_name in ["models/gemini-1.5-flash", "models/gemini-pro", "models/gemini-1.5-pro"]:
            if model_name in available_models:
                return genai.GenerativeModel(model_name.replace("models/", ""))
        # Fallback to the first available model that supports generation
        return genai.GenerativeModel(available_models[0].replace("models/", ""))
    except Exception:
        return genai.GenerativeModel('gemini-pro') # Hard fallback

model = get_best_model()

def refine_prompt(sentence: str, style: str) -> str:
    """Uses Gemini to turn a sentence into a concise, high-impact image prompt."""
    prompt = f"""
    Convert the following sentence into a SHORT, high-impact visual prompt for an image generator.
    
    IMPORTANT RULES:
    1. Do NOT use technical words like 'camera', 'lens', 'shutter', or 'photography'.
    2. Focus purely on the SUBJECT, the ENVIRONMENT, and the ATMOSPHERE.
    3. The style must be: '{style}'.
    4. Keep it under 40 words.
    
    Sentence: "{sentence}"
    
    Output ONLY the visual prompt.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.replace('"', '').strip()
    except Exception as e:
        print(f"Error in Gemini prompt refinement: {e}")
        # Fallback to original text + style
        return f"{sentence}. highly detailed, intricate, {style} style, amazing lighting"

import requests

def generate_image_hf(prompt: str) -> str:
    """Robust image generation with a fleet of models and 30s patience."""
    print(f"--- Prompt: {prompt[:50]} ---")
    
    # The "High Availability" Fleet
    model_fleet = [
        "stabilityai/stable-diffusion-3.5-large",
        "black-forest-labs/FLUX.1-schnell",
        "runwayml/stable-diffusion-v1-5"
    ]
    
    headers_hf = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    # 1. Try the Fleet
    for model_id in model_fleet:
        try:
            url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
            print(f"Trying AI Model: {model_id}")
            res = requests.post(url, headers=headers_hf, json={"inputs": prompt}, timeout=30) # 30s Patience
            if res.status_code == 200 and len(res.content) > 1000:
                print(f"SUCCESS: {model_id}")
                return base64.b64encode(res.content).decode("utf-8")
        except Exception as e:
            print(f"Model {model_id} failed: {e}")

    # 2. EMERGENCY Aesthetic Fallback (Picsum)
    try:
        import random
        seed = random.randint(1, 1000)
        fallback_url = f"https://picsum.photos/seed/{seed}/800/512"
        print(f"AI fleet exhausted. Using aesthetic fallback.")
        res = requests.get(fallback_url, timeout=10)
        if res.status_code == 200:
            return base64.b64encode(res.content).decode("utf-8")
    except Exception as e:
        print(f"Extreme failure: {e}")

    return None

async def process_pitch(text: str, style: str) -> list:
    """
    Main pipeline:
    1. Segments text
    2. Modifies prompts with Gemini
    3. Generates images via Hugging Face
    """
    sentences = sent_tokenize(text)
    
    # Keep only valid non-empty sentences and cap at say, 6 to avoid hitting rate limits or timeouts too hard
    valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 10][:6] 
    
    if len(valid_sentences) == 0:
        valid_sentences = [text] # Fallback if tokenizer fails to split properly
        
    panels = []
    
    for sentence in valid_sentences:
        # Step 1: Refine Prompt
        # Doing this in a thread so Async FastAPI doesn't freeze
        refined_prompt = await asyncio.to_thread(refine_prompt, sentence, style)
        print(f"Original: {sentence}\nRefined: {refined_prompt}\n")
        
        # Step 2: Generate Image
        image_base64 = await asyncio.to_thread(generate_image_hf, refined_prompt)
        
        panels.append({
            "original_text": sentence,
            "engineered_prompt": refined_prompt,
            "imageBase64": image_base64
        })
        
    return panels
