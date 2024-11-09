from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="library_management"
)
cursor = db.cursor()

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            session['username'] = username
            session['role'] = result[0]
            return redirect(url_for('main'))
        else:
            flash("Invalid Username or Password", "error")
    return render_template('login.html')

# Main Interface Route
@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html', role=session['role'])
    else:
        return redirect(url_for('login'))

# Manage Books Route
@app.route('/manage_books', methods=['GET', 'POST'])
def manage_books():
    if 'username' in session and session['role'] == 'admin':
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            isbn = request.form['isbn']
            cursor.execute("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", (title, author, isbn))
            db.commit()
            flash(f"Book '{title}' added successfully!", "success")
        cursor.execute("SELECT title, author, isbn FROM books")
        books = cursor.fetchall()
        return render_template('manage_books.html', books=books)
    else:
        return redirect(url_for('login'))

# Manage Users Route
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'username' in session and session['role'] == 'admin':
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
                db.commit()
                flash(f"User '{username}' added successfully!", "success")
            except mysql.connector.IntegrityError:
                flash("Username already exists.", "error")
        return render_template('manage_users.html')
    else:
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
