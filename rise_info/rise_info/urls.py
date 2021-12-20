from django.contrib import admin
from django.urls import path, include
from django.conf import settings            # mdeditor
from django.conf.urls import url            # mdeditor
from django.conf.urls.static import static  # mdeditor

from rise_info import views

urlpatterns = [
    path("", views.top, name="top"),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path('infos/', include('infos.urls')),
    url(r'mdeditor/', include('mdeditor.urls')), # mdeditor
]

if settings.DEBUG:  # mdeditor
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # mdeditor