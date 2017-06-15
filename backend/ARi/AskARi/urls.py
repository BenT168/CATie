from django.conf.urls import url

from AskARi import views


urlpatterns = [
    url(r'^AskARi/question/(?P<code>[0-9]{3})/(?P<lectureURL>[a-zA-Z0-9-]{1,'
        r'60})/(?P<q_id>[0-9]+)/$', views.get_question),
    url(r'^AskARi/$', views.get_questions),
    url(r'^AskARi/#(?P<pg_no>[0-9]+)$', views.get_questions),
    url(r'^AskARi/(?P<code>[0-9]{3})/$', views.get_questions),
    url(r'^AskARi/(?P<code>[0-9]{3})/#(?P<pg_no>[0-9]+)$', views.get_questions),
    url(r'^AskARi/(?P<code>[0-9]{3})/(?P<lectureURL>[a-zA-Z0-9-]{1,60})/$',
        views.get_questions),
    url(r'^AskARi/(?P<code>[0-9]{3})/(?P<lectureURL>[a-zA-Z0-9-]{1,60})/#('
        r'?P<pg_no>[0-9]+)$', views.get_questions),
]
