from django.conf.urls import url

from notification import views

urlpatterns = [
    url(r'^notification/$', views.get_notification),
    url(r'^notification/create/$', views.create_notification),
]
