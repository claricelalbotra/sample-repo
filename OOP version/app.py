# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from db import Database
from users import Student, Officer

app = Flask(__name__, static_folder='files', static_url_path='/files')
app.secret_key = 'your_secret_key'

# Database instance
db = Database()

# --------------------------
# Landing Page
# --------------------------
@app.route('/')
def landing():
    return render_template('landing_page.html')

# --------------------------
# Register Page
# --------------------------
@app.route('/register')
def register():
    role = request.args.get('role', 'student')
    role_name = "Officer / Admin" if role == "officer" else "Student"
    return render_template('register.html', role=role, role_name=role_name)

# --------------------------
# Perform Registration
# --------------------------
@app.route('/perform_register', methods=['POST'])
def perform_register():
    try:
        role = request.form.get('role')
        user_id = request.form.get('user_id')
        surname = request.form.get('surname')
        firstname = request.form.get('firstname')
        mid = request.form.get('mi')
        full_name = f"{surname}, {firstname} {mid + '.' if mid else ''}".strip()
        contact = request.form.get('contact')

        if role == "student":
            year_level = request.form.get('year_level')
            section = request.form.get('section')
            student = Student(user_id, full_name, contact, user_id, year_level, section)
            student.save(db)
        else:  # officer
            position = request.form.get('position')
            year_level = request.form.get('year_level')
            section = request.form.get('section')
            officer = Officer(user_id, full_name, contact, user_id, position, year_level, section)
            officer.save(db)

    except Exception as e:
        print("Registration Error:", e)
        flash("Registration failed. Duplicate ID or database error.")
        return redirect(url_for("register"))

    flash("Registration successful! Please log in.")
    return redirect(url_for("login"))

# --------------------------
# Login Page
# --------------------------
@app.route('/login')
def login():
    return render_template('login.html')

# --------------------------
# Perform Login
# --------------------------
@app.route('/perform_login', methods=['POST'])
def perform_login():
    try:
        user_id = request.form.get('username')
        password = request.form.get('password')

        student = Student.login(db, user_id, password)
        if student:
            return redirect(url_for("dashboard", user_id=student.user_id, role="student"))

        officer = Officer.login(db, user_id, password)
        if officer:
            return redirect(url_for("dashboard", user_id=officer.user_id, role="officer"))

        flash("Invalid login credentials.")
        return redirect(url_for("login"))

    except Exception as e:
        print("Login Error:", e)
        flash("Login failed due to an error.")
        return redirect(url_for("login"))

# --------------------------
# Dashboard
# --------------------------
@app.route('/dashboard')
def dashboard():
    user_id = request.args.get('user_id')
    role = request.args.get('role')
    if role == "officer":
        return f"<h1>Officer Dashboard</h1><p>Welcome, Officer {user_id}!</p>"
    else:
        return f"<h1>Student Dashboard</h1><p>Welcome, Student {user_id}!</p>"

# --------------------------
# Run App
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
