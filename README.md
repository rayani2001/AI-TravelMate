
# AI-TravelMate — Hotel Booking Agent (Prototype)

This repository contains a minimal, simulated AI agent prototype for automatic hotel bookings.
The app is intentionally lightweight so you can run it locally or push to GitHub quickly for demo purposes.

## What this prototype does
- Lets a user enter booking preferences (city, dates, price, rating, stars)
- Filters a small sample hotels dataset
- Ranks hotels using a simple heuristic score (rating & stars vs price)
- Simulates a booking action (updates available_rooms in local CSV)

## Files
- `app.py` — Streamlit application (main demo)
- `hotels.csv` — Sample hotel dataset (small, editable)
- `requirements.txt` — Python dependencies
- `README.md` — This file

## How to run locally
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows (PowerShell)
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## How to publish on GitHub
1. Initialize a Git repository in this folder:
   ```bash
   git init
   git add .
   git commit -m "Initial AI-TravelMate prototype"
   git branch -M main
   git remote add origin https://github.com/<your-username>/AI-TravelMate.git
   git push -u origin main
   ```
2. (Optional) Use Streamlit Cloud or GitHub Pages with a small wrapper to deploy.

## Extending with an LLM
- To make the agent LLM-powered, replace the simple parsing with calls to an LLM (OpenAI, Hugging Face).
- Example (pseudocode):
  ```python
  # send user's sentence to LLM -> extract city, dates, price range, stars
  # fallback to rule-based parsing if LLM returns incomplete info
  ```
- Add steps to call Booking APIs for real reservations (most require API keys and commercial agreements).

## Notes
- This prototype simulates the booking process and does not perform real payments.
- CSV updates are local; in deployments you'd use a database or API.

---
Created for a student project / mini-project submission.
