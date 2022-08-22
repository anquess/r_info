from django.urls import path
from tech_supports import views

urlpatterns = [
    path("", views.TechSupportList.as_view(), name="support_list"),
    path("new/", views.support_new, name="support_new"),
    path("<int:info_id>/", views.support_detail, name="support_detail"),
    path("<int:info_id>/edit/", views.support_edit, name="support_edit"),
    path("<int:info_id>/del/", views.support_del, name="support_del"),
    path("<int:info_id>/comment/", views.add_comment, name="support_comment"),
    path("<int:info_id>/comment_del/<int:comment_id>/",
         views.del_comment, name="support_del_comment"),
]
