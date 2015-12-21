from django.db import models
from django.contrib.auth.models import User
from supplier.choices import *
from decimal import Decimal
# Create your models here.
class ProductAndServiceCategory(models.Model):
    '''
    Product category 
    '''
    category_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Category Name')

    def __unicode__(self):
        return self.category_name

class ProductServiceCode(models.Model):
    '''
    This model will take SIC, NAICS etc code.
    code_type = SERVICE_CODE_TYPE
    '''
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Code', unique=True)
    code_type = models.CharField(max_length=15, choices=SERVICE_CODE_TYPE, blank=True, null=True, verbose_name='Code Type')
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name='Title')
    common_keywords = models.CharField(max_length=200, blank=True, null=True, verbose_name='Common Keywords')
    category = models.ForeignKey(ProductAndServiceCategory, blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.code_type, self.code)


class Buyer(models.Model):
    company_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Company Name')
    login_url = models.URLField(max_length=256, blank=True, null=True, verbose_name='Login Url')
    registration_url = models.URLField(max_length=256, blank=True, null=True, verbose_name='Registration Url')
    buyer_introduction = models.CharField(max_length=500, blank=True, null=True, verbose_name='Buyer Introduction')
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name='State')
    ps_buy_code = models.ManyToManyField(ProductServiceCode, blank=True, null=True, related_name='comp_buy_codes')
    product_service_category = models.ManyToManyField(ProductAndServiceCategory, blank=True, null=True)

    def __unicode__(self):
        return self.company_name

class Supplier(models.Model):
    user = models.OneToOneField(User)
    salutation = models.CharField(max_length=5, blank=True, null=True, verbose_name='Salutation')
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Last Name')
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name='Position')
    phone_number = models.CharField(max_length=25, blank=True, null=True, verbose_name='Phone Number')
    fax_number = models.CharField(max_length=25, blank=True, null=True, verbose_name='Fax Number')
    cell_number = models.CharField(max_length=25, blank=True, null=True, verbose_name='Cell Number')
    contact_email = models.EmailField(blank=True,null=True, verbose_name='Contact E-Mail')
    contact_address = models.CharField(max_length=500, blank=True,null=True, verbose_name='Contact Address')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Country')
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name='State')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='City')
    zip_code = models.CharField(max_length=15, blank=True, null=True, verbose_name='Zip Code')
    method_of_notification = models.CharField(max_length=10, blank=True, null=True, verbose_name='Method of Notification')
    preferred_password = models.CharField(max_length=128, blank=True, null=True, verbose_name='Password')
    subscription_status = models.CharField(max_length=10, blank=True, null=True, verbose_name='Subscription Status')
    subscription_date = models.DateField(blank=True, null=True)
    subscription_expire_date = models.DateField(blank=True, null=True)
    profile_completion_status = models.CharField(max_length=10, blank=True, null=True, verbose_name='Profile Completion Status') 

    def __unicode__(self):
        return str(self.id)

    def get_profile_completion_status_redirect_url(self):
        if int(self.profile_completion_status) == 1:
            redirect_url = "/supplier/profile/company/revenue/"
        elif int(self.profile_completion_status) == 2:
            redirect_url = "/supplier/profile/company/contacts/"
        elif int(self.profile_completion_status) == 3:
            redirect_url = "/supplier/profile/company/licenses/"
        elif int(self.profile_completion_status) == 4:
            redirect_url = "/supplier/profile/company/products-services/"
        elif int(self.profile_completion_status) == 5:
            redirect_url = "/supplier/profile/company/certification/"
        elif int(self.profile_completion_status) == 6:
            redirect_url = "/supplier/submission-status/"
        elif int(self.profile_completion_status) == 0:
            redirect_url = "/supplier/profile/company/info/"
        elif int(self.profile_completion_status) == -1:
            redirect_url = "/supplier/profile/info/"
        else:
            redirect_url = "/supplier/submission-status/"

        return redirect_url

    def is_profile_complete(self):
        if self.salutation == None or self.salutation == '':
            return False
        elif self.first_name == None or self.first_name == '':
            return False
        elif self.last_name == None or self.last_name == '':
            return False
        elif self.position == None or self.position == '':
            return False
        elif self.phone_number == None or self.phone_number == '':
            return False
        elif self.cell_number == None or self.cell_number == '':
            return False
        elif self.contact_email == None or self.contact_email == '':
            return False
        elif self.contact_address == None or self.contact_address == '':
            return False
        elif self.country == None or self.country == '':
            return False
        elif self.state == None or self.state == '':
            return False
        elif self.city == None or self.city == '':
            return False
        elif self.preferred_password == None or self.preferred_password == '':
            return False
        else:
            return True


    def get_full_name(self):
        name = self.salutation
        if self.first_name:
            name += " " + self.first_name
        if self.last_name:
            name += " " + self.last_name
        return name

