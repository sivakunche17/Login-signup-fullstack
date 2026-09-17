import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pyauth-in-memory-session-secret-key-98234')

# ==============================================================================
# In-Memory Storage (Preserving original Python logic & dictionary structure)
# Data resets when Flask restarts.
# ==============================================================================
userdata = {}
login_attempts = {}  # Tracks remaining attempts per username (default: 3)


# ==============================================================================
# Validation Helpers (Directly adapted from login & signup.py console rules)
# ==============================================================================
def validate_username(user_name):
    """
    Original rules:
    - 8 <= len(user_name) <= 12
    - At least 1 Upper case
    - At least 1 Number
    """
    upper = False
    number = False

    for characters in user_name:
        if characters.isupper():
            upper = True
        if characters.isdigit():
            number = True

    if 8 <= len(user_name) <= 12 and upper and number:
        return True, None
    else:
        return False, "Username must have: Atleast 8-12 Characters, Atleast 1 Upper case, Atleast 1 Number"


def validate_password(user_password):
    """
    Original rules:
    - 6 <= len(user_password) <= 8
    - At least 1 Upper case
    - At least 1 digit/Number
    """
    upper = False
    number = False

    for characters in user_password:
        if characters.isupper():
            upper = True
        if characters.isdigit():
            number = True

    if 6 <= len(user_password) <= 8 and upper and number:
        return True, None
    else:
        return False, "Password must have: Atleast 6-8 Characters, Atleast 1 Upper case, Atleast 1 digit"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'] not in userdata:
            session.pop('user', None)
            flash("Please login to access the dashboard", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# Routes
# ==============================================================================

@app.route('/')
def index():
    if 'user' in session and session['user'] in userdata:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get('username', '').strip()
        user_password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Check if user already exists
        if user_name in userdata:
            flash("User name already Exists!", "error")
            return render_template('signup.html', username=user_name)

        # Validate username
        is_valid_user, user_err = validate_username(user_name)
        if not is_valid_user:
            flash(user_err, "error")
            return render_template('signup.html', username=user_name)

        # Validate password
        is_valid_pass, pass_err = validate_password(user_password)
        if not is_valid_pass:
            flash(pass_err, "error")
            return render_template('signup.html', username=user_name)

        # Validate password confirmation
        if user_password != confirm_password:
            flash("Password don't match", "error")
            return render_template('signup.html', username=user_name)

        # Save to memory
        userdata[user_name] = user_password
        login_attempts[user_name] = 3  # Reset/initialize attempts
        flash("Signup Successful! You can now login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form.get('username', '').strip()
        login_password = request.form.get('password', '')

        if user_name in userdata:
            attempts_left = login_attempts.get(user_name, 3)

            # Check if user is locked out
            if attempts_left <= 0:
                flash("Too many incorrect attempts! Access blocked", "error")
                return render_template('login.html', username=user_name)

            if login_password == userdata[user_name]:
                # Successful login
                login_attempts[user_name] = 3  # Reset attempts on success
                session['user'] = user_name
                flash(f"Login Successfully! Welcome: {user_name}", "success")
                return redirect(url_for('dashboard'))
            else:
                attempts_left -= 1
                login_attempts[user_name] = attempts_left

                if attempts_left == 0:
                    flash("Wrong password! Too many incorrect attempts! Access blocked", "error")
                else:
                    flash(f"Wrong password! Attempts left: {attempts_left}", "error")

                return render_template('login.html', username=user_name)
        else:
            flash("No user found! Please Signup first", "error")
            return render_template('login.html', username=user_name)

    return render_template('login.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user_name = request.form.get('username', '').strip()
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if user_name in userdata:
            # Validate new password
            is_valid_pass, pass_err = validate_password(new_password)
            if not is_valid_pass:
                flash(pass_err, "error")
                return render_template('forgot_password.html', username=user_name)

            # Validate confirm password
            if new_password != confirm_password:
                flash("password dont match!", "error")
                return render_template('forgot_password.html', username=user_name)

            # Update password in userdata dictionary
            userdata[user_name] = new_password
            login_attempts[user_name] = 3  # Reset attempts on password reset
            flash("Password changed Successfully", "success")
            return redirect(url_for('login'))
        else:
            flash("No user found! try again", "error")
            return render_template('forgot_password.html', username=user_name)

    return render_template('forgot_password.html')


@app.route('/dashboard')
@login_required
def dashboard():
    user_name = session['user']
    return render_template('dashboard.html', username=user_name)


@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    user_name = session['user']
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')

    if current_password == userdata[user_name]:
        # Validate new password
        is_valid_pass, pass_err = validate_password(new_password)
        if not is_valid_pass:
            flash("Password must have 6-8 characters, Atleast 1 Upper case, Atleast 1 digit", "error")
            return redirect(url_for('dashboard'))

        # Validate confirm password
        if new_password != confirm_password:
            flash("Password not matched! try again", "error")
            return redirect(url_for('dashboard'))

        # Update in userdata dictionary
        userdata[user_name] = new_password
        flash("Password changed Successfully", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("Wrong Current password! Try again", "error")
        return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out Successfully", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
