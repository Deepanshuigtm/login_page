from flask import Flask, render_template, request, url_for, flash, redirect
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://2207deepanshu:Deep2207@cluster0.tk2kzqw.mongodb.net/")
db = client["User"]
users_collection = db["User"]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('signin.html')


@app.route('/takesignup')
def taketosingup():
    return render_template('signup.html')


@app.route('/takwsignin')
def taketosingin():
    return render_template('signin.html')


@app.route('/takeforgot')
def takeforgot():
    return render_template('forgot_password.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists in the database
        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            flash("User already exists.")
            return redirect(url_for('signup'))
        else:
            # Create a new user document in the database
            new_user = {
                "email": email,
                "password": password
            }
            users_collection.insert_one(new_user)
            flash("User created successfully.")
            return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')


@app.route('/signin', methods=['POST'])
def signin():
    email = request.form['email']
    password = request.form['password']

    # Query the database for the user with the provided email and password
    user = users_collection.find_one({"email": email, "password": password})

    if user:
        # Authentication successful, redirect to appropriate page
        return redirect(url_for('dashboard'))
    else:
        # Authentication failed, show error message
        flash("Invalid email or password. Please try again.")
        return redirect(url_for('signin'))


@app.route('/dashboard')
def dashboard():
    # Logic for the dashboard page
    return render_template('dashboard.html')


@app.route('/update_password', methods=['POST'])
def update_password():
    email = request.form['email']
    new_password = request.form['new_password']

    # Query the database for the user with the provided email
    user = users_collection.find_one({"email": email})

    if user:
        # Update the user's password in the database
        users_collection.update_one(
            {"email": email}, {"$set": {"password": new_password}})
        flash("Password updated successfully.")
        return redirect(url_for('dashboard'))
    else:
        flash("User not found.")
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
