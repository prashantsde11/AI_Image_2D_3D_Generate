from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import requests
import uuid
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# Output directory for generated images
OUTPUT_DIR = Path("C:/Users/Dell/Documents/AI_Image_Generate_(2D-3D Image)/backend/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Hugging Face API config
API_URL = ""
HEADERS = {
    "Authorization": "Bearer "
}

# Pydantic model for request
class PromptRequest(BaseModel):
    prompt: str
    is_shorts: bool = True  # Currently unused, but kept for future logic

# Load font once and reuse
def get_font(size: int = 20):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except IOError:
        return ImageFont.load_default()

def add_text_to_image(image_path: Path, text: str) -> Path:
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    font = get_font()
    draw.text((10, 10), text, font=font, fill=(255, 255, 255))
    image.save(image_path)
    return image_path

def generate_image_and_return_path(prompt: str) -> Path:
    payload = {"inputs": prompt}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=180)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Hugging Face API error: {str(e)}")

    if response.status_code == 200 and response.headers["Content-Type"].startswith("image/"):
        ext = response.headers["Content-Type"].split("/")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        image_path = OUTPUT_DIR / filename

        with image_path.open("wb") as f:
            f.write(response.content)

        return add_text_to_image(image_path, "PRASHANT MISHRA")

    raise HTTPException(status_code=500, detail="Image generation failed")

@app.post("/generate")
def generate_image(data: PromptRequest):
    image_path = generate_image_and_return_path(data.prompt)
    media_type = f"image/{image_path.suffix[1:]}"
    return FileResponse(str(image_path), media_type=media_type, filename=image_path.name)

# Dev server entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
