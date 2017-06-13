from django.conf.urls import url
from django.views.defaults import page_not_found

from lecture import views

urlpatterns = [
    url(r'^courses/(?P<code>[0-9]{3})/general/(?P<nameURL>.{0})$',
        views.get_lecture),
    url(r'^courses/(?P<code>[0-9]{3})/(?P<nameURL>[a-zA-Z0-9-]{1,60})/$',
        views.get_lecture),
    url(r'^lectures/create/$', views.create_lecture),
]