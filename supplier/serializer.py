from rest_framework.serializers import ModelSerializer
from supplier.models import *


class CompanyCapabilitySerializer(ModelSerializer):

    class Meta:
        model = CompanyCapabilityStatement

class ProductAndServiceCategorySerializer(ModelSerializer):

    class Meta:
        model = ProductAndServiceCategory


class CompanySerializer(ModelSerializer):
    capability = CompanyCapabilitySerializer()
    ps_categories = ProductAndServiceCategorySerializer(many=True)

    class Meta:
        model = SupplierCompany


class AddressSerializer(ModelSerializer):
	class Meta:
		model = Address

class CompanyLicenseSerializer(ModelSerializer):
	class Meta:
		model = CompanyLicense


class CompanyProductServiceSerializer(ModelSerializer):
	class Meta:
		model = CompanyProductService

class CompanyCertificationSerializer(ModelSerializer):
	class Meta:
		model = CompanyCertification


class RevenueSerializer(ModelSerializer):
    payment_address = AddressSerializer()

    class Meta:
        model = CompanyRevenue