
from django.db import models

class Operator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='operator_logos/')
    description = models.TextField()

    def __str__(self):
        return self.name


class ServicePackage(models.Model):
    name = models.CharField(max_length=100)
    is_services = models.BooleanField(default=False)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"{self.name} ({self.operator.name})"


class Package(models.Model):
    name = models.CharField(max_length=100)
    service_package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, related_name='packages')
   

    def __str__(self):
        return f"{self.name} ({self.service_package.name})"


class PackageDetail(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    activation_code = models.CharField(max_length=50,null=True, blank=True)
    deactivation_code = models.CharField(max_length=50,null=True, blank=True)
    check_balance_code = models.CharField(max_length=50,null=True, blank=True)
    code = models.CharField(max_length=50)   # مثلاً: "*122#"
    description = models.TextField(blank=True, null=True)  # توضیحات (اختیاری)
    button_active = models.CharField(max_length=50, default="Active")
    button_deactive= models.CharField(max_length=50,default="Deactive")
    button_check_blance = models.CharField(max_length=50,default="Check blance")  # متن دکمه، مثل "قرضه" یا "افزودن"
    
    def __str__(self):
        return f"{self.name} - {self.price} AFN"
    

class Gallery(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # عنوان اختیاری تصویر

    def __str__(self):
        return f"Image for {self.operator.name}"