from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Operator, ServicePackage, Package
from AfgNetwors.models import PackageDetail as PackageDetailModel  # جلوگیری از تداخل با نام ویو
# در بالای views.py اضافه کنید
from django.urls import reverse
from django.shortcuts import get_object_or_404





# ===== Operator Views =====
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


# ===== ServicePackage Views =====
class ServicePackageList(ListView):
    model = ServicePackage
    template_name = 'AfgNetwors/servicepackage_list.html'

    def get_queryset(self):
        operator_id = self.kwargs['operator_id']
        return ServicePackage.objects.filter(operator_id=operator_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        return context

class ServicePackageCreate(CreateView):
    model = ServicePackage
    fields = ['name']
    template_name = 'AfgNetwors/servicepackage_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs.get('operator_id')
        return context

    def form_valid(self, form):
        operator_id = self.kwargs.get('operator_id')
        form.instance.operator_id = operator_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('servicepackage-list', kwargs={'operator_id': self.kwargs['operator_id']})


class ServicePackageDetail(DetailView):
    model = ServicePackage
    template_name = 'AfgNetwors/servicepackage_detail.html'

class ServicePackageUpdate(UpdateView):
    model = ServicePackage
    fields = ['name', 'operator']
    template_name = 'AfgNetwors/servicepackage_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.object.operator_id  # 💡 get the related operator ID
        return context

    def get_success_url(self):
        return reverse_lazy('servicepackage-detail', kwargs={'pk': self.object.pk})

class ServicePackageDelete(DeleteView):
    model = ServicePackage
    template_name = 'AfgNetwors/servicepackage_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('servicepackage-list', kwargs={'operator_id': self.object.operator.pk})

# ===== Package Views =====

class PackageList(ListView):
    model = Package
    template_name = 'AfgNetwors/package_list.html'

    def get_queryset(self):
        service_package_id = self.kwargs['service_package_id']
        return Package.objects.filter(service_package_id=service_package_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context

class PackageCreate(CreateView):
    model = Package
    fields = ['name']  # فقط نام بسته، فیلد سرویس از URL گرفته می‌شود
    template_name = 'AfgNetwors/package_form.html'

    def dispatch(self, request, *args, **kwargs):
        # گرفتن سرویس معتبر از URL
        self.service_package = get_object_or_404(ServicePackage, id=self.kwargs['service_package_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # به صورت خودکار سرویس را به بسته اختصاص می‌دهد
        form.instance.service_package = self.service_package
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # برای استفاده در قالب (مثلا لینک‌ها و نمایش اطلاعات)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        context['service_package'] = self.service_package
        return context

    def get_success_url(self):
        # بعد از ایجاد، برمی‌گردد به لیست بسته‌های همان سرویس
        return reverse_lazy('package-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
        })


# class PackageCreate(CreateView):
#     model = Package
#     fields = ['name', 'service_package']
#     template_name = 'AfgNetwors/package_form.html'

#     def get_initial(self):
#         service_package_id = self.kwargs.get('service_package_id')
#         return {'service_package': service_package_id}

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['operator_id'] = self.kwargs['operator_id']
#         context['service_package_id'] = self.kwargs['service_package_id']
#         return context

#     def get_success_url(self):
#         return reverse_lazy('package-list', kwargs={
#             'operator_id': self.kwargs['operator_id'],
#             'service_package_id': self.kwargs['service_package_id']
#         })


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
    fields = ['name', 'service_package']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs['operator_id']
        context['service_package_id'] = self.kwargs['service_package_id']
        return context

    def get_success_url(self):
        return reverse_lazy('package-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id']
        })


# ===== PackageDetail Views =====


# نمایش لیست جزئیات یک بسته مشخص
class PackageDetailList(ListView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_list.html'
    package = None
    error_message = None

    def dispatch(self, request, *args, **kwargs):
        # تلاش برای گرفتن ServicePackage و Package
        operator_id = self.kwargs.get('operator_id')
        service_package_id = self.kwargs.get('service_package_id')
        package_id = self.kwargs.get('package_id')

        self.service_package = get_object_or_404(ServicePackage, id=service_package_id, operator_id=operator_id)
        self.package = get_object_or_404(Package, id=package_id, service_package=self.service_package)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # فقط جزئیات مربوط به بسته را می‌گیریم
        return PackageDetailModel.objects.filter(package=self.package)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'package': self.package,
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
            'package_id': self.kwargs['package_id'],
        })
        return context


# ایجاد جزئیات جدید برای بسته مشخص
class PackageDetailCreate(CreateView):
    model = PackageDetailModel
    fields = ['name', 'price', 'activation_code', 'deactivation_code', 'check_balance_code']
    template_name = 'AfgNetwors/packagedetail_form.html'

    def dispatch(self, request, *args, **kwargs):
        # برای اطمینان گرفتن بسته معتبر
        operator_id = self.kwargs.get('operator_id')
        service_package_id = self.kwargs.get('service_package_id')
        package_id = self.kwargs.get('package_id')

        self.service_package = get_object_or_404(ServicePackage, id=service_package_id, operator_id=operator_id)
        self.package = get_object_or_404(Package, id=package_id, service_package=self.service_package)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # ست کردن بسته روی مدل جزئیات قبل از ذخیره
        form.instance.package = self.package
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
        })
        return context

    def get_success_url(self):
        # بعد از ایجاد رکورد، برمی‌گردد به صفحه لیست آن بسته
        return reverse('packagedetail-list', kwargs={
            'operator_id': self.kwargs['operator_id'],
            'service_package_id': self.kwargs['service_package_id'],
            'package_id': self.kwargs['package_id'],
        })


