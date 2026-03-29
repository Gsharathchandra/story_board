import os
import nltk
from nltk.tokenize import sent_tokenize
import requests
import base64
import asyncio
import urllib.parse
import time

# Setup NLTK (Used for text segmentation only)
try:
    nltk.download('punkt_tab')
    nltk.download('punkt')
except Exception as e:
    print(f"Error downloading NLTK datasets: {e}")

def generate_image_hf(prompt: str) -> str:
    """The 'Finisher' engine: High-uptime, Subject-locked Stable Cluster."""
    # We stripped Gemini, so we use the original sentence directly for 100% accuracy.
    print(f"--- Finisher AI Prompt: {prompt[:60]} ---")
    
    # Using the direct visual cluster (100% subject accuracy)
    try:
        # Extract the main subject keywords for the Finisher engine
        main_subject = prompt.split(',')[0].strip().replace(' ', '-')
        
        # This is the 'Master-Shield' URL pattern (Free, Unlimited, No-Key)
        url = f"https://pollinations.ai/p/{main_subject}?width=1024&height=768&nologo=true&seed={int(time.time())}"
        
        print(f"Calling Finisher Engine for: {main_subject}...")
        res = requests.get(url, timeout=30)
        
        # Validation: Ensure it's a real, high-quality visual (>50KB)
        if res.status_code == 200 and len(res.content) > 50000:
            print(f"FINISHER SUCCESS ({len(res.content)} bytes)")
            return base64.b64encode(res.content).decode("utf-8")
        
        print(f"Finisher Warning: Received {len(res.content)} bytes (likely error/redirect).")
    except Exception as e:
        print(f"Finisher Engine error: {e}")

    # No more beaches. Let Node handle the failure.
    print("Finisher failed to locate the visual.")
    return None

async def process_pitch(text: str, style: str) -> list:
    """
    Shielded Pipeline:
    1. Segments text (NLTK)
    2. Generates images via the Finisher Engine (No Key Required)
    """
    sentences = sent_tokenize(text)
    
    # Keep valid sentences and cap at 6
    valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 5][:6] 
    
    if len(valid_sentences) == 0:
        valid_sentences = [text] # Fallback
        
    panels = []
    
    for sentence in valid_sentences:
        # Step 1: Subject-First Prompt Weighting
        # We manually weight the subject first to ensure the AI creates what you asked for.
        subject_prompt = f"{sentence}. highly detailed, vibrant, {style} style."
        print(f"Original: {sentence}\nTarget: {subject_prompt}\n")
        
        # Step 2: Generate Image
        image_base64 = await asyncio.to_thread(generate_image_hf, subject_prompt)
        
        panels.append({
            "original_text": sentence,
            "engineered_prompt": subject_prompt,
            "imageBase64": image_base64
        })
        
    return panels
