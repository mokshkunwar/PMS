import unittest
from password_generator import app
from flask import Flask

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.credentials = {
            'username': 'test@example.com',
            'password': 'Test_1234'}

    def test_login(self):
        tester = app.test_client(self)
        # send login data
        response = tester.post('/login_validation', data=self.credentials, follow_redirects=True)
        # should be logged in now

        self.assertTrue(response.status, 400)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
