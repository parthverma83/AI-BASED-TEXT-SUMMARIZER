from flask import Flask, request, jsonify, render_template
from summarizer import summarize_text

app = Flask(_name_)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        summary = summarize_text(text)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)
