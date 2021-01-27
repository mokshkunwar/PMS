def save_to_file(df, file_name):
    df.to_csv(file_name, index=False)

def save_to_file_mode_append(df, file_name):
    df.to_csv(file_name, mode='a', index=False)

def save_to_file_without_header(df, file_name):
    df.to_csv(file_name, mode='a', header=False, index=False)

def check_pms_login_credentials(username, password):
    import json
    with open('admins.json', 'r') as file:
        json_data = json.load(file)
        for key in json_data:
            if username == key['username'] and password == key['password']:
                return True
        return False