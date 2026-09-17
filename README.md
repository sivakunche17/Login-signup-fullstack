# PyAuth - Python Flask Login & Signup Web Application

A responsive, modern Flask web application converted from an existing Python console authentication project. It strictly maintains the original validation logic, features, and in-memory dictionary storage (`userdata = {}`), styled with a dark Modern Slate design inspired by the Stitch UI reference.

---

## Key Highlights & Constraints Met

- **Original Base Logic Preserved**: Direct mapping of the original console validation algorithms, dictionary structure, and feature flows.
- **In-Memory Storage**: Uses the Python dictionary `userdata = {}`. No external database (Firebase, Supabase, MongoDB, MySQL, SQLite, PostgreSQL) is required. Data resets when the server restarts.
- **Zero JavaScript**: Built exclusively using **Python, Flask, HTML, and CSS**. All interactions and transitions are handled via standard HTML forms and Flask routes.
- **Flask Session Management**: User login state is securely stored across requests using Flask signed session cookies.
- **Stitch UI Reference**: Modern dark slate aesthetic, glassmorphism cards, glowing ambient backdrops, gradient CTA buttons, and responsive desktop/mobile layouts.
- **Original File Untouched**: `login & signup.py` remains in the project directory as the original reference.

---

## Validation & Business Rules

1. **Username Validation**:
   - Must be between 8 and 12 characters in length.
   - Must contain at least 1 uppercase letter (`A-Z`).
   - Must contain at least 1 number (`0-9`).
   - Must not already exist in `userdata`.

2. **Password Validation**:
   - Must be between 6 and 8 characters in length.
   - Must contain at least 1 uppercase letter (`A-Z`).
   - Must contain at least 1 digit (`0-9`).

3. **Confirm Password**:
   - Must match the chosen password exactly.

4. **Login Attempts & Lockout**:
   - Maximum of 3 consecutive incorrect password attempts allowed per user.
   - Displays attempts remaining: `"Wrong password! Attempts left: X"`.
   - Blocks further attempts once exhausted: `"Too many incorrect attempts! Access blocked"`.

5. **Change Password**:
   - Requires confirming current password against stored password.
   - New password must meet standard password complexity rules.
   - New password and confirmation must match.

6. **Forgot Password**:
   - Verifies username exists in memory.
   - Validates new password and confirmation before updating `userdata`.

---

## Project Structure

```
login & signup-project/
├── app.py                      # Main Flask application and route handlers
├── login & signup.py           # Original console Python script (preserved)
├── requirements.txt            # Python dependencies (Flask>=3.0.0)
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── static/
│   ├── logo.svg                # Dual-snake Python/Auth vector logo
│   └── style.css               # Vanilla CSS design system (Modern Slate Auth)
└── templates/
    ├── base.html               # Base layout template with navbar and flash messages
    ├── login.html              # Login screen ("Welcome Back")
    ├── signup.html             # Sign up screen ("Create Account")
    ├── forgot_password.html    # Password recovery screen ("Reset Password")
    └── dashboard.html          # User Dashboard ("Profile & Change Password")
```

---

## Running the Application Locally

### 1. Prerequisites
- Python 3.8+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask Server
```bash
python app.py
```

### 4. Open in Browser
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## Application Routes & Flows

| Route | Method | Description |
|---|---|---|
| `/` | `GET` | Redirects to `/dashboard` if logged in, else `/login` |
| `/login` | `GET`, `POST` | User login with 3 attempts lockout |
| `/signup` | `GET`, `POST` | Account registration with validation rules |
| `/forgot-password` | `GET`, `POST` | Password recovery via username verification |
| `/dashboard` | `GET` | User profile overview (requires active session) |
| `/change-password` | `POST` | Update password for authenticated user |
| `/logout` | `GET` | End session and return to login screen |
