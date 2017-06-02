from django.conf.urls import url
from planner import views

urlpatterns = [
    url(r'^events/$', views.CalendarEventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.CalendarEventDetail.as_view()),
]