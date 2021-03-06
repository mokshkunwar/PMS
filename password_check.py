import configparser

import pyhibp
from pyhibp import pwnedpasswords as pw
import bcrypt, re
import datetime
import pandas as pd
from utils.helper import save_to_file_mode_append, save_to_file_without_header

config = configparser.ConfigParser(interpolation=None)
config.read('./utils/config.ini')


def validate_password(password):
    password_min_chars = int(config.get('PASSWORD', 'CHAR_COUNT'))
    required_chars = config.get('PASSWORD', 'REQUIRED_CHARS').split(',')
    if len(password) < password_min_chars or re.search('\s', password):
        return False
    for each_required_chars in required_chars:
        if not re.search(each_required_chars, password):
            return False
    return True


def check_pawned_password(password):
    pyhibp.set_user_agent(ua="HIBP Application/0.0.1")
    return pw.is_password_breached(password=password)


def hash_password(password):
    # encrypt user entered password
    raw_password = bytes(password, 'utf-8')
    salt = bcrypt.gensalt(12)
    hashed_password = bcrypt.hashpw(raw_password, salt)
    return hashed_password, salt


def save_password(hashed_password, salt, username, system):
    file_name = "password.csv"
    date = datetime.datetime.now()
    df2 = pd.DataFrame({'Username':[username],'System':[system], 'Salt':[salt],'Hashed_Password':[hashed_password],'Date':[date]})
    with open(file_name, 'rb') as file:
        if len(file.read()) == 0:
            # used to put new record in empty database
            save_to_file_mode_append(df2, file_name)
        else:
            # used to append the record in db which already contain some data
            save_to_file_without_header(df2, file_name)


def match_password(hashed_password, password):
    hashed_password = hashed_password.replace('b\'', '').replace('\'', '')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def all_checks(password, confirm_password):
    error=""
    pawned_pass_limit = int(config.get('PASSWORD', 'PAWNED_PASSWORD_LIMIT'))
    if password != confirm_password:
        error = "Passwords do not match"
    if not validate_password(password):
        error = "Password did not mach with the criteria, please try with new password"
    if check_pawned_password(password) > pawned_pass_limit:
        error = "This password is very common, please try with new password"
    return error

