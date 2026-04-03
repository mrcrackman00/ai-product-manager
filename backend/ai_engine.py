"""
AI Engine — All Gemini AI functions for ProdMind AI
Uses google-generativeai with gemini-2.0-flash-exp
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ── Constants ──────────────────────────────────────
MODEL_NAME = "gemini-2.0-flash-exp"

ANALYSIS_PROMPT = """You are a world-class product manager who has worked at multiple YC-backed startups.
Analyze these raw user interview responses carefully.

Output a structured product spec in this EXACT markdown format (use these exact headers):

## 🔥 Top Pain Points
List the top 3 pain points. For each:
- **Pain Point Title** (X/Y users mentioned) — Severity: N/10
- > "One killer verbatim quote from the data"
- Root cause explanation in 1-2 sentences

## ⚡ Quick Wins — Build This Week
List 2-3 features that:
- Solve the biggest pains directly
- Can realistically be built in 1-7 days
- Have high impact, low engineering effort

For each: feature name, what it solves, why build it this week

## 🚀 Big Bets — Build This Quarter
List 2-3 larger features for the next 90 days. For each:
- Feature name and description
- WHY this is a big bet (based specifically on the data)
- Estimated user impact

## 🚫 What NOT To Build
List 1-2 things users mentioned but that are distractions. For each:
- What it is
- Why to skip it (opportunity cost, complexity, or signal weakness)

## 📊 Confidence Score
Rate your confidence: X/10
Be honest about sample size limitations.
What would increase confidence?

## 💬 Most Powerful User Quotes
List 5 verbatim quotes from the responses that a founder should read before their next sprint planning.

---
Be direct. Be opinionated. A founder should read this at 11pm and know EXACTLY what to build tomorrow morning.
"""

FOLLOWUP_PROMPT = """You are an expert user researcher trained in the Mom Test methodology.

A user just said: "{answer}"
Product context: "{context}"

Generate 5 follow-up questions that:
- Dig into the ROOT CAUSE of their pain (not the surface complaint)
- Are non-leading (never suggest the answer)
- Focus on past behavior, not future hypotheticals
- Would make Rob Fitzpatrick (author of The Mom Test) proud

Format:
## Follow-up Questions
1. [Question] — *Why ask this: [one-line reason]*
2. [Question] — *Why ask this: [one-line reason]*
3. [Question] — *Why ask this: [one-line reason]*
4. [Question] — *Why ask this: [one-line reason]*
5. [Question] — *Why ask this: [one-line reason]*

## 🚨 Red Flags To Watch For
- [Red flag 1: sign this user might not be your target customer]
- [Red flag 2: sign the problem might not be painful enough]

Be direct. Help the founder get to truth fast."""

SURVEY_PROMPT = """You are a YC-trained product researcher and Mom Test expert.

Create a 5-question user interview script for: "{product}"

Rules:
- Zero yes/no questions
- Every question must reveal whether the problem is REAL and PAINFUL
- Questions follow Mom Test principles (talk about their life, not your idea)
- One question must be a potential kill shot — if answered wrong, the idea is dead

## 🎯 User Interview Script

**Opening line to say:** [Exact words — warm, non-pitchy, curious]

**Question 1:** [Question]
*What a good answer sounds like:* [specific signal]
*What a bad answer sounds like:* [signal the problem isn't real]

[Repeat for questions 2, 3, 4, 5]

**Closing:** [Exactly how to end the interview and what to ask for as a next step]

**Kill-shot question:** [Label which question this is and why]"""


def get_model():
    """Initialize and return a Gemini model instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set. Check your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


def extract_pain_points(responses: list[str], product_context: str = "") -> dict:
    """
    Analyzes user interview responses and returns a structured product spec.
    
    Returns a dict with 'full_text' and parsed sections.
    """
    if len(responses) < 2:
        raise ValueError("Need at least 2 user responses for meaningful analysis.")

    model = get_model()
    separator = "\n\n---\n\n"
    combined = separator.join(
        f'User {i+1}: "{r}"' for i, r in enumerate(responses)
    )

    prompt = (
        f"{ANALYSIS_PROMPT}\n\n"
        f"Product context: {product_context or 'Not specified'}\n\n"
        f"Here are {len(responses)} raw user interview responses:\n\n"
        f"{combined}"
    )

    response = model.generate_content(prompt)
    full_text = response.text

    return {
        "full_text": full_text,
        "product_context": product_context,
        "response_count": len(responses),
    }


def generate_followup_questions(initial_answer: str, product_context: str = "") -> str:
    """
    Generates Mom Test follow-up questions based on what a user just said.
    """
    model = get_model()
    prompt = FOLLOWUP_PROMPT.format(
        answer=initial_answer,
        context=product_context or "Not specified"
    )
    response = model.generate_content(prompt)
    return response.text


def generate_user_survey(product_description: str) -> str:
    """
    Creates a ready-to-use 5-question user interview script.
    """
    model = get_model()
    prompt = SURVEY_PROMPT.format(product=product_description)
    response = model.generate_content(prompt)
    return response.text
