import requests
import json
import os
from pathlib import Path

# Load from .env file directly
def load_env():
    env_file = "/root/.hermes/.env"
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

load_env()

# Higgsfield MCP Configuration
HIGGSFIELD_MCP_URL = "https://mcp.higgsfield.ai/mcp"
HIGGSFIELD_API_KEY = os.environ.get("HIGGSFIELD_API_KEY", "")

def generate_image(prompt: str, width: int = 1280, height: int = 720, 
                   model: str = "higgsfield-v2", output_path: str = None):
    """
    Generate image using Higgsfield MCP API
    
    Args:
        prompt: Image generation prompt
        width: Image width (default 1280)
        height: Image height (default 720)
        model: Model to use (default higgsfield-v2)
        output_path: Where to save the image
    
    Returns:
        dict: Response with image URL or error
    """
    
    if not HIGGSFIELD_API_KEY:
        return {"error": "HIGGSFIELD_API_KEY not set"}
    
    headers = {
        "Authorization": f"Bearer {HIGGSFIELD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": model,
        "num_images": 1,
        "negative_prompt": "blurry, low quality, watermark, text, logo"
    }
    
    try:
        # Try MCP endpoint first
        response = requests.post(
            f"{HIGGSFIELD_MCP_URL}/generate",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Save image if URL provided
            if "image_url" in data and output_path:
                img_response = requests.get(data["image_url"], timeout=30)
                if img_response.status_code == 200:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(img_response.content)
                    data["saved_path"] = output_path
            
            return data
            
        elif response.status_code == 404:
            # MCP endpoint not found, try direct API
            return generate_image_direct(prompt, width, height, model, output_path)
        else:
            return {
                "error": f"Higgsfield MCP error: {response.status_code}",
                "details": response.text[:500]
            }
            
    except requests.exceptions.Timeout:
        return {"error": "Higgsfield MCP timeout - server may be down"}
    except Exception as e:
        return {"error": f"Higgsfield MCP error: {str(e)}"}

def generate_image_direct(prompt: str, width: int = 1280, height: int = 720,
                          model: str = "higgsfield-v2", output_path: str = None):
    """Fallback to direct Higgsfield API"""
    
    headers = {
        "Authorization": f"Bearer {HIGGSFIELD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "model": model,
        "num_images": 1
    }
    
    # Try different API endpoints
    endpoints = [
        "https://api.higgsfield.ai/v1/images/generations",
        "https://higgsfield.ai/api/v1/generate",
        "https://api.higgsfield.ai/v1/generate"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "image_url" in data and output_path:
                    img_response = requests.get(data["image_url"], timeout=30)
                    if img_response.status_code == 200:
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "wb") as f:
                            f.write(img_response.content)
                        data["saved_path"] = output_path
                return data
        except:
            continue
    
    return {"error": "All Higgsfield endpoints failed"}

def generate_video(prompt: str, duration: int = 5, output_path: str = None):
    """
    Generate video using Higgsfield
    
    Args:
        prompt: Video generation prompt
        duration: Video duration in seconds
        output_path: Where to save the video
    """
    
    if not HIGGSFIELD_API_KEY:
        return {"error": "HIGGSFIELD_API_KEY not set"}
    
    headers = {
        "Authorization": f"Bearer {HIGGSFIELD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "duration": duration,
        "model": "higgsfield-video-v1"
    }
    
    try:
        response = requests.post(
            "https://api.higgsfield.ai/v1/videos/generations",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if "video_url" in data and output_path:
                vid_response = requests.get(data["video_url"], timeout=60)
                if vid_response.status_code == 200:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(vid_response.content)
                    data["saved_path"] = output_path
            return data
        else:
            return {
                "error": f"Higgsfield video error: {response.status_code}",
                "details": response.text[:500]
            }
            
    except Exception as e:
        return {"error": f"Higgsfield video error: {str(e)}"}

# Test function
if __name__ == "__main__":
    print("Higgsfield MCP Client")
    print(f"API Key present: {'Yes' if HIGGSFIELD_API_KEY else 'No'}")
    print(f"Key length: {len(HIGGSFIELD_API_KEY)}")
    print(f"MCP URL: {HIGGSFIELD_MCP_URL}")
    
    # Test with a simple prompt
    result = generate_image(
        "Professional dark background with blue geometric shapes",
        width=1280,
        height=720,
        output_path="/tmp/higgsfield_test.png"
    )
    print(f"\nTest result: {json.dumps(result, indent=2)}")
