from django.test import TestCase, Client


class LoginTests(TestCase):

    def test_bad_login(self):
        c = Client()
        resp = c.post('/login/', data={'username': 'fakeuser',
                                       'password': 'wrongpswd'})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(b'Invalid login', resp.content)

    def test_empty_login(self):
        c = Client()
        resp = c.post('/login/', data={'username': '',
                                       'password': ''})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(b'Invalid login', resp.content)

    # Not committing my password, obviously. To make this test pass, try your
    #  own credentials :)  - Harry
    def test_student_login(self):
        c = Client()
        resp = c.post('/login/', data={'username': 'hu115',
                                       'password': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b'Logged in successfully', resp.content)