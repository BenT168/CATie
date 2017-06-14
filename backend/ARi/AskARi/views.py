from django.shortcuts import render


# Create your views here.
def get_question(request):
    return None


def get_questions(request, code, lectureURL, pg_no):
    return None


def get_questions_all(request, pg_no):
    return get_questions(request, None, None, pg_no)


def get_questions_course(request, code, pg_no):
    return get_questions(request, code, None, pg_no)
