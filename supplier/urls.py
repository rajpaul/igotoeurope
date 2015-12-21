from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:


    url(r'^profile/$', 'supplier.views.supplier_profile', name='supplier-profile'),
    url(r'^profile/api/(?P<id>\d+)/$', 'supplier.views.supplier_profile_json', name='supplier-profile-json'),
    url(r'^profile/info/$', 'supplier.views.supplier_profile', name='supplier-profile'),
    
    url(r'^profile/company/info/$', 'supplier.views.comapny_info', name='comapny-info'),
    url(r'^profile/company/info/api/(?P<supplier_id>\d+)/$', 'supplier.views.comapny_info_json', name='comapny-info-json'),
    
    url(r'^profile/company/revenue/$', 'supplier.views.company_revenue', name='company-revenue'),
    url(r'^profile/company/revenue/api/(?P<supplier_id>\d+)/$', 'supplier.views.company_revenue_json', name='company-revenue-json'),

    url(r'^profile/company/contacts/$', 'supplier.views.company_contacts', name='company-contacts'),
    url(r'^profile/company/licenses/$', 'supplier.views.company_licenses', name='company-licenses'),
    url(r'^profile/company/licenses/api/(?P<supplier_id>\d+)/$', 'supplier.views.company_licenses_json', name='company-licenses-json'),
    url(r'^profile/company/products-services/$', 'supplier.views.company_products_services', name='company-products-services'),
    url(r'^profile/company/products-services/api/(?P<supplier_id>\d+)/$', 'supplier.views.company_products_services_json',
                                                                    name='company-product-services-json'),
    url(r'^profile/company/certification/$', 'supplier.views.company_certification', name='company-certification'),
    url(r'^profile/company/certification/api/(?P<supplier_id>\d+)/$', 'supplier.views.company_certification_json',
                                                                    name='company-certification-json'),


    url(r'^search-corporation/$', 'supplier.views.search_corporation', name='search-corporation'),
    url(r'^search_buyers/$', 'supplier.views.search_buyers', name='search-buyers'),
    url(r'^save_buyers/$', 'supplier.views.save_buyers', name='save-buyers'),
    url(r'^delete_buyer/$', 'supplier.views.delete_buyer', name='delete-buyers'),
    url(r'^add_manual_buyer/$', 'supplier.views.add_manual_buyer', name='add-manual-buyers'),

    url(r'^search/buyer/$', 'supplier.views.search_buyer', name='search-buyer'),
    url(r'^submission-status/$', 'supplier.views.supplier_submission_status', name='submission-status'),

    # url(r'^search-corporation/$', 'supplier.views.search_corporation', name='search-corporation'),
    
)
