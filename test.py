import unittest
import password_generator
from flask import Flask

class MyTestCase(unittest.TestCase):

    def setUp(self):
        password_generator.app.config['TESTING'] = True
        password_generator.app.config['DEBUG'] = False


    def test_pms_home(self):
        tester = password_generator.app.test_client(self)
        # send login data
        response = tester.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_pms_login_pass(self):
        tester = password_generator.app.test_client(self)
        # send login data
        credentials = {
            'username': 'test@example.com',
            'password': 'Test_1234'}
        response = tester.post('/login_validation', data=credentials, follow_redirects=True)
        self.assertTrue(response.status_code, 200)

    def test_pms_login_fail(self):
        tester = password_generator.app.test_client(self)
        # send login data
        credentials = {
            'username': 'test@example.com',
            'password': 'Test_1'}
        response = tester.post('/login_validation', data=credentials, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        import pdb
        pdb.set_trace()
        self.assertIn("Invalid Credentials", response.data)

    def test_create_password_fail(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'test_user',
            'password': 'Test_1',
            'confirm_password': 'Test_12',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_create_password_fail_criteria_matching(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'test_user',
            'password': 'Test',
            'confirm_password': 'Test',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_create_password_fail_common_password(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'test_user',
            'password': 'Test@123',
            'confirm_password': 'Test@123',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_create_password_pass(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'testing_user_new',
            'password': 'Growth@21',
            'confirm_password': 'Growth@21',
            'system': 'IT'}
        response = tester.post('/create-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_generate_password_fail(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'system': 'Finance'}
        response = tester.post('/generate-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_generate_password_pass(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'testing_user_new_again',
            'system': 'IT'}
        response = tester.post('/generate-password', data=data, follow_redirects=True)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def test_renew_password_fail(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Test_1',
            'confirm_password': 'Test_12',
            'system': 'IT'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_renew_password_pass(self):
        tester = password_generator.app.test_client(self)
        # send login data
        data = {
            'username': 'Honey',
            'password': 'Test@1446',
            'confirm_password': 'Test@1446',
            'system': 'Finance'}
        response = tester.post('/renew-password', data=data, follow_redirects=True)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()