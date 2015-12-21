from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pr3.views.home', name='home'),
    # url(r'^login/$', 'pr3.views.supplierlogin', name='login'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^subscriber/', include('subscriber.urls')),
    url(r'^supplier/', include('supplier.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
