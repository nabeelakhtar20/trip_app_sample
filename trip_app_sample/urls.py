from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('destination/', include('destination.urls')),
    path('trip/', include('trip.urls')),

]
