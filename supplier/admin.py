from django.contrib import admin
from supplier.models import *
# Register your models here.

admin.site.register(Reference)
admin.site.register(CompanyContact)
admin.site.register(BusinessCertificate)
# admin.site.register(CompanyLicense)
admin.site.register(CompanyOwner)
admin.site.register(CompanyProductService)
admin.site.register(CertificateName)
admin.site.register(CompanyCertification)
admin.site.register(SupplierSelectedBuyers)
admin.site.register(CompanyRevenue)
admin.site.register(SupplierCompany)
admin.site.register(Address)
admin.site.register(CompanyCapabilityStatement)

admin.site.register(Supplier)
admin.site.register(Buyer)
admin.site.register(ProductServiceCode)
admin.site.register(ProductAndServiceCategory)