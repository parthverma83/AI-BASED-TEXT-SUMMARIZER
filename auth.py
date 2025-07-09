from flask import Blueprint, render_template, request, redirect, url_for, session
from db import register_user, authenticate_user, get_summaries

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user_ok = authenticate_user(username, password)
        if user_ok:
            session['user_id'] = user_ok
            session['username'] = username
            session['password'] = password
            return redirect(url_for('auth.dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        if register_user(username, email, password):
            success = 'Registration successful! Please log in.'
        else:
            error = "Username or email already exists."
    return render_template('signup.html', error=error, success=success)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    summaries = get_summaries(session['user_id'])
    return render_template('dashboard.html', user=session.get('username'), summaries=summaries)
