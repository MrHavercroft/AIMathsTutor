import streamlit as st
import openai
import io
from PIL import Image
import base64

# ===== CONFIGURATION =====
# Paste your OpenAI API key here
import os
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ===== STREAMLIT APP =====
st.title("AI Maths Tutor Prototype")

st.write("Upload a photo of your maths work. The AI will check your answer and give feedback.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Convert image to base64
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    # Send image to OpenAI Vision model (GPT-4o)
    st.write("Analyzing the image...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful maths tutor. You receive an image of a student's handwritten or typed maths work. Check if their answers are correct. If there are mistakes, provide hints or a worked example. Be positive and encouraging."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Please check this maths work and provide feedback."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]}
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content
        st.markdown("### AI Feedback")
        st.write(result)

    except Exception as e:
        st.error(f"An error occurred: {e}")
