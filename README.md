You are an expert Python AI engineer. Build a Study Notes Assistant agent with these rules:

- Use OpenAgents SDK and the Gemini model.
- Gemini base URL: https://generativelanguage.googleapis.com/v1beta/openai/
- Model: gemini-2.0-flash
- API key from GEMINI_API_KEY environment variable
- Two tools:
  1) extract_pdf_text(file_path: str) -> str : reads a PDF with PyPDF and returns plain text.
- Agent instructions: "You are a Study Notes Assistant. First produce a summary, then generate a quiz."
- Output format: plain text: summary first, then quiz
- Minimal code: no extra logging or decorators
- If syntax errors occur, run @get-library-docs openai-agents
