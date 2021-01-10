# import unittest
# from password_generator import app
# from flask import Flask
#
# class MyTestCase(unittest.TestCase):
#
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['DEBUG'] = False
#
#
#     def test_login(self):
#         tester = app.test_client(self)
#         # send login data
#         credentials = {
#             'username': 'test@example.com',
#             'password': 'Test_1234'}
#         response = tester.post('/login_validation', data=credentials, follow_redirects=True)
#         # should be logged in now
#
#         self.assertTrue(response.status, 400)
#
#
# if __name__ == '__main__':
#     unittest.main()
