# AI Maths Tutor with MathPix

This Streamlit app allows primary pupils to upload a photo of their handwritten or typed maths work. It uses MathPix to extract the maths content and GPT-4o (OpenAI) to mark the work, provide hints, and show worked examples in a clear, colourful, child-friendly format.

## How to Run Locally

1. Install dependencies:
   pip install -r requirements.txt

2. Set the following environment variables or Streamlit secrets:
   - OPENAI_API_KEY = "your-openai-api-key"
   - MATHPIX_APP_ID = "your-mathpix-app-id"
   - MATHPIX_APP_KEY = "your-mathpix-app-key"

3. Run the app:
   streamlit run tutor_app.py

## Deploy on Streamlit Cloud

Upload this repository to a public GitHub repo, connect it to Streamlit Community Cloud, and set the secrets accordingly.

Enjoy giving your pupils positive, structured AI feedback!