"""
╔══════════════════════════════════════════════════════════════╗
║              AI PRODUCT MANAGER — Core Brain                ║
║                                                              ║
║  Built for early-stage founders who need to figure out       ║
║  what to build next — powered by Google Gemini AI.           ║
║                                                              ║
║  Author: AI Product Manager Team                             ║
║  Stack:  Python 3.11+ · Gemini 2.0 Flash · python-dotenv    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONSTANTS — All prompt templates in one place for easy editing
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MODEL_NAME = "gemini-2.0-flash-exp"

PAIN_POINTS_SYSTEM_PROMPT = """You are a world-class product manager who has worked at YC-backed startups.
Analyze these raw user interview responses carefully.

Output a structured product spec in this exact markdown format:

## 🔥 Top Pain Points
(List top 3 pain points. For each: pain point title, how many users mentioned it, severity score /10, and one killer quote)

## ⚡ Quick Wins — Build This Week
(2-3 features that solve the biggest pains, can be built in 1-7 days, high impact low effort)

## 🚀 Big Bets — Build This Quarter  
(2-3 larger features for next 90 days, explain WHY based on the data)

## 🚫 What NOT To Build
(1-2 things users mentioned but are distractions, explain why to skip them)

## 📊 Confidence Score
(How confident are you in this analysis? X/10 and why — be honest if sample size is small)

## 💬 Most Powerful User Quotes
(5 verbatim quotes that a founder should read before their next sprint planning)

Be direct. Be opinionated. A founder should read this and know EXACTLY what to build tomorrow morning."""

FOLLOWUP_QUESTIONS_PROMPT = """You are an expert user researcher trained in the Mom Test methodology.
A user just said: '{answer}'
Product context: '{context}'

