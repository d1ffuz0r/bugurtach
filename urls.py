from django.conf.urls.defaults import patterns, include, url
from bugurtach.views import homepage
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', homepage),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)