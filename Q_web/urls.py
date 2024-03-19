from django.contrib import admin
from django.urls import path, include
# import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
# from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('__debug__/', include(debug_toolbar.urls)),
    path('users/', include('users.urls')),
    path("", include("quiz.urls")),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)