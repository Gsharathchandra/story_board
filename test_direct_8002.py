import requests
import json

def final_test():
    url = "http://localhost:8002/generate"
    data = {"text": "An apple tree in a futuristic lab", "style": "photorealistic"}
    try:
        print(f"Post to {url}...")
        r = requests.post(url, json=data, timeout=300)
        print("Status:", r.status_code)
        if r.status_code == 200:
            res = r.json()
            panels = res.get("panels", [])
            print(f"Success! Panels: {len(panels)}")
            if panels:
                print(f"Image Base64 length: {len(panels[0].get('imageBase64', ''))}")
        else:
            print("Error content:", r.text[:200])
    except Exception as e:
        print("Error during test:", e)

if __name__ == "__main__":
    final_test()
