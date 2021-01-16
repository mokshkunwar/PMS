from flask import Flask, render_template, request
from flask_restful import Api
import random, re
import string, json
import datetime
import pandas as pd
from password_check import validate_password, check_pawned_password, hash_password, save_password, match_password, all_checks

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
    df = pd.read_csv(file_name)
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits + "@!#$&%*@!#$&%*", k=16))
        hashed_password, salt = hash_password(generated_password)
        save_password(hashed_password, salt, username=username, system=system)
        return render_template(user_login_html,
                               message="Password generated for {} is {}".format(username, generated_password))
    else:
        return render_template('generate_password.html',
                               message="The password is already generated for user '{}' in '{}' system".format
                               (username,system))

@app.route('/create-password', methods=['POST'])
def create_password():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    system = request.form.get('system')
    response = all_checks(password, confirm_password)
    if response:
        return render_template(register_html,
                               error=response)
    df = pd.read_csv(file_name)
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        hashed_password, salt = hash_password(password)
        save_password(hashed_password, salt, username, system)
        message = "Password saved successfully, please login with new password"
        return render_template(user_login_html, message=message)
    else:
        return render_template(register_html,
                               error="The password is already generated for user '{}' in '{}' system".format(
                                   username, system))

@app.route('/renew-password', methods=['POST'])
def renew_password():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    system = request.form.get('system')
    df = pd.read_csv(file_name)
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        error = "Invalid details"
        return render_template(renew_html, error=error)
    else:
        index = row.index[0]
        hashed_password = df['Hashed_Password'][index]
        response = match_password(hashed_password, password)
        if response == True:
            error = "Password cannot be same as of previous one"
            return render_template(renew_html, error=error)
        response = all_checks(password, confirm_password)
        if response:
            return render_template(renew_html,
                                   error=response)
        hashed_password, salt = hash_password(password)
        index = df.loc[df['Username'] == username].index[0]
        df['Hashed_Password'][index] = hashed_password
        df['Salt'][index] = salt
        df['Date'][index] = datetime.datetime.now()
        df.to_csv(file_name, index=False)
        message = "Password saved successfully, please login with new password"
        return render_template(user_login_html, message=message)

@app.route('/login', methods=['GET'])
def pms_home():
    return render_template('login.html')

@app.route('/user-login', methods=['GET'])
def user_login():
    return render_template(user_login_html)

@app.route('/login_validation', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    with open('admins.json', 'r') as file:
        json_data = json.load(file)
        for key in json_data:
            if username == key['username'] and password == key['password']:
                return render_template('home.html')
        error = invalid_credentials
        return render_template('login.html', error=error)

@app.route('/user-login-validation', methods=['POST'])
def user_login_validation():
    username = request.form.get('username')
    password = request.form.get('password')
    system = request.form.get('system')
    df = pd.read_csv(file_name)
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        error = invalid_credentials
        return render_template(user_login_html, error=error)
    else:
        index = row.index[0]
        hashed_password = df['Hashed_Password'][index]
        response = match_password(hashed_password, password)
        if response == False:
            error = invalid_credentials
            return render_template(user_login_html, error=error)
        else:
            if (datetime.datetime.now() - pd.to_datetime(df['Date'][index])).days >= 0:
                return render_template(renew_html, error="Password is expired! Please change password",
                                       username=username)
            return render_template('user_home.html', username=username)

@app.route('/create_generate_password', methods=['POST'])
def create_generate_password():
    password_creation_option = request.form.get('password_creation_option')
    if password_creation_option == 'create_password':
        return render_template(register_html)
    else:
        return render_template('generate_password.html')

if __name__ == '__main__':
    file_name = 'password.csv'
    user_login_html = 'user_login.html'
    register_html = 'register.html'
    renew_html = 'renew.html'
    invalid_credentials = "Invalid Credentials"
    app.run(debug=True)
