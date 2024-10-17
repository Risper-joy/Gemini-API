from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure API key from environment variable
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to handle Question Answering
def question_answering(question):
    response = model.generate_content([question])
    return response.text

# Function to handle Translation
def translation(text, target_language="French"):
    translation_prompt = f"Translate the following text to {target_language}: {text}"
    response = model.generate_content([translation_prompt])
    return response.text

@app.route('/')
def home():
    return render_template('index2.html')  # Ensure this matches your HTML file name

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    text = data.get('text')

    # You can modify the logic here based on whether it's a question or a translation
    if text.startswith("Translate to"):
        _, _, target_language = text.split(' ', 2)
        response = translation(text.split(' ', 3)[3], target_language)
    else:
        response = question_answering(text)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
