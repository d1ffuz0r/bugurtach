from django.conf.urls.defaults import patterns, include, url
from ajax.views import like
from bugurtach.views import homepage, user_settings, registration, add_bugurt, edit_bugurt, view_bugurt, all_bugurts, \
    delete_bugurt, view_user, view_tags
from django.contrib import admin
from django.contrib.auth.views import login, logout

import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', homepage),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login, {'redirect_field_name': 'next_url'}),
    url(r'^logout/', logout, {'next_page': '/'}),
    url(r'^registration/', registration),
    url(r'^settings/', user_settings),
    url(r'^bugurts/add', add_bugurt),
    url(r'^bugurts/(.*?)/edit/', edit_bugurt),
    url(r'^bugurts/(.*?)/delete/', delete_bugurt),
    url(r'^bugurts/(.*?)/', view_bugurt),
    url(r'^user/(.*?)/', view_user),
    url(r'^bugurts/', all_bugurts),
    url(r'^tags/(.*?)/', view_tags),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

ajax = patterns('',
    url('^ajax/like/', like)
)

urlpatterns += ajax