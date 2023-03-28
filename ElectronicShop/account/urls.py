from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('base/', base, name="base"),
    path("Registration/", Registration, name="Registration"),
    path("activate_email/<email_token>", activate_email, name="activate_email"),

    path("Login/", Login, name="Login"),
    path("LogOut/", LogOut, name="LogOut"),

    path("UserProfile/", UserProfile, name="UserProfile"),
    path("Cover_Pic_Set/", Cover_Pic_Set, name="Cover_Pic_Set"),
    path("Profile_Pic_Set/", Profile_Pic_Set, name="Profile_Pic_Set"),

    path("change_password/", change_password, name="change_password"),
    path("change_email/", change_email, name="change_email"),

    path('forget_password/', forget_password, name="forget_password"),
    path("Enter_otp/", Enter_otp, name="Enter_otp"),
    path("password_reset/", password_reset, name="password_reset"),
    path("password_reset/", password_reset, name="password_reset"),

    path("add_numbers/", add_numbers, name="add_numbers"),
    path('add_address/',add_address,name='add_address'),
    path('edit_address/<int:id>/',edit_address,name='edit_address'),
    path('address_delete/<int:id>/',address_delete,name='address_delete'),

]
