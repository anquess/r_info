from django.urls import path
from . import views

urlpatterns = [
    path("", views.failuer_report_list, name="failuer_report_list"),
#    path("new/", views.info_new, name="info_new"),
#    path("<int:info_id>/", views.info_detail, name="info_detail"),
#    path("<int:info_id>/edit/", views.info_edit, name="info_edit"),
#    path("<int:info_id>/del/", views.info_del, name="info_del"),
]