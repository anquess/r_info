from django.contrib import admin
from django.urls import path, include
from django.conf import settings            # mdeditor
from django.conf.urls import handler400, url            # mdeditor
from django.conf.urls.static import static  # mdeditor
# import debug_toolbar # django toolbar

from rise_info import views

urlpatterns = [
    path("", views.top, name="top"),
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("contents/", include("contents.urls")),
    path("failuer_reports/", include("failuer_reports.urls")),
    path('infos/', include('infos.urls')),
    path('offices/', include('offices.urls')),
    path('eqs/', include('eqs.urls')),
    url(r'mdeditor/', include('mdeditor.urls')),  # mdeditor
]

handler404 = 'rise_info.views.handler404'
if settings.DEBUG:  # mdeditor
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)    # mdeditor

# django toolbar
# if settings.DEBUG:
#    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
