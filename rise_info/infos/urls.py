from django.urls import path
from infos import views

urlpatterns = [
    path("", views.InfoList.as_view(), name="info_list"),
    path("new/", views.info_new, name="info_new"),
    path("<int:info_id>/", views.info_detail, name="info_detail"),
    path("<int:info_id>/edit/", views.info_edit, name="info_edit"),
    path("<int:info_id>/del/", views.info_del, name="info_del"),
    path("<int:info_id>/comment/", views.add_comment, name="info_comment"),
    path("<int:info_id>/comment_del/<int:comment_id>/",
         views.del_comment, name="info_del_comment"),
    path("<int:info_id>/send/", views.sendmail, name='info_send'),
    path("export/", views.exportInfo, name='exportInfo'),
]
