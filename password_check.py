import pyhibp
from pyhibp import pwnedpasswords as pw
from flask import render_template
import bcrypt, re
import datetime
import pandas as pd

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

def hash_password(password):
    # encrypt user entered password
    raw_password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(raw_password, salt)
    return hashed_password, salt

def save_password(hashed_password, salt, username, system):
    file = 'password.csv'
    date = datetime.datetime.now()
    df2 = pd.DataFrame({'Username':[username],'System':[system], 'Salt':[salt],'Hashed_Password':[hashed_password],'Date':[date]})
    with open(file, 'rb') as file:
        if len(file.read()) == 0:
            df2.to_csv(file, mode='a', index=False)
        else:
            df2.to_csv(file, mode='a', header=False, index=False)

def match_password(hashed_password, password):
    hashed_password = hashed_password.replace('b\'', '').replace('\'', '')
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    return False

def all_checks(password, confirm_password):
    if password != confirm_password:
        error = "Passwords Don't Match"
        return error
    criteria_satisfied = validate_password(password)
    if criteria_satisfied == False:
        error = "Password did not mach with the criteria, please try with new password"
        return error
    response = check_pawned_password(password)
    if response > 10:
        error = "This password is very common, please try with new password"
        return error