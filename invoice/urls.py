from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.generate_receipt, name="gen_receipt"),
    path('delete/<int:id>/', views.delete_invoice, name="delete_invoice"),
    # path('update/<int:id>/', views.update_item, name="update_item"),
    path('all_invoice/', views.all_invoice, name="all_invoice"),
    path('receipt/<int:id>/<str:receipt_no>/', views.single_invoice, name='single_invoice'),
    path('add_item/', views.add_items, name="add_item"),
    path('all_items/<str:receipt_no>/', views.receipt_items, name="all_items"),
]
