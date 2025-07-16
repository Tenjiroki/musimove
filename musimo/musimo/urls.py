# musimo/urls.py
from django.contrib import admin
from django.urls import path, include

# Переконайтесь, що використовуєте правильний шлях до 'musimi.urls'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('musimi.urls')),  # Перевірте, чи є файл musimi/urls.py
]



