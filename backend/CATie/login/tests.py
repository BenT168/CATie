import json

from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from rest_framework import status
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Year, Course
from lecture.models import Lecture


class LoginTests(TestCase):

    username = 'arc13'
    password = 'shoutout2allthePears'
    staffUsername = 'admin'
    staffPassword = 'fakepassword'

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
        c3 = Group.objects.create(name='c3')
        year3 = Year.objects.create(number=3, group=c3)
        cv_grp = Group.objects.create(name='Computer Vision')
        Course.objects.create(name='Computer Vision', code=316,
                              ofYear=year3, group=cv_grp)

    def test_student_login(self):
        self.setUpGroups()
        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        decoded_payload = jwt_decode_handler(resp_content_json['token'])
        self.assertEqual(decoded_payload['username'], self.username)

    def test_staff_login(self):
        self.setUpGroups()
        User.objects.create_superuser(username="admin", email="admin@admin.com",
                            password="fakepassword")
        c = Client()
        resp = c.post('/login/', data={'username': self.staffUsername,
                                       'password': self.staffPassword})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        decoded_payload = jwt_decode_handler(resp_content_json['token'])
        username = decoded_payload['username']
        self.assertEqual(decoded_payload['username'], self.staffUsername)
        user = User.objects.get(username=username)
        self.assertTrue(user.is_staff)
