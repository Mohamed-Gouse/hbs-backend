from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth_app.urls')),
    path('api/', include('hotel_side.urls')),
    path('api/', include('user_side.urls')),
    path('api/', include('interactions.urls')),
    path('api/', include('super_admin.urls')),
    path('api/', include('chat.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
