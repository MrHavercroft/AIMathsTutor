# AI Maths Tutor (Primary Friendly)

This is a Streamlit app that allows primary pupils to upload a photo of their maths work. The app uses GPT-4o (OpenAI) to mark the work, provide hints, and show worked examples — all in a clear, child-friendly format.

## How to Run Locally

1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   streamlit run tutor_app.py

## Deploy on Streamlit Cloud

Upload this repository to a public GitHub repo, connect it to Streamlit Community Cloud, and set the secret:
OPENAI_API_KEY = "your-openai-api-key"

Enjoy giving your pupils positive, structured AI feedback!