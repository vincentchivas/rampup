from django.conf.urls import patterns, include, url
import  settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testdjango.views.home', name='home'),
    # url(r'^testdjango/', include('testdjango.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/index/$','blog.views.index'),
    url(r'^site_static/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_PATH}),
    url(r'^blog/login/$','blog.views.login'),
    url(r'^blog/logout/$','blog.views.logout'),
    url(r'^blog/regist/$','blog.views.regist'),
    url(r'^blog/showreg/$','blog.views.showreg'),
    url(r'^blog/download/(?P<path>.*)','django.views.static.serve',{'document_root':'./static/blog/downfiles/','show_indexes':True}),
    #url(r'^cms/index/$','cms.views.index'),
    url(r'^blog/user/(?P<userid>\d{0,1})')
    )
