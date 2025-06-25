from flask import Flask, session, request, jsonify
from auth import auth_bp
from summarizer import summarize_text
from db import save_summary

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return "Welcome to the AI-Based Text Summarizer!"

@app.route('/summarize', methods=['POST'])
def summarize_api():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        summary = summarize_text(text)
        save_summary(session['user_id'], text, summary)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


