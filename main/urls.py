from django.urls import path
from .views import *

urlpatterns = [
    path('admin_home/', admin_home, name="admin_home"),
    path('admin_pos_reg/', admin_reg, name="admin_reg"),
    path('admin_login/', admin_login, name="admin_login"),
    path('admin_logout/', admin_logout, name="admin_logout"),
]