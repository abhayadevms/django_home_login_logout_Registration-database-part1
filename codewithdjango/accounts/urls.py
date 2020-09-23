from django.urls import path
from .views import (home,product,customer, createOrder, updateOrder,
                    deleteOrder, registration,login, logoutUser)

app_name = 'accounts'

urlpatterns =[
    path('', home, name = 'home'),

path('product/', product, name = 'product'),
path('customer/<str:pk_test>/', customer, name='customer'),
path('create_order/<str:pk_test>', createOrder, name = 'create_order'),
path('updaete_order/<str:pk_test>/', updateOrder, name='updateOrder'),
path('delete_order/<str:pk_test>/', deleteOrder, name='DeleteOrder'),
path('registration/', registration, name = 'registration'),
path('login/', login, name = 'login'),
path('logout/', logoutUser, name = 'logout'),

]