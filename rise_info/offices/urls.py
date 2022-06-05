from django.urls import path

from . import views

urlpatterns = [
    path('', views.file_upload, name='office'),
    path('download', views.file_downnload, name='office_download'),
    path("<str:office_id>/del/", views.office_del, name="office_del"),
    path('api/posts/', views.api_posts_get, name='api_posts_get'),
]
