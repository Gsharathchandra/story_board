import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

try:
    with open('result.txt', 'w') as f:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content("Hello")
            f.write("Gemini Response: " + res.text + "\n")
        except Exception as e:
            f.write("Gemini Error: " + str(e) + "\n")
        
        try:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            response = requests.post(API_URL, headers=headers, json={"inputs": "An apple tree"}, timeout=60)
            f.write("HF Status: " + str(response.status_code) + "\n")
            f.write("HF Response text: " + response.text[:200] + "\n")
        except Exception as e:
            f.write("HF Error: " + str(e) + "\n")
except Exception as e:
    pass

