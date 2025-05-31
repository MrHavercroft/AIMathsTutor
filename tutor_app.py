import streamlit as st
import openai
import io
import requests
from PIL import Image
import base64
import os

def extract_section(text, label):
    lines = text.split('\n')
    section_lines = [line.replace(f'[{label}]', '').strip() for line in lines if line.startswith(f'[{label}]')]
    return '\n'.join(section_lines) if section_lines else None

def call_mathpix_api(image_bytes):
    app_id = os.getenv('MATHPIX_APP_ID')
    app_key = os.getenv('MATHPIX_APP_KEY')
    headers = {
        'app_id': app_id,
        'app_key': app_key,
        'Content-type': 'application/json'
    }
    img_base64 = base64.b64encode(image_bytes).decode()
    data = {
        'src': f'data:image/png;base64,{img_base64}',
        'formats': ['text', 'latex_simplified'],
        'ocr': ['math', 'text']
    }
    response = requests.post('https://api.mathpix.com/v3/text', json=data, headers=headers)
    result = response.json()
    return result.get('text', '')

# ===== CONFIGURATION =====
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ===== STREAMLIT APP =====
st.title("AI Maths Tutor with MathPix")

st.write("Upload a photo of your handwritten or typed maths work. The app will extract the maths using MathPix and give clear, colourful feedback.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    st.write("Extracting maths content...")
    extracted_text = call_mathpix_api(img_bytes)
    st.write(f"**Extracted Maths:** {extracted_text}")

    if extracted_text.strip() == '':
        st.error("No maths content detected. Please try again with a clearer image.")
    else:
        st.write("Analyzing with AI...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a kind and supportive maths tutor for primary school children. Always structure your feedback using these labels: [Correct]: bullet points of what they did right; [Check]: bullet points of what they should review; [Hint]: one or two short hints; [WorkedExample]: a simple worked example if needed. Keep language simple for ages 7–11 and keep the tone friendly and positive."},
                    {"role": "user", "content": f"Please check the following maths work and provide feedback: {extracted_text}"}
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