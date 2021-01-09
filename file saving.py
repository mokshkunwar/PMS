salt="yahhooodjbjdfsjjdbnj399i*&89jnkfek"
uname=input("Enter your Username: \n")
passwd=input("Enter your password: \n")

import csv
data = {
    "username" :
    "salt":
    "hashed password":
    "date":
}
data_list =[[passwd,uname,salt]]
with open('password.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerows(data_list)
#this will write the username and hashed pass and salt into the file which will be used to read the pass

#ser =x.split("|")[1]
#we will split the line and know what is the username and the password
#in place of x we will use a finction to find the passwordand other related data
#rint(user)

