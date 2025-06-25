from flask import  Blueprint, app, render_template, request, redirect, session, url_for
from db import get_db_connection, init_db, get_summaries
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# Initialize the database (run once at startup)
init_db()

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = get_db_connection()
        db_user = conn.execute('SELECT * FROM users WHERE username = ?', (user,)).fetchone()
        conn.close()
        if db_user:
            try:
                password_hash = db_user['password']
                user_id = db_user['id']
            except TypeError:
                # fallback if db_user is a tuple
                password_hash = db_user[2]
                user_id = db_user[0]
            if check_password_hash(password_hash, pwd):
                session['user'] = user
                session['user_id'] = user_id
                return redirect(url_for('auth.dashboard'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = get_db_connection()
        if conn.execute('SELECT * FROM users WHERE username = ?', (user,)).fetchone():
            error = 'Username already exists.'
        else:
            hashed_pwd = generate_password_hash(pwd)
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user, hashed_pwd))
            conn.commit()
            success = 'Registration successful! You can now log in.'
        conn.close()
    return render_template('signup.html', error=error, success=success)

@auth_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    summaries = get_summaries(session['user_id'])
    return render_template('dashboard.html', user=session['user'], summaries=summaries)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


