# AI Maths Tutor with Annotated Feedback (Prototype)

This Streamlit app allows pupils to upload a photo of their handwritten or typed maths work. It uses MathPix to extract the maths content and bounding boxes, then checks each line with GPT-4o, and finally returns an annotated image highlighting correct, caution, or incorrect areas.

## Features

✅ Line-by-line feedback  
✅ Coloured annotations on the original image (green, yellow, red)  
✅ Downloadable annotated image

## How to Run Locally

1. Install dependencies:
   pip install -r requirements.txt

2. Set environment variables or Streamlit secrets:
   - OPENAI_API_KEY = "your-openai-api-key"
   - MATHPIX_APP_ID = "your-mathpix-app-id"
   - MATHPIX_APP_KEY = "your-mathpix-app-key"

3. Run the app:
   streamlit run tutor_app.py

## Deploy on Streamlit Cloud

Upload this repository to a public GitHub repo, connect to Streamlit Cloud, and set the secrets.

Enjoy giving your pupils visual, teacher-style feedback!