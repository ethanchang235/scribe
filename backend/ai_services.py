# backend/ai_services.py

import os
import json
import google.generativeai as genai

# --- Initialization ---
# This function sets up the Gemini model so I don't have to re-initialize it on every request
def initialize_gemini():
    """Initializes the Gemini model from the API key."""
    try:
        # Load the API key from the environment variable
        api_key = os.environ["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        return model
    except KeyError:
        # This error is critical, as the app cannot run without the API key.
        raise ValueError("ERROR: GOOGLE_API_KEY not found in environment variables.")
    except Exception as e:
        # Handle other potential initialization errors
        raise RuntimeError(f"Failed to initialize Gemini model: {e}")

# --- Core AI Functions ---

def generate_summary(model, transcript):
    """Generates a concise summary of the meeting."""
    prompt = f"""
    You are an expert meeting assistant. Your task is to provide a concise, professional executive summary
    of the following meeting transcript. Focus on the main objectives, outcomes, and conclusions.

    Transcript:
    {transcript}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during summary generation: {e}"

def extract_key_decisions(model, transcript):
    """Extracts key decisions made during the meeting."""
    prompt = f"""
    Analyze the following meeting transcript and extract the key decisions that were made.
    Present them as a clear, numbered list. If no specific decisions are found, state that.

    Transcript:
    {transcript}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during decision extraction: {e}"

def extract_action_items(model, transcript):
    """Extracts action items and returns them in a structured JSON format."""
    prompt = f"""
    You are a highly accurate task extraction bot. From the following meeting transcript, identify all
    action items. Your response MUST be a valid JSON list of objects. Each object should represent one
    action item and must have the keys 'task', 'owner', and 'deadline'. If a value for a key is not
    explicitly mentioned, use the string 'N/A'. Do not include any text, explanation, or markdown
    formatting before or after the JSON list.

    Transcript:
    {transcript}
    """
    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        # This handles cases where the model doesn't return perfect JSON
        return {"error": "Failed to parse the response as JSON.", "raw_response": response.text}
    except Exception as e:
        return {"error": f"An error occurred during action item extraction: {e}"}