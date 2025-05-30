import streamlit as st
import openai
import io
from PIL import Image
import base64
import os

def extract_section(text, symbol):
    lines = text.split('\n')
    section = '\n'.join([line for line in lines if line.startswith(symbol)])
    return section if section else None

# ===== CONFIGURATION =====
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ===== STREAMLIT APP =====
st.title("AI Maths Tutor (Primary Friendly)")

st.write("Upload a photo of your maths work. The AI will check your answer and give you clear, easy-to-understand feedback.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    st.write("Analyzing the image...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a kind and supportive maths tutor for primary school children. When giving feedback, always use short, clear sentences. Break your response into: ✅ What the child got right, ⚠ What they should check or fix, 💡 A hint or tip to help them improve, 🛠 A worked example if they need it. Use simple language appropriate for ages 7–11. Keep the tone positive, encouraging, and friendly."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Please check this maths work and provide feedback."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]}
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content

        if extract_section(result, '✅'):
            st.success(extract_section(result, '✅'))
        if extract_section(result, '⚠'):
            st.warning(extract_section(result, '⚠'))
        if extract_section(result, '💡'):
            st.info(extract_section(result, '💡'))
        if extract_section(result, '🛠'):
            st.error(extract_section(result, '🛠'))

    except Exception as e:
        st.error(f"An error occurred: {e}")