class CompanyCapabilityStatement(models.Model):
    capability_statement = models.TextField(max_length=250, blank=True, null=True, verbose_name='Capability Statement')
    upload_doc = models.FileField(blank=True, null=True, verbose_name='Document Upload',
        upload_to='attachment/doc')
    upload_video = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.capability_statement[:20])
   

class Address(models.Model):
    address_title = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    address_type = models.CharField(max_length=5, blank=True, null=True)

    def __unicode__(self):
        return "%s->%s" % (self.country, self.city)


class SupplierCompany(models.Model):
    supplier = models.OneToOneField(Supplier)
    comp_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Legal Company Name')
    organization_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='Organization Type')
    doing_business_as = models.CharField(max_length=200, blank=True, null=True, verbose_name='DBA Company Name')
    tax_id_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Federal Tax ID')
    social_security_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Social Security Number')
    comp_dunn_street = models.CharField(max_length=50, blank=True, null=True, verbose_name='Dunn & Brad Street Number')
    comp_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Company Phone Number')
    comp_fax = models.CharField(max_length=20, blank=True,null=True, verbose_name='Company Fax Number')
    comp_url = models.CharField(max_length=100, blank=True,null=True, verbose_name='Company Website (URL)')
    corporate_email = models.EmailField(blank=True,null=True, verbose_name='Corporate E-Mail')
    year_established = models.DateField(max_length=15,null=True, blank=True, verbose_name='Year Business was Established')
    num_of_employees = models.CharField(max_length=10,null=True, blank=True, verbose_name='Number Of Employees')
    # country = models.CharField(max_length=96, blank=True, null=True, verbose_name='Country')
    # state = models.CharField(max_length=96, blank=True, null=True, verbose_name='State')
    capability = models.ForeignKey(CompanyCapabilityStatement, blank=True, null=True)
    ps_categories = models.ManyToManyField(ProductAndServiceCategory, blank=True, null=True)
    product_service_description = models.TextField(max_length=200, blank=True,null=True, verbose_name='Product & Service Description')
    comp_logo = models.ImageField(blank=True, null=True, verbose_name='Current Company Logo', 
        upload_to='attachment/company/')
    comp_picture = models.ImageField(blank=True, null=True, verbose_name='Current Company/Personal Picture',
        upload_to='attachment/company/')
    comp_address = models.ForeignKey(Address, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)
    


