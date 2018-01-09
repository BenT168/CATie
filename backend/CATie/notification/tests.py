import json

from django.contrib.auth.models import User, Group
from django.test import Client, TestCase
from rest_framework import status
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Year, Course
from lecture.models import Lecture
from lecture.utils import reformat_for_url
from login.models import CATieProfile


class NotificationTests(TestCase):
    dummy_notification = None
    username = "admin"
    password = "fakepassword"
    token = None
    category = None
    name = "Region based segmentation"
    create_name = "Shared Objects & Mutual Exclusion"
    message = "Coursework deadline submission"

    def setUpData(self):
        User.objects.create_superuser(username=self.username,
                                      email="admin@admin.com",
                                      password=self.password)
        c3 = Group.objects.create(name='c3')
        year3 = Year.objects.create(number=3, group=c3)
        cv_grp = Group.objects.create(name='Computer Vision')
        self.conc_crse = Course.objects.create(name='Computer Vision', code=316,
                                               ofYear=year3,
                                               group=cv_grp)
        self.dummy_notification = Lecture.objects.create(name=self.name,
                                                    course=self.conc_crse,
                                                    message=self.message,
                                                    category= self.category)

    def loginAdmin(self):
        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        self.token = resp_content_json['token']

    def test_get_notification(self):
        self.setUpData()
        self.loginAdmin()
        c = Client()
        url = '/notification/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        self.assertEqual(resp_content_json['name'], self.name)
        self.assertEqual(resp_content_json['message'], self.message)

    def test_create_notification(self):
        self.setUpData()
        self.loginAdmin()
        c = Client()
        resp = c.post('/notification/create/',
                      data={'name': self.create_name,
                            'code': self.conc_crse.code,
                            'message': self.message},
                      HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        url = '/courses/' + str(self.conc_crse.code) + '/' + \
              reformat_for_url(self.create_name) + '/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        self.assertEqual(resp_content_json['name'], self.create_name)
        self.assertEqual(resp_content_json['message'], self.message)

