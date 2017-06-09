import json

from django.contrib.auth.models import Group, User
from django.test import TestCase, Client

# Create your tests here.
from rest_framework_jwt.utils import jwt_decode_handler

from courses.models import Year, Course, Session
from login.models import ARiProfile


class CourseTests(TestCase):

    username = 'arc13'
    password = 'shoutout2allthePears'
    c2 = None
    conc_grp = None
    arch_grp = None
    year = None
    conc_crse = None
    arch_crse = None
    sesh = None

    def setUpGroups(self):
        self.c2 = Group.objects.create(name='c2')
        self.conc_grp = Group.objects.create(name='Concurrency')
        self.arch_grp = Group.objects.create(name='Architecture')
        self.year = Year.objects.create(number=2, group=self.c2)
        self.conc_crse = Course.objects.create(name="Concurrency", code=223,
                                               ofYear=self.year,
                                               group=self.conc_grp)
        self.arch_crse = Course.objects.create(name="Architecture", code=210,
                                               ofYear=self.year,
                                               group=self.arch_grp)
        self.sesh = Session.objects.create(name="Concurrent Execution",
                                           course=self.conc_crse)

    def setUpAndLogin(self):
        self.setUpGroups()
        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        username = jwt_decode_handler(resp_content_json['token'])['username']
        user = User.objects.get(username=username)
        return ARiProfile.objects.get(user=user)

    def test_set_up_works(self):
        self.setUpGroups()
        c2_retrieved = Group.objects.get(name='c2')
        conc = Group.objects.get(name='Concurrency')
        arch = Group.objects.get(name='Architecture')
        year = Year.objects.get(number=2)
        conc_crse = Course.objects.get(name="Concurrency")
        sesh = Session.objects.get(name="Concurrent Execution")
        arch_crse = Course.objects.get(code=210)
        self.assertEqual(self.c2, c2_retrieved)
        self.assertEqual(self.conc_grp, conc)
        self.assertEqual(self.arch_grp, arch)
        self.assertEqual(self.year, year)
        self.assertEqual(self.conc_crse, conc_crse)
        self.assertEqual(self.arch_crse, arch_crse)
        self.assertEqual(self.sesh, sesh)

    def test_login_sets_groups_correctly(self):
        ari_profile = self.setUpAndLogin()
        self.assertTrue(ari_profile.user.groups.filter(
            name='Concurrency').count())

    def test_ruhi_is_in_second_year(self):
        ari_profile = self.setUpAndLogin()
        self.assertTrue(ari_profile.year.number, 2)

    def test_ruhi_does_concurrency(self):
        ari_profile = self.setUpAndLogin()
        self.assertTrue(ari_profile.courses.get(code=223))

    # Turns out ruhi does do architecture, ignore this test
    # def test_ruhi_does_not_do_architecture(self):
    #     ari_profile = self.setUpAndLogin()
    #     self.assertFalse(ari_profile.courses.filter(code=210).count())



