import re

import between as between

x='''
Your Password must contain the following:
    Minimum 8 characters.
    The alphabets must be between [a-z]
    At least one alphabet should be of Upper Case [A-Z]
    At least 1 number or digit between [0-9].
    At least 1 character from [ _ or @ or $ ].
'''
print(x)

def Try_pass():
    password=input("Enter your password: ")

    while True:
        if (len(password) < 8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif not re.search("[_@$]", password):
            flag = -1
            break
        elif re.search("\s", password):
            flag = -1
            break
        else:
            flag = 0
            print("Valid Password")
            break

    if flag == -1:
        print("Not a Valid Password")

        Try_pass()

        #print("Not a Valid Password")
Try_pass()