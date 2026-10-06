# FitBuddy AI – Personal Gym Assistant

A clean, responsive, local-first AI-style fitness chatbot for a college project. It combines a conversational fitness assistant with workout planning, nutrition education, and progress tracking.

## Features
- Modern responsive fitness dashboard
- FitBuddy conversational assistant
- Built-in local fitness knowledge engine (works without an API key)
- Optional path to connect a real LLM later
- Personalized starter workout plan
- Workout completion and streak tracking
- Weight, target weight, water and weekly-goal tracking
- Nutrition guidance cards
- Mobile-friendly layout
- Local JSON persistence

## Requirements
- Python 3.9+
- VS Code (recommended)

## Run on Windows
1. Extract the ZIP.
2. Open the folder in VS Code.
3. Open Terminal.
4. Create a virtual environment:
   `python -m venv .venv`
5. Activate it:
   `.venv\\Scripts\\activate`
6. Install dependencies:
   `pip install -r requirements.txt`
7. Start the app:
   `python app.py`
8. Open **http://127.0.0.1:5000** in your browser.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000.

## Project structure
```
FitBuddy_AI/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── progress.json
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

## Important note
The included chatbot is a deterministic local fitness assistant so the project runs without an external API. It is intended for general fitness education and is not a medical diagnosis or treatment system. For a production version, connect a trusted LLM API and add authentication, a proper database, validation, and safety filters.

## Suggested project title
**FitBuddy AI: An Intelligent Conversational Fitness and Workout Assistant**
