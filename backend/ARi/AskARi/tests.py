import json

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from AskARi.models import Question
from courses.models import Year, Course
from lecture.models import Lecture


class AskARiTests(TestCase):
    dummy_lecture = None
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
    q_poster = None


    def setUpAndLogin(self):
        c2 = Group.objects.create(name='c2')
        year2 = Year.objects.create(number=2, group=c2)
        conc_grp = Group.objects.create(name='Concurrency')
        self.conc_crse = Course.objects.create(name='Concurrency', code=223,
                                               ofYear=year2,
                                               group=conc_grp)
        self.dummy_lecture = Lecture.objects.create(name=self.name,
                                                    course=self.conc_crse,
                                                    video=self.video)
        self.q_poster = User.objects.create(username='hu115')
        self.dummy_question = \
            Question.objects.create(title=self.q_title, body=self.q_body,
                                    onLecture=self.dummy_lecture,
                                    poster=self.q_poster)
        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        self.token = resp_content_json['token']


    # TODO: this function
    def test_get_question(self):
        pass

