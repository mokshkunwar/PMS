import unittest
import password_generator
from unittest.mock import patch
import pandas as pd

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
        # send login data
        response = tester.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_generator.check_pms_login_credentials", return_value=False)
    def test_pms_login_fail(self, credentials_check):
        tester = password_generator.app.test_client(self)
        # send login data
        credentials = {
            'username': 'test@example.com',
            'password': 'Test_1'}
        response = tester.post('/login_validation', data=credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid Credentials", str(response.data))

    @patch("password_generator.check_pms_login_credentials", return_value=True)
    def test_pms_login_pass(self, credentials_check):
        tester = password_generator.app.test_client(self)
        # send login data
        credentials = {
            'username': 'test@example.com',
            'password': 'Test_1234',
            'system': 'HR'}
        response = tester.post('/login_validation', data=credentials, follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_user_login_fail(self, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        credentials = {
            'username': 'Sumit',
            'password': 'Sumit@12',
            'system': 'HR'}
        response = tester.post('/user-login-validation', data=credentials, follow_redirects=True)
        self.assertTrue(response.status_code, 400)
        self.assertIn("invalid credentials", str(response.data))

    @patch("password_generator.read_df_from_csv", return_value=df_password_login_user)
    def test_user_login_pass(self, df_pass_login_user):
        tester = password_generator.app.test_client(self)
        # send login data
        credentials = {
            'username': 'Sumit',
            'password': 'Sumit@123456',
            'system': 'HR'}
        response = tester.post('/user-login-validation', data=credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_criteria_matching(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'test_user',
            'password': 'Test_1',
            'confirm_password': 'Test_1',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "Password did not mach with the criteria, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_passwords_donot_match(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'test_user',
            'password': 'Joe1@1234',
            'confirm_password': 'Joe_123',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
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
        # send login data
        data = {
            'username': 'test_user',
            'password': 'Test@123',
            'confirm_password': 'Test@123',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "This password is very common, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_fail_already_existed_user(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Growth@21',
            'confirm_password': 'Growth@21',
            'system': 'Finance'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_mode_append", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_create_password_pass(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'John',
            'password': 'Growth@21',
            'confirm_password': 'Growth@21',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_check.save_to_file_without_header", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_generate_password_fail_already_existed_user(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'system': 'Finance'}
        response = tester.post('/generate-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @patch("password_check.save_to_file_mode_append", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_generate_password_pass(self, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Jonny',
            'system': 'IT'}
        response = tester.post('/generate-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_invalid_details(self, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Test_1',
            'confirm_password': 'Test_12',
            'system': 'IT'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "Invalid details"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_citeria_not_matched(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Test_1',
            'confirm_password': 'Test_12',
            'system': 'Finance'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 400)
        res = ">Password did not mach with the criteria, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_used_previous_password(self, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Test@1423',
            'confirm_password': 'Test@1423',
            'system': 'Finance'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 400)
        res = "Password cannot be same as of previous one"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=20)
    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_fail_pawned_password(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Honey@12345',
            'confirm_password': 'Honey@12345',
            'system': 'Finance'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        res = "This password is very common, please try with new password"
        self.assertIn(res, str(response.data))

    @patch("password_check.check_pawned_password", return_value=5)
    @patch("password_generator.save_to_file", return_value=None)
    @patch("password_generator.read_df_from_csv", return_value=df_password_new_user)
    def test_renew_password_pass(self, pawned, save_file, df_pass_existing_user):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'U12se23@13',
            'confirm_password': 'U12se23@13',
            'system': 'Finance'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()