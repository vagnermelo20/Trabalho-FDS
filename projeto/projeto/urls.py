from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),  
     path('objetivos/', include('objetivos.urls')),
    path('base/', include('base.urls')),
    
]
