import unittest
import password_generator
from unittest.mock import patch
import pandas as pd
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read('./utils/config.ini')
username1 = config.get('TEST-CREDENTIALS', 'USERNAME1')
password1 = config.get('TEST-CREDENTIALS', 'PASSWORD1')
username2 = config.get('TEST-CREDENTIALS', 'USERNAME2')
password2 = config.get('TEST-CREDENTIALS', 'PASSWORD2')
username3 = config.get('TEST-CREDENTIALS', 'USERNAME3')
password3 = config.get('TEST-CREDENTIALS', 'PASSWORD3')
username4 = config.get('TEST-CREDENTIALS', 'USERNAME4')
password4 = config.get('TEST-CREDENTIALS', 'PASSWORD4')
username5 = config.get('TEST-CREDENTIALS', 'USERNAME5')
password5 = config.get('TEST-CREDENTIALS', 'PASSWORD5')
username6 = config.get('TEST-CREDENTIALS', 'USERNAME6')
password6 = config.get('TEST-CREDENTIALS', 'PASSWORD6')
password6_wrong = config.get('TEST-CREDENTIALS', 'PASSWORD6_WRONG')
username7 = config.get('TEST-CREDENTIALS', 'USERNAME7')
password7 = config.get('TEST-CREDENTIALS', 'PASSWORD7')
username8 = config.get('TEST-CREDENTIALS', 'USERNAME8')
password8 = config.get('TEST-CREDENTIALS', 'PASSWORD8')
username9 = config.get('TEST-CREDENTIALS', 'USERNAME9')
password9 = config.get('TEST-CREDENTIALS', 'PASSWORD9')
username10 = config.get('TEST-CREDENTIALS', 'USERNAME10')
username11 = config.get('TEST-CREDENTIALS', 'USERNAME11')
password11 = config.get('TEST-CREDENTIALS', 'PASSWORD11')
password11_wrong = config.get('TEST-CREDENTIALS', 'PASSWORD11_WRONG')
username12 = config.get('TEST-CREDENTIALS', 'USERNAME12')
password12 = config.get('TEST-CREDENTIALS', 'PASSWORD12')
username13 = config.get('TEST-CREDENTIALS', 'USERNAME13')
password13 = config.get('TEST-CREDENTIALS', 'PASSWORD13')
username14 = config.get('TEST-CREDENTIALS', 'USERNAME14')
password14 = config.get('TEST-CREDENTIALS', 'PASSWORD14')

class MyTestCase(unittest.TestCase):
    data_password_login_user = [['Sumit', 'HR', 'b\'$2b$12$BMRUlgdo.xDi52MuFxBSzO\'',
                                    'b\'$2b$12$BMRUlgdo.xDi52MuFxBSzOu6F3L6FuA1IhyBQ2t09Q6L6.RGAWCYi\'',
                                    '2021-01-27 00:40:12.155977']]
    df_password_login_user = pd.DataFrame(data_password_login_user,
                                             columns=['Username', 'System', 'Salt', 'Hashed_Password', 'Date'])

    data_password_new_user = [['Honey', 'Finance', 'b\'$2b$12$gc7ot/rXwH8nBO7nceltv.\'',
                                    'b\'$2b$12$gc7ot/rXwH8nBO7nceltv.kt2vMYP501rKwD/BOHReagEOVk8CNGu\'',
                                    '2021-01-27 00:40:12.155977']]
    df_password_new_user = pd.DataFrame(data_password_new_user,
                                             columns=['Username', 'System', 'Salt', 'Hashed_Password', 'Date'])

    def setUp(self):
        password_generator.app.config['TESTING'] = True
        password_generator.app.config['DEBUG'] = False

    def test_pms_home(self):
        tester = password_generator.app.test_client(self)
        response = tester.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_generator.check_pms_login_credentials", return_value=False)
    def test_pms_login_fail(self, credentials_check):
        tester = password_generator.app.test_client(self)
        credentials = {
            'username': username1,
            'password': password1}
        response = tester.post('/login_validation', data=credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid Credentials", str(response.data))

    @patch("password_generator.check_pms_login_credentials", return_value=True)
    def test_pms_login_pass(self, credentials_check):
        tester = password_generator.app.test_client(self)
        credentials = {
            'username': username2,
            'password': password2,
            'system': 'HR'}
        response = tester.post('/login_validation', data=credentials, follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_user_login_fail(self, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        credentials = {
            'username': username3,
            'password': password3,
            'system': 'HR'}
        response = tester.post('/user-login-validation', data=credentials, follow_redirects=True)
        self.assertTrue(response.status_code, 400)
        self.assertIn("Invalid Credentials", str(response.data))

    @patch("password_generator.read_df_from_csv", return_value=df_password_login_user)
    def test_user_login_pass(self, df_pass_login_user):
        tester = password_generator.app.test_client(self)
        credentials = {
            'username': username4,
            'password': password4,
            'system': 'HR'}
        response = tester.post('/user-login-validation', data=credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_criteria_matching(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username5,
            'password': password5,
            'confirm_password': password5,
            'system': 'IT'}
        response = tester.post('/'+create_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "Password did not mach with the criteria, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_passwords_donot_match(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username6,
            'password': password6,
            'confirm_password': password6_wrong,
            'system': 'IT'}
        response = tester.post('/' + create_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "Passwords do not match"
        self.assertIn(res, str(response.data))

    '''
    when the used password has been used 11 times before, mocking pawned API call
    '''

    @patch("password_check.check_pawned_password", return_value=20)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_check_pawned_password(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username7,
            'password': password7,
            'confirm_password': password7,
            'system': 'IT'}
        response = tester.post('/' + create_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "This password is very common, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_already_existed_user(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username8,
            'password': password8,
            'confirm_password': password8,
            'system': 'Finance'}
        response = tester.post('/' + create_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_mode_append", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_pass(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username9,
            'password': password9,
            'confirm_password': password9,
            'system': 'IT'}
        response = tester.post('/' + create_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_generate_password_fail_already_existed_user(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username11,
            'system': 'Finance'}
        response = tester.post('/generate-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @patch("password_check.save_to_file_mode_append", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_generate_password_pass(self, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username10,
            'system': 'IT'}
        response = tester.post('/generate-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_invalid_details(self, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username11,
            'password': password11,
            'confirm_password': password11_wrong,
            'system': 'IT'}
        response = tester.post('/' + renew_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "Invalid details"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_citeria_not_matched(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username11,
            'password': password11,
            'confirm_password': password11_wrong,
            'system': 'Finance'}
        response = tester.post('/' + renew_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = ">Password did not mach with the criteria, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_used_previous_password(self, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username12,
            'password': password12,
            'confirm_password': password12,
            'system': 'Finance'}
        response = tester.post('/' + renew_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "Password cannot be same as of previous one"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=20)
    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_pawned_password(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username13,
            'password': password13,
            'confirm_password': password13,
            'system': 'Finance'}
        response = tester.post('/' + renew_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "This password is very common, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_pass(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        data = {
            'username': username14,
            'password': password14,
            'confirm_password': password14,
            'system': 'Finance'}
        response = tester.post('/'+renew_password, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    renew_password = 'renew-password'
    create_password ='create-password'
    unittest.main()