from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='test'
    )

# Home Page
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/myprofile')
def myprofile():
    return render_template('myprofile.html')

# Dashboard (Main Webpage after login)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials. Please try again."

    return render_template('login.html')

# Register Page
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return "Username already exists. Please choose another one."

        # Insert new user
        cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
