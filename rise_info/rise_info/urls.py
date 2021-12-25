from django.contrib import admin
from django.urls import path, include
from django.conf import settings            # mdeditor
from django.conf.urls import handler400, url            # mdeditor
from django.conf.urls.static import static  # mdeditor

from rise_info import views

urlpatterns = [
    path("", views.top, name="top"),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("failuer_reports/", include("failuer_reports.urls")),
    path('infos/', include('infos.urls')),
    path('offices/', include('offices.urls')),
    url(r'mdeditor/', include('mdeditor.urls')), # mdeditor
]

handler404= 'rise_info.views.handler404'
if settings.DEBUG:  # mdeditor
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # mdeditor