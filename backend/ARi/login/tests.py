import json

from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from rest_framework import status
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Year, Course, Session


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
        c2 = Group.objects.create(name='c2')
        Year.objects.create(number=2, group=c2)

    def test_student_login(self):
        self.setUpGroups()
        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        decoded_payload = jwt_decode_handler(resp_content_json['token'])
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(decoded_payload['username'], self.username)
        pass