class CompanyRevenue(models.Model):
    company = models.OneToOneField(SupplierCompany)
    last_year_annual_sale = models.CharField(max_length=10, blank=True, null=True)
    two_year_before_annual_sale = models.CharField(max_length=10, blank=True, null=True)
    three_year_before_annual_sale = models.CharField(max_length=10, blank=True, null=True)
    is_company_diverse = models.NullBooleanField(blank=True, null=True, default=None)
    is_company_publicly_traded = models.NullBooleanField(blank=True, null=True, default=None)
    is_sba = models.NullBooleanField(blank=True, null=True, default=None)
    minority_owned = models.NullBooleanField(blank=True, null=True, default=None)
    veteron_owned = models.NullBooleanField(blank=True, null=True, default=None)
    us_citizen_owned = models.NullBooleanField(blank=True, null=True, default=None)
    woman_owned = models.NullBooleanField(blank=True, null=True, default=None)
    service_disabled_vet = models.NullBooleanField(blank=True, null=True, default=None)
    owners_ethnicities = models.CharField(max_length=5, blank=True, null=True)
    payment_address = models.ForeignKey(Address, blank=True, null=True)
    remit_to_email = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return dict(ETHNICITIES)[int(self.owners_ethnicities)]

    @classmethod
    def get_last_year_annual_sale(self):
        return dict(ANNUAL_SALE)[int(self.last_year_annual_sale)]

    @classmethod
    def get_two_year_before_annual_sale(self):
        return dict(ANNUAL_SALE)[int(self.two_year_before_annual_sale)]

    @classmethod
    def get_three_year_before_annual_sale(self):
        return dict(ANNUAL_SALE)[int(self.three_year_before_annual_sale)]


