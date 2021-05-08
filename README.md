# Password-management-system(PMS)
A password management system is used to keep track of all of the passwords required by the applications. Since the last two decades, the IT industry has seen a significant shift in the development of applications for various purposes. These applications have their usage in a spectrum ranging from healthcare, e-commerce, social media websites, mailing systems, manufacturing, retail, etc. The onus was on  the IT professionals to build utility software as fast as possible.
### Steps to use the PMS

- ##### Check python version `$ python --version`
- ##### Check pip version `$ pip --version`
- ##### Clone the project `$ git clone https://github.com/mokshkunwar/PMS.git`
- ##### Install python virtual environment `pip install pipenv`
- #####  Activate Python environment `pipenv shell` 
- #####  Install required packages  `pip install -r requirements.txt` 

### Environments variables

###**Development** - All the main functionalities of the system
###**Test** - Testing the functions 

#### Run the system under development environment

	$env:FLASK_ENV = development
	flask run
	
###Access the apis using **POSTMAN** to test the functionality

	#http://127.0.0.1:5000/user_registration
	#http://127.0.0.1:5000/login
	#http://127.0.0.1:5000/legacy_app_list
	#http://127.0.0.1:5000/add_new_legacy_app
	#http://127.0.0.1:5000/view_all_users
	#http://127.0.0.1:5000/add_pwd_app
	#http://127.0.0.1:5000/get_all_pwds
	#http://127.0.0.1:5000/get_pwd_criteria
	#http://127.0.0.1:5000/update_pwd_criteria
	
### Note: For all the **POST** requests it is compulsary to pass the current valid JWT token in the header fields as 'x-access-tokens'

	
	$env:FLASK_ENV = test
	python -m unittest
	
### User modules
**ADMIN** and **USER**.  Some tasks such as creation of legacy application, view users passwords, update complexity can only be performed by **admin** users only.

##### Once the user successfully logs in, a JWT token is generated. To access the other functions of the system, we must use a valid current session token. This has to be added in the "header" field. 

`x-access-tokens :  "your token goes here"`

### Admin  Tasks
##### Login to system using master password - Admin
`http://127.0.0.1:5000/login`
`{
	"email": "admin@gmail.com",
	"password": "a23eSP$rt5"
}`

##### Create new legacy application - Admin[Token Required]
`http://127.0.0.1:5000/add_new_legacy_app`
 `{
    "app_name":"Finance",
    "url":"www.fin.com",
    "description":"Finance"
}`
##### View all registered User list - Admin[Token Required]
`http://127.0.0.1:5000/view_all_users`

##### Update Password complexity - Admin[Token Required]
`http://127.0.0.1:5000/update_pwd_criteria`

##Pass the updated complexity criteria in the body
 
------------

### Normal User Tasks

##### Signin  to system 
 `http://127.0.0.1:5000/user_registration`
 `{
	"username":"mapi",
	"password":"123%vRstF@",
	"email":"map@gmail.com"
}`


##### Login to system using master password
`http://127.0.0.1:5000/login`
`{
	"email": "sam@gmail.com",
	"password": "Ab@#123sJK7"
}`

##### View the password complexity [Token Not Required] 
`http://127.0.0.1:5000/get_pwd_criteria`

##### View System Legacy application list[Token Required]
 `http://127.0.0.1:5000/app_list`

##### Add New Legacy app Password [Token Required] - Main task of the PMS
`http://127.0.0.1:5000/add_pwd_app`
 `{
	"password":"123%vRstF@",
	"app_id":2,
}`

####Note: app_id is the sequence of the created applications

##### Get all passwords for current logged user [Token Required]
`http://127.0.0.1:5000/pwd_list`


