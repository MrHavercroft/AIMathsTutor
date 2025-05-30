import streamlit as st
import openai
import io
from PIL import Image
import base64
import os

def extract_section(text, label):
    lines = text.split('\n')
    section_lines = [line.replace(f'[{label}]', '').strip() for line in lines if line.startswith(f'[{label}]')]
    return '\n'.join(section_lines) if section_lines else None

# ===== CONFIGURATION =====
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ===== STREAMLIT APP =====
st.title("AI Maths Tutor (Primary Friendly Final Version)")

st.write("Upload a photo of your maths work. The AI will check your answer and give you clear, colourful, easy-to-understand feedback.")

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
                {"role": "system", "content": "You are a kind and supportive maths tutor for primary school children. Always structure your feedback using these labels: [Correct]: bullet points of what they did right; [Check]: bullet points of what they should review; [Hint]: one or two short hints; [WorkedExample]: a simple worked example if needed. Keep language simple for ages 7–11 and keep the tone friendly and positive."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Please check this maths work and provide feedback."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]}
            ],
            max_tokens=1200
        )

        result = response.choices[0].message.content

        if extract_section(result, 'Correct'):
            st.success('✅ What you got right:\n' + extract_section(result, 'Correct'))
        if extract_section(result, 'Check'):
            st.warning('⚠ What to review:\n' + extract_section(result, 'Check'))
        if extract_section(result, 'Hint'):
            st.info('💡 Hint:\n' + extract_section(result, 'Hint'))
        if extract_section(result, 'WorkedExample'):
            st.error('🛠 Worked Example:\n' + extract_section(result, 'WorkedExample'))

    except Exception as e:
        st.error(f"An error occurred: {e}")