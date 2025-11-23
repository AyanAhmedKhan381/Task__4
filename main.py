# main.py
import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agent_module import get_agent, extract_pdf_text

# --- Load environment ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Streamlit page config ---
st.set_page_config(
    page_title="📚 Study Notes & Quiz Generator",
    page_icon="📝",
    layout="wide"
)

# --- Custom CSS styling ---
st.markdown("""
<style>
/* Buttons */
.stButton>button {
    background-color: #4a90e2;
    color: white;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border-radius: 10px;
    margin-top: 10px;
}

/* Text areas */
.stTextArea textarea {
    background-color: #ffffff;
    border-radius: 10px;
    color: black; /* Summary text black */
}

/* Quiz box styling */
.quiz-box {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    color: #111111;
    font-size: 15px;
    line-height: 1.6;
    white-space: pre-wrap;
}
</style>
""", unsafe_allow_html=True)

# --- App title ---
st.title("📚 Study Notes & Quiz Generator")
st.markdown("Upload your PDF and choose to either summarize or generate a quiz.")

# --- PDF upload ---
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    temp_dir = "temp_pdfs"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded: {uploaded_file.name}")

    # Extract text for preview
    extracted_text = extract_pdf_text(file_path)
    with st.expander("📄 Preview PDF Content"):
        st.text_area("PDF Content", extracted_text, height=300)

    # Initialize agent
    agent = get_agent()

    # --- Buttons in two columns ---
    col1, col2 = st.columns(2)

    # --- Summarize Button ---
    with col1:
        if st.button("📝 Summarize"):
            st.info("Generating summary... please wait.")

            async def run_summary():
                from agents import Runner
                return await Runner.run(
                    starting_agent=agent,
                    input=f"Summarize this text:\n\n{extracted_text}"
                )

            result = asyncio.run(run_summary())
            final_output = getattr(result, "final_output", str(result))
            # Render summary in black
            st.markdown(
                f"<div style='padding:10px; border-radius:10px; background-color:#ffffff; color:black;'>{final_output}</div>",
                unsafe_allow_html=True
            )

    # --- Quiz Button ---
    with col2:
        if st.button("❓ Generate Quiz"):
            st.info("Generating quiz... please wait.")

            async def run_quiz():
                from agents import Runner
                return await Runner.run(
                    starting_agent=agent,
                    input=f"Generate a quiz (MCQs or mixed) from this text:\n\n{extracted_text}"
                )

            result = asyncio.run(run_quiz())
            final_output = getattr(result, "final_output", str(result))
            # Clean any agent HTML tags
            final_output = final_output.replace("<div class='quiz-box'>", "").replace("</div>", "")
            st.markdown(
                f"<div class='quiz-box'>{final_output}</div>",
                unsafe_allow_html=True
            )
