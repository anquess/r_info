from django.urls import path

from . import views

app_name = 'eqs'

urlpatterns = [
    path('eqtypes/', views.file_upload, name='eqtype'),
    path('eqtypes/download/', views.file_downnload, name='eqtype_download'),
    path("eqtypes/<slug:slug>/del/", views.eqtype_del, name="eqtype_del"),
    path('eqtypes/api/posts/', views.api_posts_get, name='api_posts_get'),
    path('eqtypes/new/', views.eqtype_new, name='eqtype_new'),
    path('eqclass/new/', views.eq_class_new, name='eqclass_new'),
]
