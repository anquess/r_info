from django.urls import path
from . import views

urlpatterns = [
    path("", views.FailuerReportList.as_view(), name="failuer_report_list"),
    path("new/", views.failuer_report_new, name="failuer_report_new"),
    path("<int:info_id>/", views.failuer_report_detail,
         name="failuer_report_detail"),
    path("<int:info_id>/edit/", views.failuer_report_edit,
         name="failuer_report_edit"),
    path("<int:info_id>/del/", views.failuer_report_del, name="failuer_report_del"),
    path("<int:info_id>/send_mail/", views.sendmail,
         name="send_mail"),
]
