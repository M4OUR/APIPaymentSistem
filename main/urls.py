from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

def home(request):
    return HttpResponseRedirect('/admin/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('payments/', include('payments.urls')),
]
