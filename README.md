# Scribe

An AI-powered web app that uses Gemini 2.5 Flash through the Google Gemini API to summarize meeting transcripts and identify action items.

---

## Tech Stack

*   **AI:** Google Gemini 2.5 Flash
*   **Backend:** Python, Flask
*   **Frontend:** React, TypeScript, Tailwind CSS
*   **Database:** PostgreSQL
*   **Infrastructure:** Docker, GCP (Cloud Run)

---

## Current Status (Part 1)

This project is currently in Part 1. The core logic for interacting with the Gemini API is complete and functional. The script can:
- [x] Generate an executive summary from a transcript.
- [x] Extract key decisions as a list.
- [x] Extract action items in a structured JSON format.

---

## How to Run (Part 1)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/meeting-scribe-ai.git
    cd meeting-scribe-ai
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** in the root directory and add your API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

4.  **Run the script:**
    ```bash
    python main.py
    ```
