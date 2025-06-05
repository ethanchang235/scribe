import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()

# Configure Gemini API with key from the environment
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("ERROR: GOOGLE_API_KEY not found in environment variables.")
    print("Please create a .env file and add your API key.")
    exit()

# --- Sample Data ---
# Hardcoded meeting transcript to test the logic
MEETING_TRANSCRIPT = """
Sarah (Project Manager): Good morning, everyone. Thanks for joining. The main agenda today is to finalize the plan for the new 'Project Apollo' login page redesign. Mark, how are the backend preparations going?

Mark (Lead Developer): Morning. The authentication service is solid. I've set up the basic endpoint, but I need the final specs for the data we'll be collecting on the sign-up form. Are we adding Google OAuth?

Chloe (UX/UI Designer): On the design front, I have two mockups. Mockup A is a traditional two-column layout. Mockup B is a cleaner, single-column layout which my research suggests is better for mobile conversions.

Sarah (Project Manager): Great points. Mobile-first is key for this project. Let's go with Mockup B, the single-column layout. That's our first decision. Chloe, can you create the final high-fidelity assets for that one? Let's have those ready for review by this Wednesday EOD.

Chloe (UX/UI Designer): Will do. I'll have them ready.

Sarah (Project Manager): Perfect. Mark, regarding the sign-up form, let's keep it simple for now. Just email, password, and full name. We will table the Google OAuth discussion for a future release to avoid scope creep. So, your action item is to finalize the authentication endpoint to accept just those three fields. Can you get that done by Friday?

Mark (Lead Developer): Yes, that's no problem at all. I'll have the API documentation updated by Friday as well.

Sarah (Project Manager): Fantastic. That's all for today then. Great progress, team!
"""

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
        return {"error": "Failed to parse the response as JSON. The model may have returned an invalid format.", "raw_response": response.text}
    except Exception as e:
        return {"error": f"An error occurred during action item extraction: {e}"}

# --- Main Execution Block ---
if __name__ == "__main__":
    print("Initializing Meeting Scribe AI...")
    
    # Select the model
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    print("\nProcessing transcript with Gemini API...")
    print("-" * 30)

    # 1. Generate summary
    print("\n1. Generating Executive Summary...")
    summary = generate_summary(model, MEETING_TRANSCRIPT)
    print(summary)
    print("-" * 30)

    # 2. Extract key decisions
    print("\n2. Extracting Key Decisions...")
    decisions = extract_key_decisions(model, MEETING_TRANSCRIPT)
    print(decisions)
    print("-" * 30)

    # 3. Extract action items
    print("\n3. Extracting Action Items (in JSON)...")
    action_items = extract_action_items(model, MEETING_TRANSCRIPT)
    
    # Print the JSON output
    if "error" in action_items:
        print(f"Error: {action_items['error']}")
        print(f"Raw Response from Model:\n{action_items.get('raw_response', 'N/A')}")
    else:
        print(json.dumps(action_items, indent=2))
    
    print("-" * 30)
    print("\nProcessing complete.")
