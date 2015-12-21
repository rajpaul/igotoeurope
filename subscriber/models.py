from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from supplier.models import *
# Create your models here.
from choices import PLAN_FREQUENCY


class Service(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Service Title')
    display_order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Package(models.Model):
    package_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Package Name')
    display_order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    services = models.ManyToManyField(Service)

    def __unicode__(self):
        return self.package_name

class Frequency(models.Model):
    '''
    duration = "MONTHLY, YEARLY, HALF-YEARLY, QUARTERLY"
    '''
    duration_title = models.CharField(max_length=50, choices=PLAN_FREQUENCY, blank=True, null=True)
    # standared_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return dict(PLAN_FREQUENCY)[self.duration_title]

    @classmethod
    def get_number(self):
        return self.duration_title

class PackagePlan(models.Model):
    frequency = models.ForeignKey(Frequency)
    package = models.ForeignKey(Package)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

class CouponCode(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    '''
    status = NotUsed, Used, Expired
    '''
    status = models.CharField(max_length=10, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    '''
    discount type will have two option (percent, fixed) valud 0 for fiexed amount and 1 for percent
    '''
    discount_type = models.CharField(max_length=2, choices=(('0', 'Fixed'), ('1', 'Percent')),
        blank=True, null=True)

    def __unicode__(self):
        return self.code

class CouponSupplier(models.Model):
    coupon = models.ForeignKey(CouponCode, blank=True, null=True)
    subscriber = models.ForeignKey(User, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.coupon, self.subscriber)

class Subscription(models.Model):
    user = models.ForeignKey(User)
    package_plan = models.ForeignKey(PackagePlan)
    subscription_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    coupon_used = models.ForeignKey(CouponCode, blank=True, null=True)
    plan_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    '''
        subscription_status = 0 for active, 1 for expired
    '''
    subscription_status = models.CharField(max_length=10, blank=True, null=True)

class ActivationCode(models.Model):
    '''
    status = 0, for newly created code
    status = 1, when a code is used
    status = 2, when code is not used and put in inactive state
    status = 3, when a code is not used before the expire time

    # deafault expire date is 48 hours from the creation date
    '''
    user = models.ForeignKey(User, blank=True, null=True)
    code = models.CharField(max_length=200, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expire_date = models.DateTimeField(default=datetime.now()+timedelta(days=2), blank=True, null=True)
    ACTIVATION_STATUS = ((0,"ACTIVE"), (1,"USED"), (2,"INACTIVE"), (3,"EXPIRED"))
    status = models.IntegerField(choices=ACTIVATION_STATUS)
    CODE_FOR = ((1,"PASSWORD_RESET"), (0,"USER_REGISTER"))
    code_for = models.IntegerField(choices=CODE_FOR, blank=True, null=True)

    def __unicode__(self):
        return self.code

    def is_expired(self):
        return self.expire_date > datetime.now()

    def is_active(self):
        return self.status == 0


class PaymentHistory(models.Model):
    supplier = models.ForeignKey(Supplier)
    plan = models.ForeignKey(PackagePlan)
    plan_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    coupon = models.ForeignKey(CouponCode, blank=True, null=True)

    payment_id = models.CharField(max_length=100, blank=True, null=True)
    transaction = models.CharField(max_length=500, blank=True, null=True)
    payment_status = models.CharField(max_length=10, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return "%s : %f" % (self.supplier.first_name, self.net_amount)