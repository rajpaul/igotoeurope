from django.contrib import admin
from models import *

admin.site.register(Frequency)
admin.site.register(Package)
admin.site.register(Service)
admin.site.register(PackagePlan)
admin.site.register(CouponCode)
admin.site.register(CouponSupplier)
admin.site.register(PaymentHistory)