Generate 5 follow-up questions that:
- Dig into the ROOT CAUSE of their pain (not the surface complaint)
- Are non-leading (don't suggest the answer)
- Focus on past behavior not future hypotheticals
- Would make a YC partner proud

Format:
## Follow-up Questions
1. [Question] — Why ask this: [one line reason]
2. ...

Also add:
## 🚨 Red Flags To Watch For
(2 signs this user might not be your target customer)"""

USER_SURVEY_PROMPT = """You are a YC-trained product researcher.
Create a 5-question user interview survey for this product: '{product}'

Rules:
- No yes/no questions
- Every question must reveal whether the problem is real and painful
- Questions follow Mom Test principles (talk about life, not your idea)
- Include one question that could KILL the idea if answered wrong

Output format:
## 🎯 User Interview Script
**Opening line to say:** [exactly what to say to start the interview]

**Question 1:** [question]
*Listen for:* [what a good vs bad answer sounds like]

[repeat for all 5 questions]

**Closing:** [exactly how to end the interview and what to ask for next]"""

# Separator used between individual user responses when sent to Gemini
RESPONSE_SEPARATOR = "\n\n---\n\n"

# Minimum responses needed for a meaningful analysis
MIN_RESPONSES_FOR_ANALYSIS = 2


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCTION 1: Setup Gemini
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def setup_gemini() -> Optional[genai.GenerativeModel]:
    """
    Initializes the Google Gemini AI client.

    Loads the API key from .env, configures the SDK, and returns
    a ready-to-use GenerativeModel instance.

    Returns:
        A configured Gemini model, or None if setup fails.
    """
    # Load .env from the same directory as this script
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("\n❌ GEMINI_API_KEY not found!")
        print("━" * 50)
        print("Fix this in 30 seconds:")
        print("  1. Create a file called .env in this folder")
        print("  2. Add this line:  GEMINI_API_KEY=your_key_here")
        print("  3. Get a free key: https://aistudio.google.com/apikey")
        print("━" * 50)
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL_NAME)
        print(f"✅ Gemini ({MODEL_NAME}) connected successfully!")
        return model
    except Exception as e:
        print(f"\n❌ Failed to initialize Gemini: {e}")
        print("💡 Check your API key — it might be expired or invalid.")
        return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCTION 2: Extract Pain Points from User Interviews
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_pain_points(model: genai.GenerativeModel, responses: list[str]) -> str:
    """
    Takes raw user interview responses and returns a structured
    product analysis — pain points, quick wins, big bets, and quotes.

    Why this matters: Founders waste months building the wrong thing.
    This function distills messy interview data into a clear roadmap.

    Args:
        model: A configured Gemini GenerativeModel instance.
        responses: List of raw user interview response strings.

    Returns:
        Formatted markdown string with the complete analysis.
    """
    # Guard: need enough data points for a meaningful analysis
    if len(responses) < MIN_RESPONSES_FOR_ANALYSIS:
        return (
            "⚠️ Not enough data!\n"
            f"You provided {len(responses)} response(s), but I need at least "
            f"{MIN_RESPONSES_FOR_ANALYSIS}.\n"
            "Go talk to more users — even 5 interviews can reveal gold.\n"
            "💡 Tip: Use the generate_user_survey() function to create your interview script."
        )

    # Join all responses with a clear separator so Gemini can distinguish them
    combined = RESPONSE_SEPARATOR.join(
        f"User {i+1}: \"{resp}\"" for i, resp in enumerate(responses)
    )

    # Build the full prompt: system instructions + the actual data
    full_prompt = (
        f"{PAIN_POINTS_SYSTEM_PROMPT}\n\n"
        f"Here are {len(responses)} raw user interview responses:\n\n"
        f"{combined}"
    )

    try:
        print("🧠 Analyzing responses... (this takes 10-20 seconds)")
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return (
            f"❌ Gemini API error: {e}\n\n"
            "Common fixes:\n"
            "  • Check your internet connection\n"
            "  • Verify your API key hasn't hit rate limits (free tier = 15 RPM)\n"
            "  • Try again in 60 seconds"
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCTION 3: Generate Follow-up Questions (Mom Test Style)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_followup_questions(
    model: genai.GenerativeModel,
    initial_answer: str,
    product_context: str = ""
) -> str:
    """
    Given what a user just said in an interview, generates smart
    follow-up questions using the Mom Test methodology.

    Why the Mom Test? Because users lie when you ask "would you use X?"
    These questions focus on past behavior — what they've ACTUALLY done.

    Args:
        model: A configured Gemini GenerativeModel instance.
        initial_answer: What the user just said in the interview.
        product_context: Optional context about what you're building.

    Returns:
        Formatted markdown string with follow-up questions.
    """
    # Inject the user's actual answer and context into the prompt template
    prompt = FOLLOWUP_QUESTIONS_PROMPT.format(
        answer=initial_answer,
        context=product_context if product_context else "No specific product context provided"
    )

    try:
        print("🎯 Generating follow-up questions...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return (
            f"❌ Gemini API error: {e}\n\n"
            "💡 If you're hitting rate limits, wait 60 seconds and try again."
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FUNCTION 4: Generate a User Interview Survey
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_user_survey(model: genai.GenerativeModel, product_description: str) -> str:
    """
    Creates a ready-to-use 5-question user interview script
    based on the Mom Test principles.

    Use this BEFORE you build anything — validate the problem first.

    Args:
        model: A configured Gemini GenerativeModel instance.
        product_description: What you're thinking of building.

    Returns:
        Formatted markdown interview script.
    """
    prompt = USER_SURVEY_PROMPT.format(product=product_description)

    try:
        print("📋 Creating your interview script...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return (
            f"❌ Gemini API error: {e}\n\n"
            "💡 If you're hitting rate limits, wait 60 seconds and try again."
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UTILITY: Pretty print with visual separators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def print_section(title: str, content: str) -> None:
    """Prints a section with a clear visual header."""
    print("\n")
    print("═" * 60)
    print(f"  {title}")
    print("═" * 60)
    print(content)
    print()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN — Run all 4 functions with realistic test data
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main() -> None:
    """
    Entry point — demonstrates all 4 core AI functions using
    realistic startup data about a meal planning app for busy
    Indian professionals.
    """
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          🚀 AI PRODUCT MANAGER — v1.0                   ║")
    print("║          Built for founders who ship fast               ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # ── Step 1: Connect to Gemini ──
    print("⏳ Step 1/4: Connecting to Gemini AI...")
    model = setup_gemini()
    if model is None:
        print("\n🛑 Cannot proceed without Gemini. Fix the API key and try again.")
        sys.exit(1)

    # ── Realistic test data: meal planning app for busy Indian professionals ──
    product_description = "Meal planning app for busy Indian professionals"

    sample_responses = [
        "I order Zomato every day and spend 8000 rupees a month. I want to eat healthy but I don't know what to cook and I don't have time to plan.",
        "The problem is I buy vegetables and they rot because I didn't plan what to cook. Total waste of money.",
        "I tried meal prep apps but they show American recipes. I want dal chawal and sabzi not quinoa bowls.",
        "My mom calls me every Sunday to tell me what to cook for the week but she doesn't know what's available in my fridge.",
        "I would pay good money for something that just tells me — buy THESE 10 things from BigBasket and here are 7 meals you can make.",
    ]

    # ── Step 2: Extract Pain Points ──
    print("\n⏳ Step 2/4: Analyzing user interview responses...")
    pain_points_result = extract_pain_points(model, sample_responses)
    print_section("📊 PAIN POINT ANALYSIS", pain_points_result)

    # Brief pause to respect Gemini free-tier rate limits (15 RPM)
    time.sleep(4)

    # ── Step 3: Generate Follow-up Questions ──
    print("⏳ Step 3/4: Generating follow-up questions...")
    # Use the most information-rich response to generate follow-ups
    followup_result = generate_followup_questions(
        model,
        initial_answer=sample_responses[0],  # The Zomato/₹8000 response — rich signal
        product_context=product_description
    )
    print_section("🎯 FOLLOW-UP QUESTIONS (Mom Test Style)", followup_result)

    time.sleep(4)

    # ── Step 4: Generate Interview Survey ──
    print("⏳ Step 4/4: Creating user interview script...")
    survey_result = generate_user_survey(model, product_description)
    print_section("📋 USER INTERVIEW SCRIPT", survey_result)

    # ── Done ──
    print("\n")
    print("═" * 60)
    print("  ✅ ALL DONE! Your AI Product Manager is working.")
    print("═" * 60)
    print()
    print("📌 Next steps:")
    print("   1. Replace the sample responses with YOUR user data")
    print("   2. Run: python main.py")
    print("   3. Copy the output into your sprint planning doc")
    print("   4. Build the #1 pain point this week")
    print()
    print("💡 Pro tip: Run this after every batch of 5+ user interviews")
    print("   to keep your roadmap data-driven.\n")


if __name__ == "__main__":
    main()
