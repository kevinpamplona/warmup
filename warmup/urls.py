from django.conf.urls import patterns, include, url
from django.contrib import admin
from users.views import HandlerView
from users.views import ResetView
from users.views import TestView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/login$', HandlerView.as_view(), name='my-view'),
    url(r'^users/add$', HandlerView.as_view(), name='my-view'),
    url(r'^TESTAPI/resetFixture$', ResetView.as_view(), name='reset-view'),
    url(r'^TESTAPI/unitTests$', TestView.as_view(), name='test-view'),
)
