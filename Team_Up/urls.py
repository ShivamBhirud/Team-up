from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from team_up import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('team_up/', include('team_up.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


