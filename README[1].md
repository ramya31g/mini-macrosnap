# Mini MacroSnap

A small Streamlit + Gemini AI meal analyzer based on the MacroSnap workshop guide.

## Features
- Meal text analysis
- Meal photo analysis
- Estimated calories
- Estimated protein, carbs and fat
- Chat history
- Clear chat

## Run locally

Open the project folder in VS Code.

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install packages:

pip install -r requirements.txt

Create:

.streamlit/secrets.toml

Put your Gemini key inside:

GEMINI_API_KEY = "your-key-here"

Run:

streamlit run app.py
