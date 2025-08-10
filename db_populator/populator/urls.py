from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('status/', views.status_list, name='status_list'),
    path('status/add/', views.status_add, name='status_add'),
    path('productions/', views.productions_list, name='productions_list'),
    path('productions/add/', views.productions_add, name='productions_add'),
    path('bleaching_process/', views.bleaching_process_list, name='bleaching_process_list'),
    path('bleaching_process/add/', views.bleaching_process_add, name='bleaching_process_add'),
    path('transfers/', views.transfers_list, name='transfers_list'),
    path('transfers/add/', views.transfers_add, name='transfers_add'),
]
