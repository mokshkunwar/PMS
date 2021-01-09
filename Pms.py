
import random
import string
def Pass_Generator():
    '''
    This function will generate a new password when required whose length will be in between 12 to 15 characters.
    :rtype: string
    '''

    pass_is = ''.join([random.choice(string.ascii_letters + string.digits + "@!#$&%*") for n in range(random.randint(12, 20))])
    print("The password is:",pass_is)

Pass_Generator()
