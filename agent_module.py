# agent_module.py
import os
import pypdf
from agents import Agent, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

API = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash"

# --- PDF extraction ---
def extract_pdf_text(file_path: str) -> str:
    text = ""
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# --- Tool for Agent ---
@function_tool
def pdf_tool(file_path: str) -> str:
    return extract_pdf_text(file_path)

# --- Create Agent ---
def get_agent():
    client = AsyncOpenAI(
        api_key=API,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)
    agent = Agent(
        model=model,
        name="StudyNotesAssistant",
        instructions="You are a Study Notes Assistant. You can either produce a summary or generate a quiz.",
        tools=[pdf_tool],
    )
    return agent
