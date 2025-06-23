from django.contrib import admin
from .models import Operator, ServicePackage, Package, PackageDetail


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'operator')
    list_filter = ('operator',)
    search_fields = ('name',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_package',)
    list_filter = ('service_package',)
    search_fields = ('name',)
    readonly_fields = ('service_package',)


@admin.register(PackageDetail)
class PackageDetailAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'package', 'activation_code', 'deactivation_code',
        'check_balance_code', 'code', 'button_active', 'button_deactive', 'button_check_blance'
    )
    list_filter = ('package',)
    search_fields = ('name', 'activation_code', 'deactivation_code', 'check_balance_code', 'code')
