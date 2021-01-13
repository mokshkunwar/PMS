import requests
from flask import Flask, render_template, request, flash
from flask_restful import Resource, Api
import random, re
import string, json
import bcrypt
import datetime
import pandas as pd

app = Flask(__name__)
api = Api(app)

@app.route('/generate-password', methods=['POST'])
def generate_password():
    '''
    This function will generate a new password when required whose length will be in between 12 to 15 characters.
    :rtype: string
    '''
    username = input('Enter the user name')
    generated_password = ''.join(random.choices(string.ascii_letters + string.digits + "@!#$&%*@!#$&%*", k=16))
    hashed_password, salt = hash_password(generated_password)
    save_password(hashed_password, salt, username=username)
    return render_template('user_login.html')

def validate_password(password):
    if len(password) < 8 or re.search("\s", password) \
            or not re.search("[a-z]", password) \
            or not re.search("[A-Z]", password) \
            or not re.search("[0-9]", password) \
            or not re.search("[@!#$&%*]", password):
        criteria_satisfied = False
    else:
        criteria_satisfied = True
    return criteria_satisfied

@app.route('/create-password', methods=['POST'])
def create_password(renew_password=None):
   # tries = 1
   # while tries < 4:
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        return render_template('register.html', error="Passwords Don't Match")
    criteria_satisfied = validate_password(password)
    if criteria_satisfied == False:
        error = "Password did not mach with the criteria, please try with new password"
        return render_template('register.html', error=error)
    else:
        hashed_password, salt = hash_password(password)
        if renew_password:
            return hashed_password, salt
        save_password(hashed_password, salt, username)
    message = "Password saved successfully, please login with new password"
    return render_template('user_login.html', message=message)

@app.route('/renew-password', methods=['POST'])
def renew_password():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        return render_template('renew.html', error="Passwords Don't Match")
    # TODO: the new password should not be the same as of last one
    criteria_satisfied = validate_password(password)
    if criteria_satisfied == False:
        error = "Password did not mach with the criteria, please try with new password"
        return render_template('renew.html', error=error)
    else:
        hashed_password, salt = hash_password(password)
        df = pd.read_csv('password.csv')
        index = df.loc[df['Username'] == username].index[0]
        df['hashed_password'][index] = hashed_password
        df['Salt'][index] = salt
        df['Date'][index] = datetime.datetime.now()
        df.to_csv('password.csv', index=False)
        message = "Password saved successfully, please login with new password"
    return render_template('user_login.html', message=message)


def hash_password(password):
    # encrypt user entered password
    raw_password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(raw_password, salt)
    return hashed_password, salt

def save_password(hashed_password, salt, username):
    date = datetime.datetime.now()
    df2 = pd.DataFrame({'Username':[username],'Salt':[salt],'hashed_password':[hashed_password],'Date':[date]})
    with open('password.csv', 'rb') as file:
        if len(file.read()) == 0:
            df2.to_csv('password.csv', mode='a', index=False)
        else:
            df2.to_csv('password.csv', mode='a', header=False, index=False)

@app.route('/login', methods=['GET'])
def pms_home():
    return render_template('login.html')

@app.route('/user-login', methods=['GET'])
def user_login():
    return render_template('user_login.html')

@app.route('/login_validation', methods=['POST'])
def login():
    error = None
    username = request.form.get('username')
    password = request.form.get('password')
    with open("admins.json", 'r') as file:
        json_data = json.load(file)
        for key in json_data:
            if username == key['username'] and password == key['password']:
                return render_template('home.html')
        error = "Invalid credentials"
        return render_template('login.html', error=error)

@app.route('/user-login-validation', methods=['POST'])
def user_login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    df = pd.read_csv('password.csv')
    row = df.loc[df['Username'] == username]
    if row.empty:
        error = "Invalid credentials"
        return render_template('user_login.html', error=error)
    else:
        index = row.index[0]
        # Todo: The password is yet to be verified
        # hashed_password = df['hashed_password'][row.index]
        # bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        # check if the password is expired or not, time = 30 minutes
        if (datetime.datetime.now()-pd.to_datetime(df['Date'][index])).days >= 30:
            return render_template('renew.html', error="Password is expired! Please change password", username=username)
        return render_template('user_home.html', username=username)

@app.route('/create_generate_password', methods=['POST'])
def create_generate_password():
    password_creation_option = request.form.get('password_creation_option')
    if password_creation_option == 'create_password':
        return render_template('register.html')
    else:
        return render_template('generate_password.html')

if __name__ == '__main__':
    app.run(debug=True)
