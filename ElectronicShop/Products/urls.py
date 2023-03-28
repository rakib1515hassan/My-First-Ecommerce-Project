from django.urls import path,include
from .views import *

urlpatterns = [
    path('Products_Details/<int:id>/', Products_Details, name="Products_Details"),
    #path('pro_eye/<int:id>/', pro_eye, name="pro_eye"),


    path('Products_Category_Show/<int:category_id>/', Products_Category_Show, name="Products_Category_Show"),
    path('Search_Products_results/', Search_Products_results, name="Search_Products_results"),
    path('filter-data/', filter_data, name='filter_data'),

    path('Add_To_Cart/<int:id>/', Add_To_Cart, name='Add_To_Cart'),
    path('Show_Cart/', Show_Cart, name='Show_Cart'),

    path('plus_cart/', plus_cart, name='plus_cart'),
    path('minus_cart/', minus_cart, name='minus_cart'),
    path('remove_cart/', remove_cart, name='remove_cart'),

    path('payment/', payment, name='payment'),
    path('payment_done/', payment_done, name='payment_done'),

    # path('ssl_status/', ssl_status, name='ssl_status'),
    # path('ssl_complete/<val_id>/<tran_id>/', ssl_complete, name='ssl_complete'),

    path('Success_Order/', Success_Order, name='Success_Order'),
    path('fail_order/', fail_order, name='fail_order'),


    path('Compleate_Pyment/', Compleate_Pyment, name='Compleate_Pyment'),
    path('add_wish_list/', add_wish_list, name='add_wish_list'),
    path('wish_delete/<id>', wish_delete, name='wish_delete'),
    path('Wish_Count/', Wish_Count, name='Wish_Count'),


    path('eye_products/', eye_products, name='eye_products'),
    path('abc/', abc, name='abc'),

    path('CartPDF/', CartPDF, name='CartPDF'),

]
