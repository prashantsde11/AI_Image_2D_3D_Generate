# AI Image Generator API

A FastAPI-based AI image generation API that creates images from text prompts using the Hugging Face Inference API. The project automatically saves generated images, adds custom watermark text, and returns the final image through a REST API.

---

## 🚀 Features

- 🎨 Generate AI images from text prompts
- ⚡ FastAPI backend for high performance
- 🖼️ Automatic image saving
- ✍️ Add custom watermark/text on generated images
- 🔑 Hugging Face API integration
- 📂 Organized output directory for generated images
- 🌐 REST API support

---

## 🛠️ Technologies Used

- Python 3.10+
- FastAPI
- Pillow (PIL)
- Requests
- Uvicorn
- Hugging Face Inference API

---

## 📁 Project Structure

```bash
project/
│
├── main.py
├── outputs/
├── requirements.txt
└── README.md
