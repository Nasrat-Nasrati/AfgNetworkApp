from django.urls import path
from . import views

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
    path('operators/<int:operator_id>/service-packages/<int:pk>/', views.ServicePackageDetail.as_view(), name='servicepackage-detail'),
    path('operators/<int:operator_id>/service-packages/<int:pk>/edit/', views.ServicePackageUpdate.as_view(), name='servicepackage-edit'),
    path('operators/<int:operator_id>/service-packages/<int:pk>/delete/', views.ServicePackageDelete.as_view(), name='servicepackage-delete'),

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
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:pk>/',
        views.PackageDetail.as_view(),
        name='package-detail'  # برای نمایش جزئیات پکیج
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:pk>/edit/',
        views.PackageUpdate.as_view(),
        name='package-edit'
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:pk>/delete/',
        views.PackageDelete.as_view(),
        name='package-delete'
    ),


    # ✅ Bandle (PackageDetail) URLs (rewritten cleanly)

    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/bandels/',
        views.PackageDetailList.as_view(),
        name='bandel-list'
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/bandels/create/',
        views.PackageDetailCreate.as_view(),
        name='bandel-create'
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/bandels/<int:pk>/',
        views.PackageDetailView.as_view(),
        name='bandel-detail'
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/bandels/<int:pk>/edit/',
        views.PackageDetailUpdate.as_view(),
        name='bandel-edit'
    ),
    path(
        'operators/<int:operator_id>/service-packages/<int:service_package_id>/packages/<int:package_id>/bandels/<int:pk>/delete/',
        views.PackageDetailDelete.as_view(),
        name='bandel-delete'
    ),


        # ✅ Isolated Gallery URLs
    path('gallery/', views.GalleryList.as_view(), name='gallery-list'),
    path('gallery/create/', views.GalleryCreate.as_view(), name='gallery-create'),
    path('gallery/<int:pk>/', views.GalleryDetail.as_view(), name='gallery-detail'),
    path('gallery/<int:pk>/edit/', views.GalleryUpdate.as_view(), name='gallery-edit'),
    path('gallery/<int:pk>/delete/', views.GalleryDelete.as_view(), name='gallery-delete'),


]
