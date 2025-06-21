
from django.db import models

class Operator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='operator_logos/')
    description = models.TextField()

    def __str__(self):
        return self.name


class ServicePackage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"{self.name} ({self.operator.name})"


class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)
    service_package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, related_name='packages')

    def __str__(self):
        return f"{self.name} ({self.service_package.name})"


class PackageDetail(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    activation_code = models.CharField(max_length=50, unique=True)
    deactivation_code = models.CharField(max_length=50)
    check_balance_code = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name} - {self.price} AFN"