# نمایش جزئیات یک رکورد خاص
class PackageDetailView(DetailView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
        })
        return context


# ویرایش یک رکورد جزئیات
class PackageDetailUpdate(UpdateView):
    model = PackageDetailModel
    fields = ['name', 'price', 'activation_code', 'deactivation_code', 'check_balance_code']
    template_name = 'AfgNetwors/packagedetail_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
        })
        return context

    def get_success_url(self):
        return reverse_lazy('packagedetail-detail', kwargs={
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
            'pk': self.object.pk,
        })


# حذف یک رکورد جزئیات
class PackageDetailDelete(DeleteView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
        })
        return context

    def get_success_url(self):
        return reverse_lazy('packagedetail-list', kwargs={
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
        })


# class PackageDetailList(ListView):
#     model = PackageDetailModel
#     template_name = 'AfgNetwors/packagedetail_list.html'
#     package = None
#     error_message = None  # برای پیام خطا به قالب

#     def get_service_package(self):
#         try:
#             return ServicePackage.objects.get(
#                 id=self.kwargs['service_package_id'],
#                 operator_id=self.kwargs['operator_id']
#             )
#         except ServicePackage.DoesNotExist:
#             self.error_message = "Service Package not found for the given Operator."
#             return None

#     def get_package(self, service_package):
#         try:
#             return Package.objects.get(
#                 id=self.kwargs['package_id'],
#                 service_package=service_package
#             )
#         except Package.DoesNotExist:
#             self.error_message = "Package not found under the given Service Package."
#             return None

#     def get_queryset(self):
#         service_package = self.get_service_package()
#         if not service_package:
#             return PackageDetailModel.objects.none()  # queryset خالی

#         self.package = self.get_package(service_package)
#         if not self.package:
#             return PackageDetailModel.objects.none()  # queryset خالی

#         return PackageDetailModel.objects.filter(package=self.package)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'package': self.package,
#             'operator_id': self.kwargs['operator_id'],
#             'service_package_id': self.kwargs['service_package_id'],
#             'package_id': self.kwargs['package_id'],
#             'error_message': self.error_message,
#         })
#         return context
    

# class PackageDetailCreate(CreateView):
#     model = PackageDetailModel
#     fields = ['name', 'price', 'activation_code', 'deactivation_code', 'check_balance_code']
#     template_name = 'AfgNetwors/packagedetail_form.html'

#     def form_valid(self, form):
#         package_id = self.kwargs.get('package_id')
#         form.instance.package_id = package_id
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['operator_id'] = self.kwargs.get('operator_id')
#         context['service_package_id'] = self.kwargs.get('service_package_id')
#         context['package_id'] = self.kwargs.get('package_id')
#         return context

#     def get_success_url(self):
#         return reverse(
#             'packagedetail-list',
#             kwargs={
#                 'operator_id': self.kwargs['operator_id'],
#                 'service_package_id': self.kwargs['service_package_id'],
#                 'package_id': self.kwargs['package_id'],  # یا self.object.package_id
#             }
#         )
    

# class PackageDetailView(DetailView):
#     model = PackageDetailModel
#     template_name = 'AfgNetwors/packagedetail_detail.html'



# class PackageDetailUpdate(UpdateView):
#     model = PackageDetailModel
#     fields = ['package', 'name', 'price', 'activation_code', 'deactivation_code', 'check_balance_code']
#     template_name = 'AfgNetwors/packagedetail_form.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # ارسال مقادیر مورد نیاز برای url template
#         context['operator_id'] = self.kwargs.get('operator_id')
#         context['service_package_id'] = self.kwargs.get('service_package_id')
#         context['package_id'] = self.kwargs.get('package_id')
#         return context

#     def get_success_url(self):
#         return reverse_lazy('packagedetail-detail', kwargs={
#             'operator_id': self.kwargs.get('operator_id'),
#             'service_package_id': self.kwargs.get('service_package_id'),
#             'package_id': self.kwargs.get('package_id'),
#             'pk': self.object.pk
#         })


# class PackageDetailDelete(DeleteView):
    model = PackageDetailModel
    template_name = 'AfgNetwors/packagedetail_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operator_id'] = self.kwargs.get('operator_id')
        context['service_package_id'] = self.kwargs.get('service_package_id')
        context['package_id'] = self.kwargs.get('package_id')
        return context

    def get_success_url(self):
        return reverse_lazy('packagedetail-list', kwargs={
            'operator_id': self.kwargs.get('operator_id'),
            'service_package_id': self.kwargs.get('service_package_id'),
            'package_id': self.kwargs.get('package_id'),
        })
