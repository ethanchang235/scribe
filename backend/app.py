# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import ai_services  # Import new module

# --- Flask App Initialization ---
load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- Initialize Gemini Model ---
# Initialize the model once when the app starts
try:
    gemini_model = ai_services.initialize_gemini()
except (ValueError, RuntimeError) as e:
    # If the model fails to initialize, log the error and exit.
    print(e)
    exit()

# --- API Routes ---
@app.route('/api/analyze', methods=['POST'])
def analyze_transcript():
    """
    The main endpoint to analyze a meeting transcript.
    Accepts a JSON payload with a 'transcript' key.
    """
    # 1. Validate the request
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    transcript = data.get('transcript', None)

    if not transcript:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400

    # 2. Process with AI Services
    try:
        summary = ai_services.generate_summary(gemini_model, transcript)
        decisions = ai_services.extract_key_decisions(gemini_model, transcript)
        action_items = ai_services.extract_action_items(gemini_model, transcript)

        # 3. Construct the response
        response_data = {
            "summary": summary,
            "decisions": decisions,
            "action_items": action_items
        }
        return jsonify(response_data), 200

    except Exception as e:
        # General error handler for unexpected issues
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# --- Main Execution ---
if __name__ == '__main__':
    # Runs the Flask app in debug mode, which provides helpful error messages
    # and automatically reloads the server when changes are made.
    app.run(debug=True, port=5000)