"""
ProdMind AI — FastAPI Backend
Serves AI analysis endpoints to the frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List, Optional
import os
from dotenv import load_dotenv

from ai_engine import extract_pain_points, generate_followup_questions, generate_user_survey

load_dotenv()

# ── App Setup ──────────────────────────────────────
app = FastAPI(
    title="ProdMind AI API",
    description="AI-powered product management for early-stage founders",
    version="1.0.0"
)

# CORS — allow frontend (Live Server default port) and localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "null",  # file:// protocol when opening HTML directly
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request Models ────────────────────────────────

class AnalyzeRequest(BaseModel):
    responses: List[str]
    product_context: Optional[str] = ""
    user_id: Optional[str] = ""

    @validator('responses')
    def check_responses(cls, v):
        cleaned = [r.strip() for r in v if r.strip()]
        if len(cleaned) < 2:
            raise ValueError("At least 2 non-empty responses required.")
        return cleaned


class FollowupRequest(BaseModel):
    answer: str
    context: Optional[str] = ""


class SurveyRequest(BaseModel):
    product_description: str


# ── Routes ────────────────────────────────────────

@app.get("/")
async def root():
    return {"status": "ProdMind AI API is running 🚀", "version": "1.0.0"}


@app.get("/api/health")
async def health():
    return {"ok": True}


@app.post("/api/analyze")
async def analyze(req: AnalyzeRequest):
    """
    Analyzes user interview responses and returns a structured product spec.
    """
    try:
        result = extract_pain_points(req.responses, req.product_context)
        return {
            "success": True,
            "data": result,
            "meta": {
                "response_count": len(req.responses),
                "product_context": req.product_context
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")


@app.post("/api/generate-questions")
async def generate_questions(req: FollowupRequest):
    """
    Generates Mom Test style follow-up questions.
    """
    if not req.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")
    try:
        result = generate_followup_questions(req.answer, req.context)
        return {"success": True, "data": {"questions": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-survey")
async def generate_survey(req: SurveyRequest):
    """
    Creates a 5-question user interview script.
    """
    if not req.product_description.strip():
        raise HTTPException(status_code=400, detail="Product description cannot be empty.")
    try:
        result = generate_user_survey(req.product_description)
        return {"success": True, "data": {"survey": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Run locally ───────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