class Reference(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    contact_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    services_provided = models.CharField(max_length=200, blank=True, null=True)
    company = models.ForeignKey(SupplierCompany)

    def __unicode__(self):
        return self.company_name + " :" + self.contact_name

class CompanyContact(models.Model):
    company = models.ForeignKey(SupplierCompany)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_ext = models.CharField(max_length=5, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    contact_type = models.CharField(max_length=5, choices=CONTACT_TYPE, blank=True, null=True)

    def __unicode__(self):
        return self.company.comp_name

class BusinessCertificate(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    upload_file = models.FileField(upload_to="/media/certificate/")
    company = models.ForeignKey(SupplierCompany)
    
    def __unicode__(self):
        return str(self.title)

class CompanyLicense(models.Model):
    company = models.ForeignKey(SupplierCompany)
    insurance_limit = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    business_license = models.FileField(upload_to="/media/license/", blank=True, null=True)
    geographical_service_area = models.CharField(max_length=20, blank=True, null=True)
    has_online_catalog = models.NullBooleanField(blank=True, null=True)
    can_sell_online = models.NullBooleanField(blank=True, null=True)
    accepts_credit_card = models.NullBooleanField(blank=True, null=True)
    is_edi_capable = models.NullBooleanField(blank=True, null=True)
    company = models.ForeignKey(SupplierCompany)

    def __unicode__(self):
        return str(self.insurance_limit)

    # business_certificate_files


class CompanyOwner(models.Model):
    company = models.ForeignKey(SupplierCompany)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female')), 
        blank=True, null=True)
    ethnicity = models.CharField(max_length=100, choices=ETHNICITIES, blank=True, null=True)
    percent_ownership = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


    def __unicode__(self):
        return self.company.comp_name


class CompanyProductService(models.Model):
    naics_code = models.CharField(max_length=200, blank=True, null=True)
    sic_code = models.CharField(max_length=200, blank=True, null=True)
    unspsc_code = models.CharField(max_length=200, blank=True, null=True)
    nigp_code = models.CharField(max_length=200, blank=True, null=True)
    cage_code = models.CharField(max_length=200, blank=True, null=True)
    company = models.OneToOneField(SupplierCompany)

    def __unicode__(self):
        return self.company.comp_name
   

class CertificateName(models.Model):
    cert_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=0)

    def __unicode__(self):
        return self.cert_name


class CompanyCertification(models.Model):
    certificate_name = models.OneToOneField(CertificateName, related_name='company_cert')
    cert_number = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    certification_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    certificate_duration = models.CharField(max_length=50, blank=True, null=True)
    upload_certificate = models.FileField(upload_to="/media/certification/", blank=True, null=True)
    company = models.ForeignKey(SupplierCompany)

    def __unicode__(self):
        return self.cert_number


class SupplierSelectedBuyers(models.Model):
    supplier = models.ForeignKey(Supplier)
    buyer = models.ForeignKey(Buyer)
    selection_date = models.DateTimeField(auto_now=True, auto_now_add=True, null=True, verbose_name='Selection Date')
    submission_date = models.DateTimeField(null=True, verbose_name='Submission Date')
    submission_status = models.CharField(max_length=10, choices=SUBMISSION_STATUS, blank=True, null=True, verbose_name='Submission Status') 

    def __unicode__(self):
        return dict(SUBMISSION_STATUS)[int(self.submission_status)]



"""
class Section(models.Model):
    #code
    section_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Section Name')
    display_order = models.IntegerField(blank=True, null=True, verbose_name='Display Order')

    def __unicode__(self):
        return self.section_name

    
class SupplierProfileField(models.Model):
    field_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Field Name')
    field_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='Field Type')
    character_limit = models.IntegerField(blank=True, null=True, verbose_name='Character Limit')
    required = models.NullBooleanField(default=False, blank=True, null=True, verbose_name='Required')
    section_to_display = models.ForeignKey(Section, blank=True, null=True, verbose_name='Section to display')
    display_order = models.IntegerField(blank=True, null=True, verbose_name='Display Order')
    default_value = models.CharField(max_length=50, blank=True, null=True, verbose_name='Default Value')
    options = models.CharField(max_length=200, blank=True, null=True, verbose_name='Field Name')


    def __unicode__(self):
        return self.field_name

class BuyerRequiredProfileField(models.Model):
    buyer = models.ForeignKey(Buyer)
    supplier_profile_field = models.ForeignKey(SupplierProfileField)
    # character_limit = models.IntegerField(max_length=50, blank=True, null=True, verbose_name='Character Limit')
    required = models.NullBooleanField(default=False, blank=True, null=True, verbose_name='Required')
    # section_to_display = models.ForeignKey(Section, blank=True, null=True, verbose_name='Section to display')
    # display_order = models.IntegerField(blank=True, null=True, verbose_name='Display Order')
    # default_value = models.CharField(max_length=50, blank=True, null=True, verbose_name='Default Value')
    # option_values = models.CharField(max_length=200, blank=True, null=True, verbose_name='Field Name')
    
class SupplierProfileFieldValue(models.Model):
    #code
    supplier = models.ForeignKey(Supplier)
    supplier_profile_field = models.ForeignKey(SupplierProfileField)
    field_value = models.CharField(max_length=50, blank=True, null=True, verbose_name='Field Value')
    option_values = models.CharField(max_length=100, blank=True, null=True, verbose_name='Option Values')

class SupplierRequestedBuyers(models.Model):
    #code
    buyer_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='Buyer Name')
    website = models.URLField(blank=True, null=True, verbose_name='Website')
    is_registered = models.BooleanField(blank=True, null=True, verbose_name='Is Registered')
    username = models.CharField(max_length=96, blank=True, null=True, verbose_name='User Name')
    password = models.CharField(max_length=96, blank=True, null=True, verbose_name='Password')

class SupplierSelectedBuyers(models.Model):
    supplier = models.ForeignKey(Supplier)
    buyer = models.ForeignKey(Buyer)
    selection_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Selection Date') 
    submission_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='Submission Status') 


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True, verbose_name='Company')
    contact_type = models.ForeignKey(ContactType, blank=True, null=True, verbose_name='Contact Type')
    name = models.CharField(max_length=100,null=True, blank=True, verbose_name='Contact Name')
    title = models.CharField(max_length=100,null=True, blank=True, verbose_name='Contact Title')
    phone = models.CharField(max_length=20,null=True, blank=True, verbose_name='Contact Phone Number')
    phone_ext = models.CharField(max_length=20,null=True, blank=True, verbose_name='Phone Ext.')
    fax = models.CharField(max_length=20,null=True, blank=True, verbose_name='Contact Fax Number')
    email = models.EmailField(blank=True,null=True, verbose_name='Contact E-Mail')
    gender = models.CharField(max_length=10,null=True, blank=True, verbose_name='Contact Gender')
    ethnicity = models.CharField(max_length=50,null=True, blank=True, verbose_name='Contact Ethnicity')
    percent_ownership = models.CharField(max_length=3, blank=True, null=True, default='0', verbose_name='Contact Ownership', )
    

    def __unicode__(self):
        return "%s" % (self.name)
"""