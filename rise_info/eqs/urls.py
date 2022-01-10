from django.urls import path

from . import views

urlpatterns = [
    path('eqtypes/', views.file_upload, name='eqtype'),
    path('eqtypes/api/', views.get_eqtypes_json, name='eqtype_api'),
    path("eqtypes/<slug:slug>/del/", views.eqtype_del, name="eqtype_del"),
]