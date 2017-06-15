import json

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from rest_framework import status

from AskARi.models import Question
from courses.models import Year, Course
from lecture.models import Lecture
from lecture.utils import reformat_for_url
from login.models import ARiProfile


class AskARiTests(TestCase):
    year2 = None
    conc_dummy_lecture = None
    arch_dummy_lecture = None
    username = "arc13"
    password = "shoutout2allthePears"
    token = None
    name = "Concurrent Execution"
    video = "https://imperial.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id" \
            "=5154e0fc-84a3-4747-92fa-38c6db73d920"
    dummy_question = None
    q_title = "Sharing vs Relabelling in Chapter 3"
    q_body = "What is the difference between sharing and relabelling in this " \
             "example? Isn't the purpose of relabelling to match action names" \
             " to lead to sharing? Referring to the purple arrow above, " \
             "in this case, we have an a.release and b.release for the " \
             "resource process. In the lectures, the following examples were " \
             "used to show the difference between sharing and explicit " \
             "relabelling but surely in both cases, we are finding a way to " \
             "rename release to a.release and b.release to lead to the " \
             "resource and users sharing those two actions?"
    q_poster_name_dummy = 'hu115'
    q_url = '/AskARi/question/223/concurrent-execution/1/'


    def setUpAndLogin(self):
        c2 = Group.objects.create(name='c2')
        self.year2 = Year.objects.create(number=2, group=c2)
        conc_grp = Group.objects.create(name='Concurrency')
        self.conc_crse = Course.objects.create(name='Concurrency', code=223,
                                               ofYear=self.year2,
                                               group=conc_grp)
        self.conc_dummy_lecture = Lecture.objects.create(name=self.name,
                                                         course=self.conc_crse,
                                                         video=self.video)

        arch_grp = Group.objects.create(name='Architecture')
        self.arch_crse = Course.objects.create(name='Architecture', code=210,
                                               ofYear=self.year2,
                                               group=arch_grp)
        self.arch_dummy_lecture = Lecture.objects.create(name="Hardware Compilation",
                                                         course=self.arch_crse,
                                                         video=self.video)

        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        self.token = resp_content_json['token']

    def create_dummy_questions(self):
        user = User.objects.create(username='hu115')
        q_poster = ARiProfile.objects.create(user=user, year=self.year2)

        ruhi_user = User.objects.get(username='arc13')
        ruhi_poster = ARiProfile.objects.get(user=ruhi_user)

        self.dummy_question = \
            Question.objects.create(title=self.q_title, body=self.q_body,
                                    onLecture=self.conc_dummy_lecture,
                                    poster=q_poster)
        Question.objects.create(title="+ Set notation",
                                body="Guys, what is '+ All' doing here? What i "
                                     "tried in LTSA does not seem to clarify to "
                                     "me how a set is used.",
                                onLecture=self.conc_dummy_lecture,
                                poster=q_poster)
        Question.objects.create(title="Datapath diagram",
                                body="data path diagrams are",
                                onLecture=self.arch_dummy_lecture,
                                poster=ruhi_poster)


    def test_get_question(self):
        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        resp = c.get(self.q_url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        question = json.loads(resp_content_str)
        self.assertEqual(question['title'], self.q_title)
        self.assertEqual(question['body'], self.q_body)
        self.assertEqual(question['lecture'], reformat_for_url(self.name))
        self.assertEqual(question['poster'], self.q_poster_name_dummy)

    def test_create_question(self):
        self.setUpAndLogin()
        c = Client()
        resp = c.post('/AskARi/question/create/',
                      data={'title': self.q_title,
                            'body': self.q_body,
                            'code': 223,
                            'lecture': reformat_for_url(self.name)},
                      HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = c.get(self.q_url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        question = json.loads(resp_content_str)
        self.assertEqual(question['title'], self.q_title)
        self.assertEqual(question['body'], self.q_body)
        self.assertEqual(question['lecture'], reformat_for_url(self.name))
        self.assertEqual(question['poster'], self.username)

    def test_get_questions_conc(self):
        expected_questions = [{"title": "Sharing vs Relabelling in Chapter 3",
                               "body": "What is the difference between sharing " 
                                       "and relabelling in this example? Isn't the " 
                                       "purpose of relabelling to match action names " 
                                       "to lead to sharing? Referring to the purple " 
                                       "arrow above, in this case, we have an a.release " 
                                       "and b.release for the resource process. In "
                                       "the lectures, the following examples were "
                                       "used to show the difference between sharing "
                                       "and explicit relabelling but surely in both cases, "
                                       "we are finding a way to rename release to "
                                       "a.release and b.release to lead to the resource "
                                       "and users sharing those two actions?",
                               "lecture": "concurrent-execution",
                               "poster": "hu115"},
                              {"title": "+ Set notation",
                               "body": "Guys, what is '+ All' doing here? What i "
                                       "tried in LTSA does not seem to clarify to "
                                       "me how a set is used.",
                               "lecture": "concurrent-execution",
                               "poster": "hu115"}
                             ]


        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        url = '/AskARi/223/concurrent-execution/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        questions = json.loads(resp_content_str)

        pairs = zip(expected_questions, questions)

        self.assertFalse(any(x != y for x, y in pairs))

    def test_get_questions_all_courses(self):
        expected_questions = [{"title": "Sharing vs Relabelling in Chapter 3",
                               "body": "What is the difference between sharing "
                                       "and relabelling in this example? Isn't the "
                                       "purpose of relabelling to match action names "
                                       "to lead to sharing? Referring to the purple "
                                       "arrow above, in this case, we have an a.release "
                                       "and b.release for the resource process. In "
                                       "the lectures, the following examples were "
                                       "used to show the difference between sharing "
                                       "and explicit relabelling but surely in both cases, "
                                       "we are finding a way to rename release to "
                                       "a.release and b.release to lead to the resource "
                                       "and users sharing those two actions?",
                               "lecture": "concurrent-execution",
                               "poster": "hu115"},
                              {"title": "+ Set notation",
                               "body": "Guys, what is '+ All' doing here? What i "
                                       "tried in LTSA does not seem to clarify to "
                                       "me how a set is used.",
                               "lecture": "concurrent-execution",
                               "poster": "hu115"},
                              {"title": "Datapath diagram",
                               "body": "data path diagrams are",
                               "lecture": "hardware-compilation",
                               "poster": "arc13"}
                             ]


        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        url = '/AskARi/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        questions = json.loads(resp_content_str)

        pairs = zip(expected_questions, questions)

        self.assertFalse(any(x != y for x, y in pairs))
