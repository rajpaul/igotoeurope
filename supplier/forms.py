from django import forms
from supplier.models import *

class ProfileForm(forms.ModelForm):

	class Meta:
		model = Supplier
		exclude = ['subscription_status', 'profile_completion_status']


class CompInfoForm(forms.ModelForm):
	class Meta:
		model = SupplierCompany


class CapabilityForm(forms.ModelForm):
	class Meta:
		model = CompanyCapabilityStatement


class RevenueForm(forms.ModelForm):
	class Meta:
		model = CompanyRevenue
		exclude = ['company',]

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address

class CompanyLicenseForm(forms.ModelForm):
	class Meta:
		model = CompanyLicense
        exclude = ['company',]

class CompanyCertificationForm(forms.ModelForm):
	class Meta:
		model = CompanyCertification
        exclude = ['company',]

class CertificateNameForm(forms.ModelForm):
	class Meta:
		model = CertificateName
        exclude = ['display_order','active']

class CompanyProductServiceForm(forms.ModelForm):
    class Meta:
        model = CompanyProductService
        exclude = ['company',]

