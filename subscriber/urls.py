from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'subscriber.views.supplier_login', name='subscriber-login'),
    url(r'^logout/$', 'subscriber.views.supplier_logout', name='subscriber-logout'),
    
    url(r'^registration/$', 'subscriber.views.registration', name='registration'),
    url(r'^registration/(?P<activation_code>[\w]+)/active/$', 'subscriber.views.registration_active', name='registration-active'),
    url(r'^(?P<uid>\d+)/registration/success/$', 'subscriber.views.registration_success', name='registration-success'),

    url(r'^get-started/$', 'subscriber.views.get_started', name='get-started'),

    url(r'^get-coupon/(?P<code>[\w]+)/$', 'subscriber.views.get_coupon', name='get-coupon'),

    # url(r'^payment/$', 'supplier.views.payment', name='payment'),
    url(r'^payment/create/$', 'subscriber.views.payment_create', name='payment_create'),
    url(r'^payment/execute/$', 'subscriber.views.payment_execute', name='payment_execute'),
    url(r'^payment/success/$', 'subscriber.views.payment_success', name='payment_success'),

)
