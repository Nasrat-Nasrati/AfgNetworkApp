from django.contrib import admin
from .models import Operator, ServicePackage, Package, PackageDetail,Gallery
from django.utils.html import format_html

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'operator','is_services')
    list_filter = ('operator',)
    search_fields = ('name','is_services')


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
        'check_balance_code')
    list_filter = ('package',)
    search_fields = ('name', 'activation_code', 'deactivation_code', 'check_balance_code')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'operator', 'caption', 'image_tag', 'image')
    list_filter = ('operator',)
    search_fields = ('caption', 'operator__name')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Preview'


