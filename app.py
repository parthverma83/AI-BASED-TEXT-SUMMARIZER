from flask import Flask, session, request, jsonify, redirect, render_template, url_for
from auth import auth_bp
from summarizer import summarize_text
from db import save_summary, save_feedback

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    if session.get('user_id'):
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/summarize', methods=['POST'])
def summarize_api():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401   # Unauthorized access
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400  # Bad request
    try:
        summary = summarize_text(text)  # Generating summary using NLP model
        save_summary(session['user_id'], text, summary) # Saving to database
        return jsonify({'summary': summary})  # Return summary to client
    except Exception as e:
        return jsonify({'error': str(e)}), 500   # Internal server error

@app.route('/feedback', methods=['POST'])
def feedback_api():
    feedback = request.form.get('feedback', '').strip()
    user_id = session.get('user_id')
    if not feedback:
        return redirect(request.referrer or '/')
    save_feedback(user_id, feedback)
    # Redirect with thank you message
    return redirect(url_for('auth.dashboard', thanks=1))

if __name__ == "__main__":
    app.run(debug=True) 


