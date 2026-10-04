from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static


admin.site.site_header = "سامانه مدیریت مشتریان | CRM"
admin.site.site_title = "پنل مدیریت"
admin.site.index_title = "خوش آمدید"

urlpatterns = [
   
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('customers.urls')),
    prefix_default_language=True,  
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)