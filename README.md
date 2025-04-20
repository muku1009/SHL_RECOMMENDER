📝 Solution Approach Document – SHL Assessment Recommendation System
By: Muskan Sangwan

✅ Objective 
To build and deploy an AI-powered recommendation system that suggests SHL assessments based on a provided job description. This includes:

- A **Flask-based REST API** for backend processing.
- A **Streamlit web app** for user interaction.
- Integration with **Google Gemini** for intelligent, structured recommendations.

🛠️ Tools & Libraries Used

| Tool/Library         | Purpose                                               |
|----------------------|-------------------------------------------------------|
| **Flask**            | REST API backend for processing and routing           |
| **Streamlit**        | Frontend UI for user interaction                      |
| **Google Generative AI (Gemini)** | SHL recommendation generation using LLM         |
| **Requests**         | Fetching job descriptions from URLs                   |
| **BeautifulSoup4**   | HTML content parsing for job pages                    |
| **Pandas**           | Displaying tabular data in the frontend               |
| **Regex (re)**       | JSON extraction from Gemini output                    |
| **Gunicorn**         | Production-ready WSGI server                          |


⚙️ Implementation Overview

🔹1. Streamlit Frontend
- **Hosted At**:  
  🔗 [https://muskansangwan2003.streamlit.app/](https://muskansangwan2003.streamlit.app/)
  
- **Features**:
  - Select between **pasting job description** or **fetching from URL**.
  - Display AI-generated SHL assessment suggestions in tabular form.
  - Expandable section for **raw Gemini response** (for debugging).
  - Example prompt included for quick testing.

🔹 2. Flask REST API
- **Base URL**:  
  🔗 [https://shl-recommender-dha7.onrender.com](https://shl-recommender-dha7.onrender.com)

- **Endpoints**:
  - **Health Check**  
    🔍 [https://shl-recommender-dha7.onrender.com/health](https://shl-recommender-dha7.onrender.com/health)  
    *(Returns API status as JSON)*

  - **Get Recommendations (POST)**  
    🔁 `https://shl-recommender-dha7.onrender.com/recommendations`  
    - Use **Postman** to test.
    - Set method to **POST**.
    - Choose `Body > raw > JSON`, then paste your job description in this format:

    ```json
    {
      "job_description": "Looking for a data analyst familiar with Python, SQL, and basic statistics."
    }
    ```

    - Click **Send** to receive structured SHL assessment recommendations.


📂 GitHub Repository

All source code for the Flask API, Streamlit app, and Gemini prompt engineering is available on GitHub:  
🔗 [https://github.com/muku1009/SHL_RECOMMENDER](https://github.com/muku1009/SHL_RECOMMENDER)


💡 Gemini Prompt Strategy

A structured prompt is sent to Gemini, requesting a JSON array of up to 10 SHL assessments with fields like:

- `"Assessment Name"`, `"URL"`, `"Remote Testing Support"`, `"Adaptive/IRT Support"`, `"Duration"`, `"Test Type"`

Regex is used to cleanly extract the response in valid JSON format for further processing.


🌐 Deployment

- **API deployed using Render** and **Gunicorn** for production.
- **Frontend hosted on Streamlit Cloud** for simplicity and accessibility.
- Supports real-time inference with robust error handling.


✅ Conclusion

This solution leverages Gemini AI, Flask, and Streamlit to deliver accurate, real-time SHL assessment suggestions from any job description.
It is accessible via a user-friendly web interface and a robust API, offering both interactivity and integration potential.

