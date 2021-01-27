from flask import Flask, render_template, request
from flask_restful import Api
import random, re
import string, json
import datetime
import pandas as pd
from password_check import hash_password, save_password, match_password, all_checks, validate_password
import configparser
from utils.helper import save_to_file, check_pms_login_credentials, read_df_from_csv, file_names
config = configparser.ConfigParser(interpolation=None)
config.read('./utils/config.ini')

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
    df = read_df_from_csv(file_names('file_name'))
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        generated_password = ''.join(random.choices(string.ascii_letters + string.digits + "@!#$&%*@!#$&%*", k=16))
        hashed_password, salt = hash_password(generated_password)
        if not username:
            return render_template('generate_password.html',
                                   message="username can be blank"),400
        save_password(hashed_password, salt, username=username, system=system)
        return render_template(file_names('user_login_html'),
                                   message="Password generated for {} is {}".format(username, generated_password)),200
    else:
        return render_template('generate_password.html',
                               message="The password is already generated for user '{}' in '{}' system".format
                               (username,system)),400

@app.route('/create-password', methods=['POST'])
def create_password():
    register_html = 'register.html'
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    system = request.form.get('system')
    response = all_checks(password, confirm_password)
    if response:
        return render_template(register_html,
                               error=response), 400
    df = read_df_from_csv(file_names('file_name'))
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        hashed_password, salt = hash_password(password)
        if not username:
            return render_template(register_html,
                                   error="username can be blank"),400
        save_password(hashed_password, salt, username, system)
        message = "Password saved successfully, please login with new password"
        return render_template(file_names('user_login_html'), message=message),200
    else:
        return render_template(register_html,
                               error="The password is already generated for user '{}' in '{}' system".format(
                                   username, system)),400

@app.route('/renew-password', methods=['POST'])
def renew_password():
    renew_html = 'renew.html'
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    system = request.form.get('system')
    df = read_df_from_csv(file_names('file_name'))
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    import pdb
    pdb.set_trace()
    if row.empty:
        error = "Invalid details"
        return render_template(renew_html, error=error),400
    else:
        index = row.index[0]
        hashed_password = df['Hashed_Password'][index]
        response = match_password(hashed_password, password)
        if response == True:
            error = "Password cannot be same as of previous one"
            return render_template(renew_html, error=error),400
        response = all_checks(password, confirm_password)
        if response:
            return render_template(renew_html,
                                   error=response),400
        hashed_password, salt = hash_password(password)
        index = df.loc[df['Username'] == username].index[0]
        df['Hashed_Password'][index] = hashed_password
        df['Salt'][index] = salt
        df['Date'][index] = datetime.datetime.now()
        save_to_file(df, file_names('file_name'))
        message = "Password saved successfully, please login with new password"
        return render_template(file_names('user_login_html'), message=message), 200

@app.route('/login', methods=['GET'])
def pms_home():
    return render_template('login.html'), 200

@app.route('/user-login', methods=['GET'])
def user_login():
    return render_template(file_names('user_login_html'))

@app.route('/login_validation', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    response = check_pms_login_credentials(username, password)
    if response == True:
        return render_template('home.html'), 200
    error = file_names('invalid_credentials')
    return render_template('login.html', error=error), 400

@app.route('/user-login-validation', methods=['POST'])
def user_login_validation():
    renew_html = 'renew.html'
    username = request.form.get('username')
    password = request.form.get('password')
    system = request.form.get('system')
    df = read_df_from_csv(file_names('file_name'))
    row = df.loc[(df['Username'] == username) & (df['System'] == system)]
    if row.empty:
        error = file_names('invalid_credentials')
        return render_template(file_names('user_login_html'), error=error), 400
    else:
        index = row.index[0]
        hashed_password = df['Hashed_Password'][index]
        response = match_password(hashed_password, password)
        if response == False:
            error = file_names('invalid_credentials')
            return render_template(file_names('user_login_html'), error=error)
        else:
            password_min_chars = str(config.get('PASSWORD', 'CHAR_COUNT'))
            required_chars = str(config.get('PASSWORD', 'REQUIRED_CHARS').split(',')[3])
            if (datetime.datetime.now() - pd.to_datetime(df['Date'][index])).days >= 30:
                return render_template(renew_html, error="Password is expired! Please change password",
                                       username=username, password_min_chars=password_min_chars, required_chars=required_chars)
            if not validate_password(password):
                return render_template(renew_html, error="Password criteria is revised! Please change password",
                                       username=username, password_min_chars=password_min_chars, required_chars=required_chars)
            return render_template('user_home.html', username=username)

@app.route('/create_generate_password', methods=['POST'])
def create_generate_password():
    register_html = 'register.html'
    password_creation_option = request.form.get('password_creation_option')
    if password_creation_option == 'create_password':
        return render_template(register_html)
    else:
        return render_template('generate_password.html')

if __name__ == '__main__':
    app.run(debug=True)
