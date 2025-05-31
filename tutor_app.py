import streamlit as st
import openai
import io
import requests
from PIL import Image, ImageDraw, ImageFont
import base64
import os

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
        'formats': ['text', 'json'],
        'ocr': ['math', 'text']
    }
    response = requests.post('https://api.mathpix.com/v3/text', json=data, headers=headers)
    result = response.json()
    return result

def annotate_image(image, boxes_feedback):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    for item in boxes_feedback:
        box = item['box']
        feedback = item['feedback']
        color = item['color']
        draw.rectangle(box, outline=color, width=3)
        draw.text((box[0], box[1] - 10), feedback, fill=color, font=font)
    return image

# ===== CONFIGURATION =====
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# ===== STREAMLIT APP =====
st.title("AI Maths Tutor with Annotated Feedback (Prototype)")

st.write("Upload a photo of your handwritten or typed maths work. The app will extract lines, check them, and return an annotated image just like a teacher would.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_container_width=True)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    st.write("Processing with MathPix...")
    mathpix_result = call_mathpix_api(img_bytes)
    regions = mathpix_result.get('regions', [])

    if not regions:
        st.error("No maths regions detected. Please try again with a clearer image.")
    else:
        lines = [region['text'] for region in regions]
        combined_text = '\n'.join([f"Line {i+1}: {line}" for i, line in enumerate(lines)])

        st.write("Analyzing with AI...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a supportive maths tutor. For each line, say if it's [Correct], [Check], or [Incorrect] with a short reason."},
                    {"role": "user", "content": f"Here is the student's work:\n{combined_text}\nPlease provide feedback for each line."}
                ],
                max_tokens=1500
            )
            result = response.choices[0].message.content.split('\n')

            boxes_feedback = []
            for i, region in enumerate(regions):
                box = [region['bounding_box']['left'], region['bounding_box']['top'],
                       region['bounding_box']['left'] + region['bounding_box']['width'],
                       region['bounding_box']['top'] + region['bounding_box']['height']]
                feedback_line = next((line for line in result if f"Line {i+1}:" in line), "Line {i+1}: [Check] Could not evaluate")
                if '[Correct]' in feedback_line:
                    color = 'green'
                elif '[Incorrect]' in feedback_line:
                    color = 'red'
                else:
                    color = 'yellow'
                feedback_text = feedback_line.split(':', 1)[-1].strip()
                boxes_feedback.append({'box': box, 'feedback': feedback_text, 'color': color})

            annotated_img = annotate_image(image.copy(), boxes_feedback)
            st.image(annotated_img, caption='Annotated Feedback', use_container_width=True)

            buf = io.BytesIO()
            annotated_img.save(buf, format='PNG')
            byte_im = buf.getvalue()
            st.download_button(label="Download Annotated Image", data=byte_im, file_name="annotated_feedback.png", mime="image/png")

        except Exception as e:
            st.error(f"An error occurred: {e}")