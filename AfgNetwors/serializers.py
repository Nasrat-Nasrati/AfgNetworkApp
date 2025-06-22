from rest_framework import serializers
from .models import Operator, ServicePackage, Package, PackageDetail

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


class ServicePackageSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer(read_only=True)

    class Meta:
        model = ServicePackage
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    service_package = ServicePackageSerializer(read_only=True)

    class Meta:
        model = Package
        fields = '__all__'


class PackageDetailSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)

    class Meta:
        model = PackageDetail
        fields = '__all__'
