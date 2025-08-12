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
    path('productions/add-multiple/', views.productions_formset_view, name='productions_add_multiple'),
    path('bleaching_process/', views.bleaching_process_list, name='bleaching_process_list'),
    path('bleaching_process/add/', views.bleaching_process_add, name='bleaching_process_add'),
    path('transfers/', views.transfers_list, name='transfers_list'),
    path('transfers/add/', views.transfers_add, name='transfers_add'),
    path('transfers/add-multiple/', views.transfers_inline_formset_view, name='transfers_add_multiple'),
    path('checker/', views.production_vs_transfers_checker, name='production_vs_transfers_checker'),
    # API endpoints
    path('api/daily_production/', views.api_daily_production, name='api_daily_production'),
    path('api/weekly_production/', views.api_weekly_production, name='api_weekly_production'),
    path('api/monthly_production/', views.api_monthly_production, name='api_monthly_production'),
    path('dashboard/', views.infographics_dashboard, name='infographics_dashboard'),
    path('reports/', views.reports_index, name='reports_index'),
    path('reports/batch_production/', views.report_batch_production, name='report_batch_production'),
    path('reports/daily_transfer_details/', views.report_daily_transfer_details, name='report_daily_transfer_details'),
    path('reports/supervisor_transfer_summary/', views.report_supervisor_transfer_summary, name='report_supervisor_transfer_summary'),
    path('reports/daily_transfer_summary/', views.report_daily_transfer_summary, name='report_daily_transfer_summary'),
    path('reports/total_production/', views.report_total_production, name='report_total_production'),
    path('reports/total_transfer_summary/', views.report_total_transfer_summary, name='report_total_transfer_summary'),
]
