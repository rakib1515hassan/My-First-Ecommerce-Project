from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Categoriys)
class Catagory_admin(admin.ModelAdmin):
    list_display = ("Category_Name", "Category_Image")


@admin.register(Products)
class Products_admin(admin.ModelAdmin):
    list_display = ("Category", "Product_Name", "Product_Brand", "Product_Model")


@admin.register(Brand)
class Products_admin(admin.ModelAdmin):
    list_display = ("Brand_Name",)


@admin.register(Carousel_Image)
class Products_admin(admin.ModelAdmin):
    list_display = ("image_1", "image_2", "image_3")


@admin.register(Cart)
class Products_admin(admin.ModelAdmin):
    # list_display = ("image_1", "image_2", "image_3")
    pass


#admin.site.register(Order)
@admin.register(Order)
class Order_admin(admin.ModelAdmin):
    list_display = ("user", "Order_Products", "quentity", "Pyment_Method", "Order_Confirm")


@admin.register(wishlist)
class wishlist_admin(admin.ModelAdmin):
    list_display = ("user", "product",)