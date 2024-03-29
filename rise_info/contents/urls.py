from django.urls import path
from contents import views

urlpatterns = [
    path("new/", views.content_new, name="content_new"),
    path("<int:content_id>/", views.content_detail, name="content_detail"),
    path("<int:content_id>/edit/", views.content_edit, name="content_edit"),
    path("content/del/<int:content_id>/",
         views.content_del, name="content_del"),
    path("content/up/<int:content_id>/", views.content_up, name="content_up"),
    path("content/down/<int:content_id>/",
         views.content_down, name="content_down"),
    path("menu/list/", views.menu_list, name="menu_list"),
    path("menu/new/", views.menu_new, name="menu_new"),
    path("menu/new/<int:menu_id>/", views.menu_edit, name="menu_edit"),
    path("menu/up/<int:menu_id>/", views.menu_up, name="menu_up"),
    path("menu/down/<int:menu_id>/", views.menu_down, name="menu_down"),
    path("menu/del/<int:menu_id>/", views.menu_del, name="menu_del"),
    path("<int:content_id>/comment/", views.add_comment, name="content_comment"),
    path("<int:content_id>/comment_del/<int:comment_id>/",
          views.del_comment, name="content_del_comment"),

]
