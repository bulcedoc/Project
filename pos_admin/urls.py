from django.urls import path
from .views import *


urlpatterns = [
    path('pos_admin_login/', pos_admin_login , name="pos_admin_login"),  
    path('pos_admin_add_cat/', pos_admin_add_cat , name="pos_admin_add_cat"), 
    path('pos_admin_add_product/', pos_admin_add_product , name="pos_admin_add_product"), 
    path('pos_admin_add_table/', pos_admin_add_table , name="pos_admin_add_table"), 
    path('pos_admin_home/', pos_admin_home , name="pos_admin_home"), 
    path('pos_admin_edit_product/', pos_admin_edit_product , name="pos_admin_edit_product"), 
    path('pos_admin_edits_product/<int:pk>/', pos_admin_edits_product , name="pos_admin_edits_product"), 
    path('pos_admin_edit_cat/', pos_admin_edit_cat , name="pos_admin_edit_cat"), 
    path('pos_admin_edits_cat/<int:pk>/', pos_admin_edits_cat , name="pos_admin_edits_cat"), 
    path('pos_admin_edit_tab/', pos_admin_edit_tab , name="pos_admin_edit_tab"), 
    path('pos_admin_edits_tab/<int:pk>/', pos_admin_edits_tab , name="pos_admin_edits_tab"), 
    path('pos_admin_del_pro/<int:pk>/', del_pro , name="del_pro"), 
    path('pos_admin_del_tab/<int:pk>/', del_tab , name="del_tab"), 
    path('pos_admin_logout/', pos_admin_logout , name="pos_admin_logout"), 
    path('pos_admin_reprint_bill/<int:pb>/<str:pd>/', pos_admin_reprint_bill , name="pos_admin_reprint_bill"), 
    path('pos_admin_view_bill/', pos_admin_view_bill , name="view_bill"),  
]

