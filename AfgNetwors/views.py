

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Operator, ServicePackage, Package,Gallery
from AfgNetwors.models import PackageDetail as PackageDetailModel  # جلوگیری از تداخل با نام ویو
# در بالای views.py اضافه کنید
from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import viewsets

from .serializers import (
    OperatorSerializer,
    ServicePackageSerializer,
    PackageSerializer,
    PackageDetailSerializer,
    GallerySerializer
)


# ===============================
# Operator Views
# ===============================
class OperatorList(ListView):
    model = Operator
    template_name = 'AfgNetwors/operator_list.html'


class OperatorCreate(CreateView):
    model = Operator
    fields = ['name', 'logo', 'description']
    template_name = 'AfgNetwors/operator_form.html'
    success_url = reverse_lazy('operator-list')


class OperatorDetail(DetailView):
    model = Operator
    template_name = 'AfgNetwors/operator_detail.html'


class OperatorUpdate(UpdateView):
    model = Operator
    fields = ['name', 'logo', 'description']
    template_name = 'AfgNetwors/operator_form.html'
    success_url = reverse_lazy('operator-list')


class OperatorDelete(DeleteView):
    model = Operator
    template_name = 'AfgNetwors/operator_confirm_delete.html'
    success_url = reverse_lazy('operator-list')


# ===============================
# ServicePackage Views
# ===============================
class ServicePackageList(ListView):
    model = ServicePackage
    fields = ['name', 'is_services']
    template_name = 'AfgNetwors/servicepackage_list.html'

    def get_queryset(self):
        return ServicePackage.objects.filter(operator_id=self.kwargs['operator_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        return context


class ServicePackageCreate(CreateView):
    model = ServicePackage
    fields = ['name','is_services']
    template_name = 'AfgNetwors/servicepackage_form.html'

    def form_valid(self, form):
        form.instance.operator_id = self.kwargs['operator_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('servicepackage-list', kwargs={'operator_id': self.kwargs['operator_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        return context


class ServicePackageDetail(DetailView):
    model = ServicePackage
    template_name = 'AfgNetwors/servicepackage_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        return context


class ServicePackageUpdate(UpdateView):
    model = ServicePackage
    fields = ['name','is_services']
    template_name = 'AfgNetwors/servicepackage_form.html'

    def get_success_url(self):
        return reverse_lazy('servicepackage-detail', kwargs={
            'operator_id': self.object.operator_id,  # ضروری
            'pk': self.object.pk
    })


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.object.operator_id
        return context


class ServicePackageDelete(DeleteView):
    model = ServicePackage
    template_name = 'AfgNetwors/servicepackage_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.object.operator_id
        return context

    def get_success_url(self):
        return reverse_lazy('servicepackage-list', kwargs={
            'operator_id': self.object.operator.pk
        })




# ===============================
# Package Views
# ===============================
class PackageList(ListView):
    model = Package
    template_name = 'AfgNetwors/package_list.html'

    def get_queryset(self):
        return Package.objects.filter(service_package_id=self.kwargs['service_package_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context


class PackageCreate(CreateView):
    model = Package
    fields = ['name']
    template_name = 'AfgNetwors/package_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.service_package = get_object_or_404(ServicePackage, id=self.kwargs['service_package_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.service_package = self.service_package
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('package-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context


class PackageDetail(DetailView):
    model = Package
    template_name = 'AfgNetwors/package_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context


class PackageUpdate(UpdateView):
    model = Package
    fields = ['name']
    template_name = 'AfgNetwors/package_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context

    def get_success_url(self):
        return reverse_lazy('package-detail', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
            'pk': self.object.pk
        })


class PackageDelete(DeleteView):
    model = Package
    template_name = 'AfgNetwors/package_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('package-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id']
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context


# ===============================
# PackageDetail Views
# ===============================
class PackageDetailList(ListView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.package = get_object_or_404(Package, id=self.kwargs['package_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return PackageDetailModel.objects.filter(package=self.package)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = self.package
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        context['package_id'] = self.kwargs['package_id']
        return context


class PackageDetailCreate(CreateView):
    model = PackageDetailModel
    fields = [
    'name',
    'price',
    'activation_code',
    'deactivation_code',
    'check_balance_code',]

    template_name = 'AfgNetwors/packagedetail_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.package = get_object_or_404(Package, id=self.kwargs['package_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.package = self.package
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        context['package_id'] = self.kwargs['package_id']
        return context

    def get_success_url(self):
        # اینجا نام url رو اصلاح کردیم به bandel-list
        return reverse('bandel-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
            'package_id': self.kwargs['package_id'],
        })


class PackageDetailView(DetailView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        context['package_id'] = self.kwargs['package_id']
        return context


class PackageDetailUpdate(UpdateView):
    model = PackageDetailModel
    fields = [
    'name',
    'price',
    'activation_code',
    'deactivation_code',
    'check_balance_code',]

    template_name = 'AfgNetwors/packagedetail_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        context['package_id'] = self.kwargs['package_id']
        return context

    def get_success_url(self):
        return reverse_lazy('bandel-detail', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
            'package_id': self.kwargs['package_id'],
            'pk': self.object.pk,
        })


class PackageDetailDelete(DeleteView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        context['package_id'] = self.kwargs['package_id']
        return context

    def get_success_url(self):
        return reverse_lazy('bandel-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
            'package_id': self.kwargs['package_id'],
        })
    





# ===============================
# ✅ Isolated Gallery Views
# ===============================

class GalleryList(ListView):
    model = Gallery
    paginate_by = 6   # تعداد تصاویر در هر صفحه
    template_name = 'AfgNetwors/gallery_list.html'


class GalleryCreate(CreateView):
    model = Gallery
    fields = ['operator', 'image', 'caption']
    template_name = 'AfgNetwors/gallery_form.html'
    success_url = reverse_lazy('gallery-list')


class GalleryDetail(DetailView):
    model = Gallery
    template_name = 'AfgNetwors/gallery_detail.html'


class GalleryUpdate(UpdateView):
    model = Gallery
    fields = ['operator', 'image', 'caption']
    template_name = 'AfgNetwors/gallery_form.html'
    success_url = reverse_lazy('gallery-list')


class GalleryDelete(DeleteView):
    model = Gallery
    template_name = 'AfgNetwors/gallery_confirm_delete.html'
    success_url = reverse_lazy('gallery-list')



# all views related to the serializer or api 
# 📦 API ViewSet برای Operator
class OperatorViewSet(viewsets.ModelViewSet):
    """
    API برای لیست کردن، ایجاد، بروزرسانی و حذف اپراتورها
    """
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer


# 📦 API ViewSet برای ServicePackage
class ServicePackageViewSet(viewsets.ModelViewSet):
    """
    API برای لیست کردن، ایجاد، بروزرسانی و حذف سرویس‌پکیج‌ها (برای هر اپراتور)
    """
    queryset = ServicePackage.objects.all()
    serializer_class = ServicePackageSerializer


# 📦 API ViewSet برای Package
class PackageViewSet(viewsets.ModelViewSet):
    """
    API برای لیست کردن، ایجاد، بروزرسانی و حذف پکیج‌ها
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


# 📦 API ViewSet برای PackageDetail
class PackageDetailViewSet(viewsets.ModelViewSet):
    queryset = PackageDetailModel.objects.all()  # ✅ درست
    serializer_class = PackageDetailSerializer



# 🖼️ API ViewSet برای Gallery
class GalleryViewSet(viewsets.ModelViewSet):
    """
    API برای تصاویر گالری مرتبط با اپراتورها
    """
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
