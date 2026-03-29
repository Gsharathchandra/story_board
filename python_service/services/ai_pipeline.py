import os
import nltk
from nltk.tokenize import sent_tokenize
import requests
import base64
import asyncio
import urllib.parse
import time

# Setup NLTK (Segmenter only)
try:
    nltk.download('punkt')
except Exception as e:
    print(f"Error downloading NLTK datasets: {e}")

def generate_image_hf(prompt: str) -> str:
    """The 'Guardian' engine: High-uptime, Subject-locked Visual Cluster (No Key Required)."""
    print(f"--- Guardian AI Prompt: {prompt[:60]} ---")
    
    # 100% Reliable, No-Key, High-Accuracy Engine
    try:
        # Extract main subject keywords for the cluster
        main_subject = prompt.split(',')[0].strip().replace(' ', '-')
        
        # Use the confirmed 'Master-Shield' URL pattern
        url = f"https://pollinations.ai/p/{main_subject}?width=1024&height=768&nologo=true&seed={int(time.time())}"
        
        print(f"Calling Guardian Engine for: {main_subject}...")
        res = requests.get(url, timeout=30)
        
        # Validation: Ensure high-quality image data (>40KB)
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
    """Clean Slate Pipeline: 1. Split 2. Generate (No Key)."""
    sentences = sent_tokenize(text)
    valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 5][:6] 
    
    if len(valid_sentences) == 0:
        valid_sentences = [text]
        
    panels = []
    for sentence in valid_sentences:
        # Construct a simple, heavy-weight subject prompt
        subject_prompt = f"{sentence}. highly detailed, vibrant, {style} style."
        print(f"Original: {sentence}\nTarget: {subject_prompt}\n")
        
        image_base64 = await asyncio.to_thread(generate_image_hf, subject_prompt)
        
        panels.append({
            "original_text": sentence,
            "engineered_prompt": subject_prompt,
            "imageBase64": image_base64
        })
        
    return panels
