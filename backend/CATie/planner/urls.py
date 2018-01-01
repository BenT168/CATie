from django.conf.urls import url
from planner import views

urlpatterns = [
    url(r'^calendar/$', views.get_events),
    url(r'^calendar/create/$', views.create_event),
]
