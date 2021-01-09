# encrypt user entered password
import bcrypt
password = b"SuperSercet34"
x=bcrypt.gensalt(12)
for i in range (5):
    hashed = bcrypt.hashpw(password,x)
    print(hashed)