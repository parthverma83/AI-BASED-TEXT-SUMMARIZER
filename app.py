from flask import Flask, session
from auth import auth_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return "Welcome to the AI-Based Text Summarizer!"

if __name__ == "__main__":
    app.run(debug=True)

