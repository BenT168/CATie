from django.conf.urls import url

from AskARi import views

urlpatterns = [
    url(r'^AskARi/question/(?P<code>[0-9]{3})/(?P<lectureURL>[a-zA-Z0-9-]{1,'
        r'60})/(?P<q_id>[0-9]+)/$', views.get_question),
    url(r'^AskARi/all/?(#(?P<pg_no>[0-9]+))$', views.get_questions_all),
    url(r'^AskARi/(?P<code>[0-9]{3})/?(#(?P<pg_no>[0-9]+))$',
        views.get_questions_course),
    url(r'^AskARi/(?P<code>[0-9]{3})/(?P<lectureURL>[a-zA-Z0-9-]{1,60})/$',
        views.get_questions),
]