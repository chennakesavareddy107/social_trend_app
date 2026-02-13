import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit Page Config
st.set_page_config(page_title="Social Media Trend Analysis", layout="wide")

st.title("📊 Social Media Trend Analysis using LLM")

st.write("Paste social media posts below to analyze trends, topics, and sentiment.")

# Input Text Area
user_input = st.text_area(
    "Enter Social Media Data (tweets, comments, hashtags, etc):",
    height=250
)

analysis_type = st.selectbox(
    "Choose Analysis Type",
    ["Trend Summary", "Topic Extraction", "Sentiment Analysis", "Full Analysis"]
)

# Function to call LLM
def analyze_trends(text, analysis):
    prompt = f"""
    You are a social media analyst.

    Perform {analysis} on the following social media data.

    Data:
    {text}

    Provide:
    - Key trends
    - Popular topics
    - Audience sentiment
    - Suggestions for content creators
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are an expert in social media trend analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


# Analyze Button
if st.button("Analyze Trends"):
    if user_input.strip() == "":
        st.warning("Please enter some social media text.")
    else:
        with st.spinner("Analyzing trends..."):
            result = analyze_trends(user_input, analysis_type)

        st.subheader("📈 Analysis Result")
        st.write(result)
