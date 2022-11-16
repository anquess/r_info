from django.urls import path

from . import views

urlpatterns = [
    path('', views.AddressList.as_view(), name='address_list'),
    path('new/', views.addresses_new, name='address_new'),
    path('<int:address_id>/edit/', views.addresses_edit, name='address_edit'),
    path('<int:address_id>/del/', views.addresses_del, name='address_del')

]
