from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^webapp/', include('webapp.foo.urls')),

    (r'^$', 'blog.post.index'),
    (r'^index/$', 'blog.post.index'),
    (r'^index/(?P<page>\d+)/$', 'blog.post.index'),
    (r'^post/(?P<post_id>\d+)/$', 'blog.post.details'),
    (r'^category/(?P<category_id>\d+)/$', 'blog.post.category'),                     
    (r'^category/(?P<category_id>\d+)/(?P<page>\d+)/$', 'blog.post.category'),
                       
    (r'^post/(?P<post_id>\d+)/comment/$', 'blog.post.comment'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
