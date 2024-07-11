from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
# Change this to a random secret key in a real application
app.secret_key = 'supersecretkey'

# Path to the JSON file
users_file = 'users.json'

# Load users from the JSON file


def load_users():
    if not os.path.exists(users_file):
        return {}
    with open(users_file, 'r') as f:
        return json.load(f)

# Save users to the JSON file


def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

# Route for the home page


@app.route('/')
def home():
    return render_template('home.html')

# Route for the signup page


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        users = load_users()
        if username in users:
            flash('Username already exists!')
            return redirect(url_for('signup'))

        users[username] = {
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        save_users(users)
        flash('Signup successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Route for the login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('partner_score_card'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route for the Partner Score Card page


@app.route('/partner_score_card')
def partner_score_card():
    if 'username' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    return render_template('partner_score_card.html')

# Route for the logout


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
