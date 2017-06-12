from django.conf.urls import url

from session import views

urlpatterns = [
    url(r'^courses/(?P<code>[0-9]{3})/(?P<nameURL>[a-zA-Z0-9-]{1,60})/$',
        views.get_session),
    url(r'^sessions/create/$', views.create_session),
]
