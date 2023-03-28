from django.db import models
from django.contrib.auth.models import User
from account.models import multi_address


# Create your models here.
# -----------------------------------Category Table--------------------------------------------------------------------
class Categoriys(models.Model):
    Category_Image = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png",
                                       upload_to="ProductsImage/Catagory_Image")
    Category_Name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Category_Name


# -----------------------------------Brand Table-----------------------------------------------------------------------
class Brand(models.Model):
    Brand_Name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Brand_Name


# -----------------------------------Products Table--------------------------------------------------------------------
class Products(models.Model):
    Category = models.ForeignKey(Categoriys, on_delete=models.CASCADE)
    Image = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png",
                              upload_to="ProductsImage/Laptop_Image")
    Image_1 = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png",
                                upload_to="ProductsImage/Laptop_Image")
    Image_2 = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png",
                                upload_to="ProductsImage/Laptop_Image")

    Product_Name = models.TextField(max_length=300, null=True, blank=True)
    Product_Model = models.TextField(max_length=300, null=True, blank=True)
    Product_Brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    Regular_Price = models.IntegerField(default=0)
    Special_Price = models.IntegerField(default=0)
    Warranty = models.CharField(max_length=50)

    Product_Details = models.TextField(max_length=1000)

    def __str__(self):
        return self.Product_Name



# -----------------------------------Carousel Image Table---------------------------------------------------
class Carousel_Image(models.Model):
    image_1 = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png", upload_to="Carousel")
    image_2 = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png", upload_to="Carousel")
    image_3 = models.ImageField(default="ProductsImage/Catagory_Image/CatagoryDefultImage.png", upload_to="Carousel")



# ----------------------------------------Cart Table----------------------------------------------------------
class Cart(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)

    purchesed = models.BooleanField(default=False)

    quantity = models.PositiveIntegerField(default=1)
    total = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.products.Product_Name} X {self.quantity}"
    @property
    def total_price(self):
        total = self.quantity * self.products.Special_Price
        total_amount = format(total, '0.2f')
        return total_amount
    # total_price = property(total_price)



# ----------------------------------------Place Order Payment Table------------------------------------------------
Order_Status = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel")
)
pyment_method = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Pyple", "Pyple"),
    ("SSL Commerz", "SSL Commerz"),
)


class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    Order_Products = models.ForeignKey(Products, related_name="products", on_delete=models.CASCADE)
    Delivery_address = models.ForeignKey(multi_address, on_delete=models.CASCADE)

    quentity = models.PositiveIntegerField(default=1)
    Order_Confirm = models.BooleanField(default=False)
    Confirm_Time = models.DateTimeField(auto_now_add=True)

    Payment_ID = models.CharField(max_length=300, blank=True, null=True)
    Order_ID = models.CharField(max_length=300, blank=True, null=True)

    Status = models.CharField(max_length=30, choices=Order_Status)
    Pyment_Method = models.CharField(max_length=50, choices=pyment_method, default="Cash On Delivery")

    @property
    def All_Produt_Price(self):
        total = 0
        for pro in self.Order_Products.all():
            total = total + float(pro.total_price())
        return total
    # all_products_price = property(total)

# ----------------------------------------Wish List Table-------------------------------------------------------------
class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



