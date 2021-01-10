import requests
from flask import Flask, render_template, request, flash
from flask_restful import Resource, Api
import random,re
import string,json
import bcrypt
import datetime
from getpass import getpass

app = Flask(__name__)
api = Api(app)

def generate_password():
    '''
    This function will generate a new password when required whose length will be in between 12 to 15 characters.
    :rtype: string
    '''
    username = input('Enter the user name')
    generated_password = ''.join(random.choices(string.ascii_letters + string.digits + "@!#$&%*@!#$&%*", k=16))
    hashed_password, salt = hash_password(generated_password)
    save_password(hashed_password, salt, username=username)
    return generated_password

def validate_password(password):
    if len(password) < 8 and re.search("\s", password)\
            and not re.search("[a-z]", password)\
            and not re.search("[A-Z]", password)\
            and not re.search("[0-9]", password)\
            and not re.search("[@!#$&%*]", password):
        flag = 1
        return flag
    else:
        flag = 0
        return flag

def create_password():
    tries =1
    while(tries<4):
        username = input('Enter the user name')
        password = input("Enter your password: ")
        flag = validate_password(password)
        if flag==1:
            print("Password did not mach with the criteria, please try with new password")
            tries = tries + 1
        else:
            print("Let's save")
            hashed_password,salt = hash_password(password)
            save_password(hashed_password,salt,username)
            return "Password saved successfully"

def hash_password(password):
    # encrypt user entered password
    raw_password=bytes(password, 'utf-8')
    salt = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(raw_password, salt)
    return hashed_password, salt

def save_password(hashed_password, salt,username):
    data = {
        "username": username,
        "salt": salt,
        "hashed password": hashed_password,
        "date": datetime.datetime.now()
    }
    with open('password.csv', 'a') as file:
        file.write("\n")
        file.write(str(data))
        file.close()

@app.route('/login', methods=['GET'])
def pms_home():
   return render_template('login.html')

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
        return render_template('login.html',  error=error)

@app.route('/create_generate_password', methods=['POST'])
def create_generate_password():
    password_creation_option = request.form.get('password_creation_option')
    if password_creation_option == 'create_password':
        return create_password()
    else:
        return generate_password()


if __name__ == '__main__':
    app.run(debug=True)