from django.urls import path
from infos import views

urlpatterns = [
    path("", views.InfoList.as_view(), name="info_list"),
    path("new/", views.info_new, name="info_new"),
    path("<int:info_id>/", views.info_detail, name="info_detail"),
    path("<int:info_id>/edit/", views.info_edit, name="info_edit"),
    path("<int:info_id>/del/", views.info_del, name="info_del"),
]
