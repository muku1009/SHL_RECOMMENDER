import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import re

# ✅ Configure Gemini API
genai.configure(api_key="AIzaSyCDfMfEiCCGMfhDQMhPgRezoYkdv09tpXU")  # Replace with your API key

# 🔍 Extract valid JSON from Gemini output
def extract_json(response_text):
    try:
        match = re.search(r'\[\s*{.*?}\s*]', response_text, re.DOTALL)
        return json.loads(match.group()) if match else []
    except:
        return []

# 🤖 Generate SHL Assessment Recommendations
def get_assessment_recommendations(job_desc):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        "You are a helpful assistant. Based on the job description below, recommend up to 10 SHL assessments in JSON:\n\n"
        f"{job_desc.strip()}\n\n"
        "Response format:\n"
        '[{"Assessment Name": "...", "URL": "...", "Remote Testing Support": "Yes", '
        '"Adaptive/IRT Support": "No", "Duration": "30 mins", "Test Type": "Cognitive"}]'
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"🔴 Gemini API Error: {e}")
        return ""

# 🌐 Scrape job description from URL
def fetch_description_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        st.error(f"🔴 URL fetch failed: {e}")
        return ""

# 🎯 App Layout
st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("🧠 SHL Assessment Recommender")
st.markdown("Get SHL test suggestions tailored to any job description using Google Gemini AI.")

# 📥 Input Section
input_type = st.radio("Input Type:", ["📝 Paste Job Description", "🔗 Job Description URL"], horizontal=True)
job_description = ""

if input_type == "📝 Paste Job Description":
    job_description = st.text_area("📋 Paste the job description here:")
else:
    job_url = st.text_input("🔗 Enter the job description URL:")
    if job_url:
        job_description = fetch_description_from_url(job_url)

# 🚀 Trigger Gemini
if st.button("🎯 Generate SHL Recommendations") and job_description.strip():
    with st.spinner("🔍 Talking to Gemini..."):
        raw_output = get_assessment_recommendations(job_description)
        recommendations = extract_json(raw_output)

    required_keys = {"Assessment Name", "URL", "Remote Testing Support", "Adaptive/IRT Support", "Duration", "Test Type"}
    valid = [r for r in recommendations if required_keys.issubset(r)]

    if valid:
        st.success("✅ SHL Assessments Recommended:")
        st.table(pd.DataFrame(valid))
    else:
        st.error("⚠️ No valid recommendations found. Please refine the job description.")

    # 📦 Debug Section
    with st.expander("📦 Raw Gemini Output (for debugging)"):
        st.code(raw_output, language="json")

# 🧪 Example Prompt
with st.expander("🧪 Example Job Description"):
    st.markdown("""
    > I am hiring for Java developers who can also collaborate effectively with my business teams.  
    Looking for an assessment(s) that can be completed in 40 minutes.
    """)

# 📌 Footer
st.markdown("---")
st.caption("🚀 Created with ❤️ by Muskan Sangwan | Powered by Gemini AI")
