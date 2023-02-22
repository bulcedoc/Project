from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import  settings
from .views import *

urlpatterns = [
    path('',home, name="sadada_home" ),
    path('', include('pos.urls')),
    path('', include('main.urls')),
    path('', include('pos_admin.urls')),
]

urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

handler404 = "sadada.views.err_404"
handler500 = "sadada.views.err_500"
handler400 = "sadada.views.err_400"
