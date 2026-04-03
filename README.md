# 🚀 ProdMind AI

**ProdMind AI** is a premium, AI-powered product management SaaS built to help early-stage founders extract deep insights from user interviews automatically. It replaces hours of manual analysis with instant, structured product specs, follow-up questions (Mom Test style), and survey generation.

![ProdMind AI Hero](frontend/images/dashboard-preview.png)

## ✨ Features
- **🔮 Magic Interview Analysis:** Paste rough user interview notes, and the AI extracts core pain points, features, and sentiment.
- **💡 Smart Follow-ups:** Automatically generates highly effective follow-up questions based on the "Mom Test" framework to validate user needs without bias.
- **📊 Automated Survey Generation:** Instantly creates a 5-question user interview script tailored to your product description.
- **🎨 Premium Dark UI:** An ultra-smooth, high-conversion glassmorphism frontend built for founders.
- **⚡ Lightning Fast AI Engine:** Powered by a FastAPI backend integrated with state-of-the-art LLMs.

## 🛠️ Tech Stack
- **Frontend:** HTML5, Premium Native CSS (Glassmorphism, Dark UI), Vanilla JS.
- **Backend:** Python + FastAPI (High-performance API server).
- **AI Integration:** Google Gemini / LLMs.

---

## 💻 Local Setup & Installation

### 1. Backend (FastAPI)
Navigate to the root directory and install dependencies:
```bash
pip install -r requirements.txt
```
Create a `.env` file in the root or `backend` directory:
```env
GEMINI_API_KEY="your-api-key-here"
```
Run the Fast API server:
```bash
cd backend
python main.py
```
> The server will start running on `http://127.0.0.1:8000`.

### 2. Frontend
You can serve the frontend folder using any local web server (e.g., VS Code Live Server):
- Open `frontend/index.html` in your browser via Live Server (runs on `http://localhost:5500`).

---

## 🌐 API Overview
- `GET /api/health` - Server health check
- `POST /api/analyze` - Extracts pain points from user feedback
- `POST /api/generate-questions` - Generates Mom test questions
- `POST /api/generate-survey` - Creates a custom automated survey

---

## 🚀 Deployment

The project is fully structured for easy deployment on **Render** or **Railway**.
1. Create a Web Service.
2. Link this GitHub repo.
3. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

---
*Built for the future of Product Management.*
