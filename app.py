from flask import Flask, render_template, request
from googletrans import Translator, LANGUAGES

app = Flask(__name__)

# Supported languages (simplified version)
languages = {
    'kn': 'Kannada',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'ml': 'Malayalam',
    'te': 'Telugu',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'or': 'Odia'
}

# Home route to display the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html', languages=languages)

# Route to handle the translation page
@app.route('/translate_page')
def translate_page():
    # Get the selected language direction from the URL
    lang = request.args.get('lang')
    
    if lang is None:
        return "Error: No language direction provided", 400

    # Pass the selected language direction to the translation page
    return render_template('translation.html', lang=lang)

# Route to handle the translation logic
@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    lang = request.form['lang']
    
    if not text:
        return "Error: No text to translate", 400

    # Initialize the translator
    translator = Translator()

    # Translate the text based on the selected language direction
    if 'en-to-' in lang:
        target_language = lang.split('-to-')[1]
        translated_text = translator.translate(text, src='en', dest=target_language).text
    elif '-to-en' in lang:
        source_language = lang.split('-to-en')[0]
        translated_text = translator.translate(text, src=source_language, dest='en').text
    else:
        return "Error: Invalid language direction", 400

    return render_template('translation.html', lang=lang, input_text=text, translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
