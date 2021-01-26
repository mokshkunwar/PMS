def save_to_file(df, file_name):
    df.to_csv(file_name, index=False)

def save_to_file_mode_append(df, file_name):
    df.to_csv(file_name, mode='a', index=False)

def save_to_file_without_header(df, file_name):
    df.to_csv(file_name, mode='a', header=False, index=False)