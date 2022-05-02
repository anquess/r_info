from django.urls import path

from . import views

urlpatterns = [
    path('', views.file_upload, name='office'),
    path('download', views.file_downnload, name='office_download'),
    path("<str:office_id>/del/", views.office_del, name="office_del"),
]
