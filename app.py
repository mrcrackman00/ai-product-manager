"""
AI Product Manager - Streamlit Application
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def main():
    st.set_page_config(
        page_title="AI Product Manager",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 AI Product Manager")
    st.markdown("Your AI-powered product management assistant.")

    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found. Please set it in your .env file.")
        return

    # User input
    user_input = st.text_area(
        "What do you need help with?",
        placeholder="e.g., Write a PRD for a food delivery app..."
    )

    if st.button("Generate", type="primary"):
        if user_input:
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    response = model.generate_content(user_input)
                    st.markdown("### Response")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a prompt first.")

if __name__ == "__main__":
    main()
