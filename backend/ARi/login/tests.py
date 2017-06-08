import json

from django.test import TestCase, Client
from rest_framework import status
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Year, Course


class LoginTests(TestCase):

    username = 'arc13'
    password = 'shoutout2allthePears'

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

    def setUpGroups(self):
        second_year = Year(name='c2', number=2)
        second_year.save()
        concurrency = Course(name='Concurrency', code=223, ofYear=second_year)
        concurrency.save()

    def test_student_login(self):
        self.setUpGroups()
        c = Client()
        #resp = c.post('/login/', data={'username': self.username,
        #                               'password': self.password})
        #resp_content_str = resp.content.decode('utf-8')
        #resp_content_json = json.loads(resp_content_str)
        #decoded_payload = jwt_decode_handler(resp_content_json['token'])
        #self.assertEqual(resp.status_code, status.HTTP_200_OK)
        #self.assertEqual(decoded_payload['username'], self.username)
        pass
