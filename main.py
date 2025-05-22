from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import uuid
import os
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

# Output directory for generated images
OUTPUT_DIR = "C:/Users/Dell/Documents/AI_Image_Generate_(2D-3D Image)/backend/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Hugging Face API config
API_URL = ""
HEADERS = {
    "Authorization": "Bearer "
}

# Request model for image generation
class PromptRequest(BaseModel):
    prompt: str
    is_shorts: bool = True


def add_text_to_image(image_path: str, text: str):
    base_image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(base_image)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 10), text, font=font, fill=(255, 255, 255))
    base_image.save(image_path)
    return image_path


def generate_image_and_return_path(prompt: str) -> str:
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=180)

    if response.status_code == 200 and response.headers["Content-Type"].startswith("image/"):
        ext = response.headers["Content-Type"].split("/")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        output_path = os.path.join(OUTPUT_DIR, filename)

        with open(output_path, "wb") as f:
            f.write(response.content)

        return add_text_to_image(output_path, "PRASHANT MISHRA")
    else:
        raise HTTPException(status_code=500, detail="Image generation failed")


@app.post("/generate")
def generate_image(data: PromptRequest):
    try:
        image_path = generate_image_and_return_path(data.prompt)
        ext = image_path.split(".")[-1]
        return FileResponse(image_path, media_type=f"image/{ext}", filename=os.path.basename(image_path))
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to Hugging Face timed out")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
