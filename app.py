from flask import Flask, request, jsonify
import json
import google.generativeai as genai
import re

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyCDfMfEiCCGMfhDQMhPgRezoYkdv09tpXU")  # Replace with your actual API key

# Initialize Flask app
app = Flask(__name__)

# Health Check Endpoint: Verifies the API is running
@app.route("/health", methods=["GET"])
def health_check():
    try:
        return jsonify({"status": "healthy", "message": "API is running"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Extract valid JSON from Gemini API output
def extract_json(response_text):
    try:
        match = re.search(r'\[\s*{.*?}\s*]', response_text, re.DOTALL)
        return json.loads(match.group()) if match else []
    except:
        return []

# Generate SHL Assessment Recommendations based on job description
@app.route("/recommendations", methods=["POST"])
def get_assessment_recommendations():
    # Get the job description or query from the request
    data = request.get_json()
    job_desc = data.get('job_description', '')

    if not job_desc:
        return jsonify({"status": "error", "message": "Job description is required"}), 400

    try:
        # Define the prompt for Gemini API
        prompt = (
            "You are a helpful assistant. Based on the job description below, recommend up to 10 SHL assessments in JSON:\n\n"
            f"{job_desc.strip()}\n\n"
            "Response format:\n"
            '[{"Assessment Name": "...", "URL": "...", "Remote Testing Support": "Yes", '
            '"Adaptive/IRT Support": "No", "Duration": "30 mins", "Test Type": "Cognitive"}]'
        )

        # Call Gemini API to get recommendations
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        # Extract valid JSON from the response
        recommendations = extract_json(raw_output)

        if not recommendations:
            return jsonify({"status": "error", "message": "No valid recommendations found"}), 404

        # Return recommendations as JSON
        return jsonify({"status": "success", "recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Start the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
