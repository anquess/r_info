from django.urls import path
from contents import views

urlpatterns = [
    path("new/", views.content_new, name="content_new"),
    path("<int:content_id>/", views.content_detail, name="content_detail"),
    path("<int:content_id>/edit/", views.content_edit, name="content_edit"),
]
