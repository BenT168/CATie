from django.conf.urls import url
from planner import views

urlpatterns = [
    url(r'^calendar/$', views.CalendarEventList.get_events),
    url(r'^calendar/create/$', views.CalendarEventList.create_event),
]
