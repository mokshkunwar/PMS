import requests
from flask import Flask, render_template, request, flash
from flask_restful import Resource, Api
import random, re
import string, json
import bcrypt
import datetime
import pandas as pd
import pyhibp
from pyhibp import pwnedpasswords as pw

app = Flask(__name__)
api = Api(app)

@app.route('/generate-password', methods=['POST'])
def generate_password():
    '''
    This function will generate a new password when required whose length will be in between 12 to 15 characters.
    :rtype: string
    '''
    username = request.form.get('username')
    system = request.form.get('system')
    try:
        df = pd.read_csv('password.csv')
        row = df.loc[(df['Username'] == username) & (df['System'] == system)]
        return render_template('generate_password.html',
                               message="The password is already generated for this user for {} system".format(system))
    except:
        print("NO data in Dataframe yet")
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits + "@!#$&%*@!#$&%*", k=16))
        hashed_password, salt = hash_password(generated_password)
        save_password(hashed_password, salt, username=username, system=system)
        return render_template('user_login.html',
                               message="Password generated for {} is {}".format(username, generated_password))

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

def check_pawned_password(password):
    pyhibp.set_user_agent(ua="HIBP Application/0.0.1")
    resp = pw.is_password_breached(password=password)
    return resp

@app.route('/create-password', methods=['POST'])
def create_password():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    system = request.form.get('system')
    if password != confirm_password:
        return render_template('register.html', error="Passwords Don't Match")
    criteria_satisfied = validate_password(password)
    if criteria_satisfied == False:
        error = "Password did not mach with the criteria, please try with new password"
        return render_template('register.html', error=error)
    response = check_pawned_password(password)
    if response > 10:
        error = "This password is very common, please try with new password"
        return render_template('register.html', error=error)
    else:
        try:
            df = pd.read_csv('password.csv')
            row = df.loc[(df['Username'] == username) & (df['System'] == system)]
            return render_template('register.html',
                                   error="The password is already generated for this user for {} system".format(
                                       system))
        except:
            hashed_password, salt = hash_password(password)
            save_password(hashed_password, salt, username, system)
            message = "Password saved successfully, please login with new password"
            return render_template('user_login.html', message=message)

@app.route('/renew-password', methods=['POST'])
def renew_password():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    system = request.form.get('system')
    if password != confirm_password:
        return render_template('renew.html', error="Passwords Don't Match")
    df = pd.read_csv('password.csv')
    try:
        row = df.loc[(df['Username'] == username) & (df['System'] == system)]
        index = row.index[0]
        hashed_password = df['Hashed_Password'][index]
        response = match_password(hashed_password, password)
        if response == True:
            error = "Password cannot be same as of previous one"
            return render_template('renew.html', error=error)
        criteria_satisfied = validate_password(password)
        if criteria_satisfied == False:
            error = "Password did not mach with the criteria, please try with new password"
            return render_template('renew.html', error=error)
        response = check_pawned_password(password)
        if response > 10:
            error = "This password is very common, please try with new password"
            return render_template('register.html', error=error)
        else:
            hashed_password, salt = hash_password(password)
            df = pd.read_csv('password.csv')
            index = df.loc[df['Username'] == username].index[0]
            df['Hashed_Password'][index] = hashed_password
            df['Salt'][index] = salt
            df['Date'][index] = datetime.datetime.now()
            df.to_csv('password.csv', index=False)
            message = "Password saved successfully, please login with new password"
            return render_template('user_login.html', message=message)
    except:
        error = "Invalid details"
        return render_template('renew.html', error=error)

def hash_password(password):
    # encrypt user entered password
    raw_password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(raw_password, salt)
    return hashed_password, salt

def save_password(hashed_password, salt, username, system):
    date = datetime.datetime.now()
    df2 = pd.DataFrame({'Username':[username],'System':[system], 'Salt':[salt],'Hashed_Password':[hashed_password],'Date':[date]})
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
    system = request.form.get('system')
    with open("./admins.json", 'r') as file:
        json_data = json.load(file)
        for key in json_data:
            if username == key['username'] and password == key['password']:
                return render_template('home.html')
        error = "Invalid credentials"
        return render_template('login.html', error=error)

def match_password(hashed_password, password):
    hashed_password = hashed_password.replace('b\'', '').replace('\'', '')
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    return False

@app.route('/user-login-validation', methods=['POST'])
def user_login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    system = request.form.get('system')
    df = pd.read_csv('password.csv')
    try:
        row = df.loc[(df['Username'] == username) & (df['System'] == system)]
        index = row.index[0]
        hashed_password = df['Hashed_Password'][index]
        response = match_password(hashed_password, password)
        if response == False:
            error = "Invalid credentials"
            return render_template('user_login.html', error=error)
        else:
            if (datetime.datetime.now() - pd.to_datetime(df['Date'][index])).days >= 0:
                return render_template('renew.html', error="Password is expired! Please change password",
                                       username=username)
            return render_template('user_home.html', username=username)
    except:
        error = "Invalid credentials"
        return render_template('user_login.html', error=error)

@app.route('/create_generate_password', methods=['POST'])
def create_generate_password():
    password_creation_option = request.form.get('password_creation_option')
    if password_creation_option == 'create_password':
        return render_template('register.html')
    else:
        return render_template('generate_password.html')

if __name__ == '__main__':
    app.run(debug=True)
