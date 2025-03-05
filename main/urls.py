from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("API Payment System: Главная страница работает!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include('payments.urls')),
]