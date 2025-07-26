import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-1.0-pro")

# Page config
st.set_page_config(page_title="AI Blog & Essay Generator", layout="wide")
st.title("✍️ AI-Powered Blog & Essay Generator")
st.caption("Powered by Gemini 1.5 Flash • Customize, Learn & Improve Your Writing")

# Sidebar options
st.sidebar.header("Customize Content")

content_type = st.sidebar.selectbox("Select Content Type", ["Blog", "Essay"])
length = st.sidebar.selectbox("Select Length", ["Concise (500–700 words)", "Standard (1000–1500 words)", "Extended (up to 3000 words)"])
style = st.sidebar.selectbox("Select Writing Style", ["Formal", "Informal", "Conversational", "Academic"])
tone = st.sidebar.selectbox("Select Tone", ["Informative", "Persuasive", "Neutral", "Descriptive"])
summary_required = st.sidebar.checkbox("Include Summary at the End?")
keywords = st.sidebar.text_input("Keywords (comma-separated)", placeholder="Optional")

# Main input
topic = st.text_input("Enter Topic")
generate_button = st.button("📝 Generate Content")

def construct_prompt(topic, content_type, length, style, tone, summary_required, keywords):
    prompt = f"""You are an expert content writer.

Write a {content_type.lower()} on the topic: "{topic}".

Length: {length}
Style: {style}
Tone: {tone}
{"Include a brief summary at the end." if summary_required else ""}
{"Include these keywords: " + keywords if keywords else ""}

Structure content in clear paragraphs. Label each paragraph for paraphrasing. Explain why the generated content is stylistically good at the end."""
    return prompt

# Generate content
if generate_button and topic:
    with st.spinner("Generating content..."):
        prompt = construct_prompt(topic, content_type, length, style, tone, summary_required, keywords)
        response = model.generate_content(prompt)
        content = response.text

        # Split paragraphs for paraphrasing
        paragraphs = content.split("\n\n")
        for i, para in enumerate(paragraphs):
            if para.strip():
                st.markdown(f"**Paragraph {i+1}:**\n{para}")
                with st.expander("🔁 Paraphrase this paragraph"):
                    para_response = model.generate_content(f"Paraphrase this paragraph more simply or differently:\n{para}")
                    st.write(para_response.text)

        # Explanation at the end
        st.divider()
        st.subheader("📘 Why This Writing Is Stylistically Effective")
        explanation_prompt = f"Explain why this generated {content_type.lower()} is stylistically good. Highlight structure, tone, readability, and engagement based on {style} style and {tone} tone."
        explanation = model.generate_content(explanation_prompt)
        st.write(explanation.text)

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit and Gemini 1.5 Flash")
