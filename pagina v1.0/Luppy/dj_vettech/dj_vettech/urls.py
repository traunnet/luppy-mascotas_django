from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicioVet.urls')),      # Página de inicio
    path('auth/', include('loginVet.urls')),  # Sugerencia: usa 'auth/' para evitar confusión con el nombre de la vista
]

# Solo necesitas esto una vez y siempre fuera de la lista principal
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)