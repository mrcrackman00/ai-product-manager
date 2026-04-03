# 🚀 AI Product Manager

An AI-powered product management assistant built with **Streamlit** and **Google Gemini**.

## Setup

1. **Clone the repo** and navigate into the project:
   ```bash
   cd ai-product-manager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your `GEMINI_API_KEY`.

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   Or:
   ```bash
   python main.py
   ```

## Project Structure

```
ai-product-manager/
├── app.py              # Streamlit application
├── main.py             # Entry point
├── .env.example        # Example environment variables
├── .gitignore          # Git ignore rules
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Tech Stack

- **Streamlit** — UI framework
- **Google Generative AI (Gemini)** — LLM backend
- **python-dotenv** — Environment variable management
