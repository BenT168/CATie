from django.conf.urls import url

from courses import views

urlpatterns = [
    url(r'^courses/$', views.get_courses),
]
