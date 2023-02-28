from django.urls import path
from .views import *


urlpatterns = [
    path('pos_login/', pos_login , name="pos_login"), 
    path('pos_billing/', pos_billing , name="pos_billing"), 
    path('pos_cart/', pos_cart , name="pos_cart"), 
    path('pos_home/', pos_home, name="pos_home"), 
    path('pos_logout/', pos_logout, name="pos_logout"), 
    path('pos_checkouts/', pos_checkouts ,name='pos_checkouts'), 
    path('pos_checkout/<str:pk>/', pos_checkout,name='pos_checkout'), 
    path('pos_bill/', pos_bill ,name='pos_bill'),
    path('pos_tables/', pos_tables ,name='pos_tables'),
    path('pos_b_t/<int:pi>/<str:pn>/', pos_b_t ,name='pos_b_t'),
    path('fast_pos_billing/',fast_pos_billing,name='fast_pos_billing'),
    path('fast_pos_check/<str:bill>',fast_pos_check,name='fast_pos_check'),

]   

