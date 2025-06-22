from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# this is all route of my serializer application 
# ✅ 1. ساخت router برای ViewSetها
router = DefaultRouter()
router.register(r'api/operators', views.OperatorViewSet)
router.register(r'api/service-packages', views.ServicePackageViewSet)
router.register(r'api/packages', views.PackageViewSet)
router.register(r'api/package-details', views.PackageDetailViewSet)


urlpatterns = [
    # Operator URLs
    path('operators/', views.OperatorList.as_view(), name='operator-list'),
    path('operators/create/', views.OperatorCreate.as_view(), name='operator-create'),
    path('operators/<int:pk>/', views.OperatorDetail.as_view(), name='operator-detail'),
    path('operators/<int:pk>/edit/', views.OperatorUpdate.as_view(), name='operator-edit'),
    path('operators/<int:pk>/delete/', views.OperatorDelete.as_view(), name='operator-delete'),

    # ServicePackage URLs
    path('operators/<int:operator_id>/service-packages/', views.ServicePackageList.as_view(), name='servicepackage-list'),
    path('operators/<int:operator_id>/service-packages/create/', views.ServicePackageCreate.as_view(), name='servicepackage-create'),
    path('service-packages/<int:pk>/', views.ServicePackageDetail.as_view(), name='servicepackage-detail'),
    path('service-packages/<int:pk>/edit/', views.ServicePackageUpdate.as_view(), name='servicepackage-edit'),
    path('service-packages/<int:pk>/delete/', views.ServicePackageDelete.as_view(), name='servicepackage-delete'),

    # Package URLs
   path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/',
        views.PackageList.as_view(),
        name='package-list'
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/create/',
        views.PackageCreate.as_view(),
        name='package-create'
    ),
    path('operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:pk>/', views.PackageDetail.as_view(), name='package-detail'),
    path('operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:pk>/edit/', views.PackageUpdate.as_view(), name='package-edit'),
    path('operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:pk>/delete/', views.PackageDelete.as_view(), name='package-delete'),

   # ===== PackageDetail URLs =====


    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/list/',
        views.PackageDetailList.as_view(),
        name='packagedetail-list'
    ),

    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/details/create/',
        views.PackageDetailCreate.as_view(),
        name='packagedetail-create'
    ),

    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/details/<int:pk>/',
        views.PackageDetailView.as_view(),
        name='packagedetail-detail'
    ),

    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/details/<int:pk>/edit/',
        views.PackageDetailUpdate.as_view(),
        name='packagedetail-edit'
    ),

    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/details/<int:pk>/delete/',
        views.PackageDetailDelete.as_view(),
        name='packagedetail-delete'
    ),

     path('', include(router.urls)), 

]


