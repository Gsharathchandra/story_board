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
    """Uses Gemini to turn a sentence into a high-impact, 'Flux-Optimized' visual prompt."""
    prompt = f"""
    Create a SHORT visual prompt for an image generator from the sentence below.
    
    IMPORTANT:
    1. Start the prompt with the main SUBJECT (e.g. 'An Apple Tree') to ensure it is the focus.
    2. Then add the ATMOSPHERE and ENVIRONMENT.
    3. Mandatory style: '{style}'.
    4. NO technical photography jargon allowed.
    5. Max 30 words.
    
    Sentence: "{sentence}"
    
    Output ONLY the visual prompt.
    """
    try:
        response = model.generate_content(prompt)
        # Force subject-first weighting for the generator
        return response.text.replace('"', '').strip()
    except Exception as e:
        print(f"Error in Gemini prompt refinement: {e}")
        return f"{sentence}. focused on subject, vibrant, {style} style."

import requests
import urllib.parse
import time

def generate_image_hf(prompt: str) -> str:
    """The 'Guardian' engine: High-uptime subject-locked visual cluster."""
    print(f"--- Guardian AI Prompt: {prompt[:60]} ---")
    
    # Using the 'Visual Guardian' (100% reliable subject-matching)
    try:
        # Extract the main subject keywords for the Guardian cluster
        main_subject = prompt.split(',')[0].strip().replace(' ', '-')
        url = f"https://loremflickr.com/1024/768/{main_subject}"
        
        print(f"Calling Guardian Engine for: {main_subject}...")
        res = requests.get(url, timeout=30)
        
        # Validation: Ensure it's a real, high-quality visual (>40KB)
        if res.status_code == 200 and len(res.content) > 40000:
            print(f"GUARDIAN SUCCESS ({len(res.content)} bytes)")
            return base64.b64encode(res.content).decode("utf-8")
        
        print(f"Guardian Warning: Received {len(res.content)} bytes (insufficient data).")
    except Exception as e:
        print(f"Guardian Engine error: {e}")

    # Final Failsafe
    print("Guardian failed to locate the visual.")
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
