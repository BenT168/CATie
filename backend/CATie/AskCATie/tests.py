import json

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from rest_framework import status

from AskCATie.models import Question, Comment
from courses.models import Year, Course
from lecture.models import Lecture
from lecture.utils import reformat_for_url
from login.models import CATieProfile


class AskCATieTests(TestCase):
    year3 = None
    dummy_lecture = None
    simul_dummy_lecture2 = None
    vision_dummy_lecture = None
    username = "arc13"
    password = "shoutout2allthePears"
    token = None
    name = "Simulation and Modelling Introduction"
    video = "https://imperial.cloud.panopto.eu/Panopto/Pages/Embed.aspx?id" \
            "=df19de61-a458-49c8-ba48-e5aa611f7773"
    dummy_question = None
    q_title = "PS4 Q3, where do i find the example?"
    q_body = "Hi, I cannot seem to locate the example " \
             "of the 2 machines sharing an I/O device " \
             "in the notes for the question? Can anyone " \
             "point me in the right direction? Thanks!"
    q_poster_name_dummy = 'hu115'
    commenter_name_dummy = 'sib115'
    q_url = '/AskCATie/question/337/simulation-and-modelling-introduction/1/'
    c_content = 'Markov Process Slide 2'
    dummy_comment = None
    dummy_comment_id = None

    def setUpAndLogin(self):
        c3 = Group.objects.create(name='c3')
        self.year3 = Year.objects.create(number=3, group=c3)
        simul_grp = Group.objects.create(name='Simulation and Modelling')
        self.simul_crse = Course.objects.create(name='Simulation and Modelling', code=337,
                                               ofYear=self.year3,
                                               group=simul_grp)
        self.dummy_lecture = Lecture.objects.create(name=self.name,
                                                          course=self.simul_crse,
                                                          video=self.video)
        self.simul_dummy_lecture2 = Lecture.objects.create(name="Markov Process",
                                                          course=self.simul_crse,
                                                          video=self.video)

        arch_grp = Group.objects.create(name='Computer Vision')
        self.arch_crse = Course.objects.create(name='Computer Vision', code=316,
                                               ofYear=self.year3,
                                               group=arch_grp)
        self.vision_dummy_lecture = Lecture.objects.create(name="Projection",
                                                         course=self.arch_crse,
                                                         video=self.video)
        c = Client()
        resp = c.post('/login/', data={'username': self.username,
                                       'password': self.password})
        resp_content_str = resp.content.decode('utf-8')
        resp_content_json = json.loads(resp_content_str)
        self.token = resp_content_json['token']

    def create_dummy_question(self):
        user = User.objects.create(username='hu115')
        q_poster = CATieProfile.objects.create(user=user, year=self.year3)
        self.dummy_question = \
            Question.objects.create(title=self.q_title, body=self.q_body,
                                    parent=self.dummy_lecture,
                                    poster=q_poster)

    def create_dummy_questions(self):
        self.create_dummy_question()

        ruhi_user = User.objects.get(username='arc13')
        ruhi_poster = CATieProfile.objects.get(user=ruhi_user)

        Question.objects.create(title="Meaning of executing",
                                body="What exactly does executing mean? Is it "
                                     "issuing a request or start the servicing "
                                     "of said request?",
                                parent=self.simul_dummy_lecture2,
                                poster=ruhi_poster)
        Question.objects.create(title="Pinhole assumption",
                                body="Why do the pictures in the lecture slides "
                                     "show the centre of projection being behind "
                                     "the camera and the image not inverted?",
                                parent=self.vision_dummy_lecture,
                                poster=ruhi_poster)

    def create_commenter(self):
        user = User.objects.create(username=self.commenter_name_dummy)
        return CATieProfile.objects.create(user=user, year=self.year3)

    def create_dummy_comment(self, commenter):
        self.dummy_comment = \
            Comment.objects.create(content=self.c_content,
                                   poster=commenter,
                                   parent=self.dummy_question)
        self.dummy_comment_id = self.dummy_comment.id_per_question

    def test_get_question(self):
        self.setUpAndLogin()
        self.create_dummy_question()
        commenter = self.create_commenter()
        self.create_dummy_comment(commenter)
        c = Client()
        resp = c.get(self.q_url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        question = json.loads(resp_content_str)
        self.assertEqual(question['title'], self.q_title)
        self.assertEqual(question['body'], self.q_body)
        self.assertEqual(question['lecture'], reformat_for_url(self.name))
        self.assertEqual(question['poster'], self.q_poster_name_dummy)
        comments = question['comment_set']
        self.assertEqual(len(comments), 1)
        comment = comments[0]
        self.assertEqual(comment['poster'], self.commenter_name_dummy)
        self.assertEqual(comment['score'], 0)
        self.assertEqual(comment['questionId'], question['id'])
        self.assertEqual(comment['parentId'], None)

    def test_create_question(self):
        self.setUpAndLogin()
        c = Client()
        resp = c.post('/AskCATie/question/create/',
                      data={'title': self.q_title,
                            'body': self.q_body,
                            'code': 337,
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

    def test_post_comment(self):
        self.setUpAndLogin()
        self.create_dummy_question()
        c = Client()
        resp = c.post(self.q_url + 'reply/',
                      data={'content': self.c_content},
                      HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = c.get(self.q_url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        question = json.loads(resp_content_str)
        comments = question['comment_set']
        matching_comments = [d for d in comments if d['content'] ==
                             self.c_content]
        self.assertEqual(len(matching_comments), 1)
        my_comment = matching_comments[0]
        self.assertEqual(my_comment['poster'], self.username)
        self.assertEqual(my_comment['score'], 0)
        self.assertEqual(my_comment['questionId'], question['id'])
        self.assertEqual(my_comment['parentId'], None)

    def test_reply_to_comment(self):
        self.setUpAndLogin()
        self.create_dummy_question()
        self.create_dummy_comment(self.create_commenter())
        follow_up_content = "Hi there, I answered this question. Hope it helps."
        c = Client()
        resp = c.post(self.q_url + 'reply/',
                      data={'content': follow_up_content,
                            'parent': self.dummy_comment_id},
                      HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = c.get(self.q_url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        question = json.loads(resp_content_str)
        comments = question['comment_set']
        matching_comments = [d for d in comments if d['content'] ==
                             follow_up_content]
        self.assertEqual(len(matching_comments), 1)
        my_comment = matching_comments[0]
        self.assertEqual(my_comment['poster'], self.username)
        self.assertEqual(my_comment['score'], 0)
        self.assertEqual(my_comment['questionId'], question['id'])
        self.assertEqual(my_comment['parentId'], self.dummy_comment_id)



    # TODO: Ruhi - edit this so it adds the second question in a
    # create_dummy_questions method and ignores the id value
    def test_get_questions_conc_with_lec(self):
        # expected_questions
        q1_title = "PS4 Q3, where do i find the example?"
        q1_body = ("Hi, I cannot seem to locate the "
                   "example of the 2 machines sharing "
                   "an I/O device in the notes for "
                   "the question? Can anyone point me "
                   "in the right direction? Thanks!")
        q1_lecture = "simulation-and-modelling-introduction"
        q1_poster = "hu115"

        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        url = '/AskCATie/337/simulation-and-modelling-introduction/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        questions = json.loads(resp_content_str)

        self.assertTrue(questions[0]['title'] == q1_title)
        self.assertTrue(questions[0]['body'] == q1_body)
        self.assertTrue(questions[0]['lecture'] == q1_lecture)
        self.assertTrue(questions[0]['poster'] == q1_poster)

    def test_get_questions_conc_without_lec(self):
        # expected_questions
        q1_title = "PS4 Q3, where do i find the example?"
        q1_body = ("Hi, I cannot seem to locate the "
                   "example of the 2 machines sharing "
                   "an I/O device in the notes for "
                   "the question? Can anyone point me "
                   "in the right direction? Thanks!")
        q1_lecture = "simulation-and-modelling-introduction"
        q1_poster = "hu115"
        q2_title = "Meaning of executing"
        q2_body = ("What exactly does executing mean? Is it "
                   "issuing a request or start the servicing "
                   "of said request?")
        q2_lecture = "markov-process"
        q2_poster = "arc13"

        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        url = '/AskCATie/337/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        questions = json.loads(resp_content_str)

        self.assertTrue(questions[0]['title'] == q2_title)
        self.assertTrue(questions[0]['body'] == q2_body)
        self.assertTrue(questions[0]['lecture'] == q2_lecture)
        self.assertTrue(questions[0]['poster'] == q2_poster)

        self.assertTrue(questions[1]['title'] == q1_title)
        self.assertTrue(questions[1]['body'] == q1_body)
        self.assertTrue(questions[1]['lecture'] == q1_lecture)
        self.assertTrue(questions[1]['poster'] == q1_poster)

    def test_get_questions_all_courses(self):
        # expected_questions
        q1_title = "PS4 Q3, where do i find the example?"
        q1_body = ("Hi, I cannot seem to locate the "
                   "example of the 2 machines sharing "
                   "an I/O device in the notes for "
                   "the question? Can anyone point me "
                   "in the right direction? Thanks!")
        q1_lecture = "simulation-and-modelling-introduction"
        q1_poster = "hu115"
        q2_title = "Meaning of executing"
        q2_body = ("What exactly does executing mean? Is it "
                   "issuing a request or start the servicing "
                   "of said request?")
        q2_lecture = "markov-process"
        q2_poster = "arc13"
        q3_title = "Pinhole assumption"
        q3_body = ("Why do the pictures in the lecture slides "
                   "show the centre of projection being behind "
                   "the camera and the image not inverted?")
        q3_lecture = "projection"
        q3_poster = "arc13"

        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        url = '/AskCATie/'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        questions = json.loads(resp_content_str)

        self.assertTrue(questions[0]['title'] == q3_title)
        self.assertTrue(questions[0]['body'] == q3_body)
        self.assertTrue(questions[0]['lecture'] == q3_lecture)
        self.assertTrue(questions[0]['poster'] == q3_poster)

        self.assertTrue(questions[1]['title'] == q2_title)
        self.assertTrue(questions[1]['body'] == q2_body)
        self.assertTrue(questions[1]['lecture'] == q2_lecture)
        self.assertTrue(questions[1]['poster'] == q2_poster)

        self.assertTrue(questions[2]['title'] == q1_title)
        self.assertTrue(questions[2]['body'] == q1_body)
        self.assertTrue(questions[2]['lecture'] == q1_lecture)
        self.assertTrue(questions[2]['poster'] == q1_poster)

    def test_get_questions_all_courses_specific_page(self):
        # expected_questions
        q1_title = "PS4 Q3, where do i find the example?"
        q1_body = ("Hi, I cannot seem to locate the "
                   "example of the 2 machines sharing "
                   "an I/O device in the notes for "
                   "the question? Can anyone point me "
                   "in the right direction? Thanks!")
        q1_lecture = "simulation-and-modelling-introduction"
        q1_poster = "hu115"
        q2_title = "Meaning of executing"
        q2_body = ("What exactly does executing mean? Is it "
                   "issuing a request or start the servicing "
                   "of said request?")
        q2_lecture = "markov-process"
        q2_poster = "arc13"
        q3_title = "Pinhole assumption"
        q3_body = ("Why do the pictures in the lecture slides "
                   "show the centre of projection being behind "
                   "the camera and the image not inverted?")
        q3_lecture = "projection"
        q3_poster = "arc13"

        self.setUpAndLogin()
        self.create_dummy_questions()
        c = Client()
        url = '/AskCATie/#0'
        resp = c.get(url, HTTP_AUTHORIZATION=self.token)
        resp_content_str = resp.content.decode('utf-8')
        questions = json.loads(resp_content_str)

        self.assertTrue(questions[0]['title'] == q3_title)
        self.assertTrue(questions[0]['body'] == q3_body)
        self.assertTrue(questions[0]['poster'] == q3_poster)
        self.assertTrue(questions[0]['lecture'] == q3_lecture)

        self.assertTrue(questions[1]['title'] == q2_title)
        self.assertTrue(questions[1]['body'] == q2_body)
        self.assertTrue(questions[1]['lecture'] == q2_lecture)
        self.assertTrue(questions[1]['poster'] == q2_poster)

        self.assertTrue(questions[2]['lecture'] == q1_lecture)
        self.assertTrue(questions[2]['title'] == q1_title)
        self.assertTrue(questions[2]['body'] == q1_body)
        self.assertTrue(questions[2]['poster'] == q1_poster)

    def test_upvote(self):
        self.setUpAndLogin()
        self.create_dummy_question()
        self.create_dummy_comment(self.create_commenter())
        c = Client()
        resp = c.post(self.q_url + '1/rate/',
                      data={'rating': 1},
                      HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = c.get(self.q_url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_content_str = resp.content.decode('utf-8')
        question = json.loads(resp_content_str)
        comments = question['comment_set']
        matching_comments = [d for d in comments if d['content'] ==
                             self.c_content]
        self.assertEqual(len(matching_comments), 1)
        voted_comment = matching_comments[0]
        self.assertEqual(voted_comment['score'], 1)
        self.assertEqual(question['upvotes'], '1')

