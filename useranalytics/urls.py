from django.conf.urls import patterns, include, url

from .views import *

urlpatterns = patterns('',
    url(r'^client/(?P<client_name>[-\w\d]+)/$', ClientView.as_view(), name='client'),
    url(r'^client/(?P<client_name>[-\w\d]+)/data/$', ClientDataView.as_view(), name='client-data'),
    url(r'^client/(?P<client_name>[-\w\d]+)/onlineusers/$',
        ClientOnlineUserView.as_view(), name='online_users'),

)