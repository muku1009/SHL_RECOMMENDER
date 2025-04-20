from flask import Flask, request, jsonify
import json
import google.generativeai as genai
import re

# ✅ Configure Gemini API
genai.configure(api_key="YOUR_API_KEY_HERE")  # Replace with your actual API key

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Home Route (optional, for browser check)
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to SHL Assessment API!",
        "routes": {
            "health": "/health",
            "recommendations": "/recommendations"
        }
    })

# ✅ Health Check Endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"}), 200

# ✅ Extract valid JSON from Gemini API response
def extract_json(response_text):
    try:
        match = re.search(r'\[\s*{.*?}\s*]', response_text, re.DOTALL)
        return json.loads(match.group()) if match else []
    except Exception as e:
        print("JSON extract error:", e)
        return []

# ✅ Recommendation Endpoint
@app.route("/recommendations", methods=["POST"])
def get_assessment_recommendations():
    try:
        data = request.get_json()
        job_desc = data.get('job_description', '').strip()

        if not job_desc:
            return jsonify({"status": "error", "message": "Job description is required"}), 400

        prompt = (
            "You are a helpful assistant. Based on the job description below, recommend up to 10 SHL assessments in JSON:\n\n"
            f"{job_desc}\n\n"
            "Response format:\n"
            '[{"Assessment Name": "...", "URL": "...", "Remote Testing Support": "Yes", '
            '"Adaptive/IRT Support": "No", "Duration": "30 mins", "Test Type": "Cognitive"}]'
        )

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        recommendations = extract_json(raw_output)

        if not recommendations:
            return jsonify({"status": "error", "message": "No valid recommendations found"}), 404

        return jsonify({
            "status": "success",
            "recommendations": recommendations,
            "raw_output": raw_output  # Optional: remove this line if not needed
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ✅ Run locally (ignored by Render/Heroku in production)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
