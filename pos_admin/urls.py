from django.urls import path
from .views import *


urlpatterns = [
    path('pos_admin_login/', pos_admin_login , name="pos_admin_login"),  
    path('pos_admin_add_cat/', pos_admin_add_cat , name="pos_admin_add_cat"), 
    path('pos_admin_add_product/', pos_admin_add_product , name="pos_admin_add_product"), 
    path('pos_admin_add_table/', pos_admin_add_table , name="pos_admin_add_table"), 
    path('pos_admin_home/', pos_admin_home , name="pos_admin_home"), 
    path('pos_admin_logout/', pos_admin_logout , name="pos_admin_logout"), 
]

