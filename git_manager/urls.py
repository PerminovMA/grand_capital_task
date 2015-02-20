__author__ = 'PerminovMA@live.ru'

from django.conf.urls import patterns, url
from gc_task.settings import STATIC_ROOT

urlpatterns = patterns('',
    url(r'^$', 'git_manager.views.index'),
    url(r'^github_login$', 'git_manager.oauth_views.github_auth_connect'),
    url(r'^log_out$', 'git_manager.oauth_views.log_out'),
    url(r'^get_reps$', 'git_manager.views.get_reps'),
    url(r'^get_rep_statistic$', 'git_manager.views.get_rep_statistic'),
    url(r'^github_auth_callback$', 'git_manager.oauth_views.github_auth_callback'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),
)