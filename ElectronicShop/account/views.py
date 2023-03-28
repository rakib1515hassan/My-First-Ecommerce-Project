import os
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import random
import time
from django.http import HttpResponseRedirect, HttpResponse
from Products.models import *

# For Authentication-------------------------------------------------
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# For Email-----------------------------------------------------------
import uuid
from .utils import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage

# Hash Compare Password----------------------------------------------
from passlib.hash import django_pbkdf2_sha256


# Create your views here.**********************************************************************************************
def base(request):
    user = request.user
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        # cat_prod = Cart.objects.filter(user=user) < 3
    cat = Categoriys.objects.all()
    return render(request, "base.html", locals())

from django.urls import reverse
def home(request):
    user = request.user
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)[:2]
    carousel_img = Carousel_Image.objects.all()
    cat = Categoriys.objects.all()
    pro = Products.objects.all()
    top_sell = Products.objects.all()
    # Calculate Total Price For Cart View-------------------------------------
    amount = 0.00
    shipping_amount = 100.00
    total_amount = 0.00
    cart_products = [p for p in Cart.objects.all() if p.user == request.user]

    for p in cart_products:
        temp_amount = (p.quantity * p.products.Special_Price)
        amount = amount + temp_amount
        total_amount = amount + shipping_amount,

    # ------------------------------------------------------------------------
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------
    return render(request, "home.html", locals())


def Registration(request):
    if request.method == "POST":
        First_Name = request.POST["first_name"]
        Last_Name = request.POST["last_name"]
        User_Name = request.POST["user_name"]
        Email_Address = request.POST["email"]
        password = request.POST["password"]
        Confirm_Password = request.POST["c_password"]
        if password == Confirm_Password:
            if User.objects.filter(username=User_Name).exists():
                messages.error(request, 'User name is already taken.')
                return redirect(Registration)
            elif User.objects.filter(email=Email_Address).exists():
                messages.error(request, 'Email is already taken.')
                return redirect(Registration)
            else:
                user_obj = User.objects.create(first_name=First_Name, last_name=Last_Name, username=User_Name,
                                               email=Email_Address, password=password)
                user_obj.set_password(password)
                user_obj.save()
                messages.warning(request, 'Please check in your email, and verify your account.')
                return redirect(Login)
    return render(request, "Auth/sign-up.html")


# Verify Email-----------------------------------------------------
def activate_email(request, email_token):
    try:
        obj = Profile.objects.filter(email_token=email_token).first()
        if obj:
            obj.is_email_verified = True
            obj.save()
            messages.success(request, 'Profile is verified.')
            return redirect('Login')
        else:
            return HttpResponseRedirect("Profile is not valide.")
    except Exception as e:
        messages.error(request, 'Invalid Your Email.')
        return render(request, "Auth/sign-up.html")


def Login(request):
    if request.method == "POST":
        user_name = request.POST["username"]
        passw = request.POST["password"]

        user_obj = User.objects.filter(username=user_name).first()
        if user_obj is None:
            messages.error(request, "User Not Found")
            return redirect('Login')

        pro_obj = Profile.objects.filter(user=user_obj).first()
        if not pro_obj.is_email_verified:
            messages.error(request, "Email Is Not Verified")
            return redirect('Login')

        user = authenticate(username=user_name, password=passw)
        if user is None:
            messages.error(request, "User Not Found")
            return redirect('Login')
        login(request, user)
        return redirect('UserProfile')
    return render(request, "Auth/login.html")


@login_required
def LogOut(request):
    auth.logout(request)
    return redirect(Login)


@login_required
def UserProfile(request):
    user = request.user
    # Products Counts----------------------------------------------
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
    # --------------------------------------------------------------
    user1 = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        user1.date_of_birth = date_of_birth
        user1.gender = gender
        user1.phone = phone
        user1.address = address
        user1.save()
        return redirect(UserProfile)
    # Delete Profile-----------------------------------------------
    delete = request.GET.get('profile')
    if delete:
        delete_user = User.objects.get(id=delete)
        delete_user.delete()
        return redirect("Login")
    # --------------------------------------------------------------
    addresses = multi_address.objects.filter(user=request.user)

    # Show Place Order---------------------------------------------
    cat = Categoriys.objects.all()
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)
        order = Order.objects.filter(user=user)
        order_count = Order.objects.filter(user=user).count()
        # print(cat_prod)

        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        save_money = 0.00
        quantity = 1
        cart_products = [p for p in Cart.objects.all() if p.user == user]
        print("Cart Object: ", cart_products)

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.products.Special_Price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
    # --------------------------------------------------------------
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
        wish_prod = wishlist.objects.filter(user=user)
    #---------------------------------------------------------------

    data = {
        "user": user,
        "cat": cat,
        "count": count,
        "user1": user1,
        "addresses": addresses,

        "amount": amount,
        "total_amount": total_amount,
        "cat_prod": cat_prod,
        "order": order,
        "order_count": order_count,
        "count_wish": count_wish,
        "wish_prod": wish_prod,

    }
    return render(request, "Auth/profile.html", data)


@login_required
def Cover_Pic_Set(request):
    user1 = Profile.objects.get(user=request.user)
    try:
        if request.method == 'POST':
            c_pic = request.FILES.get('Cov_pic')
            if len(request.FILES) != 0:
                if len(user1.Cov_pic) > 0:
                    if user1.Cov_pic != 'default_cover.jpg':
                        os.remove(user1.Cov_pic.path)
                user1.Cov_pic = c_pic
            user1.save()
            return redirect(UserProfile)
        return render(request, 'Auth/profile.html', locals())
    except OSError as e:
        return render(request, 'Auth/profile.html', locals())


@login_required
def Profile_Pic_Set(request):
    user1 = Profile.objects.get(user=request.user)
    try:
        if request.method == 'POST':
            p_pic = request.FILES.get('pro_pic')
            if len(request.FILES) != 0:
                if len(user1.pro_pic) > 0:
                    if user1.pro_pic != 'default_pic.jpg':
                        os.remove(user1.pro_pic.path)
                user1.pro_pic = p_pic
            user1.save()
            return redirect(UserProfile)
        return render(request, 'Auth/profile.html', locals())
    except OSError as e:
        return render(request, 'Auth/profile.html', locals())


@login_required()
def change_password(request):
    if request.method == "POST":
        old_pass = request.POST["Old_Password"]
        new_pass = request.POST["New_Password"]
        cnew_pass = request.POST["New_Password_Confirmation"]
        if new_pass == cnew_pass:
            user = User.objects.get(id=request.user.id)
            un = user.username
            check = user.check_password(old_pass)
            if check == True:
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Your Password is successfully changed.')
                user = User.objects.get(username=un)
                return redirect("Login")
            else:
                messages.error(request, "Old password is wrong!")
                return redirect("UserProfile")
    return redirect(UserProfile)


@login_required()
def change_email(request):
    if request.method == "POST":
        Old_email = request.POST["Old_email"]
        New_Email = request.POST["New_Email"]
        Password = request.POST["Password"]
        user = User.objects.get(id=request.user.id)
        p = user.check_password(Password)
        if p == True:
            if user.email == Old_email:
                user.email = New_Email
                user.save()
                messages.success(request, 'Your Email is successfully changed.')
                return redirect(UserProfile)
        else:
            return redirect(Login)
    return redirect(UserProfile)


def forget_password(request):
    # otp = random.randint(1111, 9999)
    otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
    if request.method == "POST":
        email = request.POST.get('email')
        user_obj = User.objects.filter(email=email).first()
        pro_obj = Profile.objects.filter(user=user_obj).first()
        if user_obj:
            pro_obj.otp = otp
            pro_obj.save()
            send_otp(email, otp)
            request.session['email'] = request.POST['email']
            messages.success(request, "You OTP is send on your Email. Please Check Out.")
            return redirect('Enter_otp')
        else:
            messages.error(request, "Invalid Email, Please Enter Correct Email.")
    return render(request, "Auth/ForgetPass/forget_password.html")


def Enter_otp(request):
    email = request.session['email']
    if request.session.has_key('email'):
        user_obj = User.objects.filter(email=email).first()
        pro_obj = Profile.objects.filter(user=user_obj).first()
        if request.method == "POST":
            otp_u = request.POST.get('otp')

            if not otp_u:
                messages.error(request, "OTP is Required.")
                return redirect('Enter_otp')
            elif int(pro_obj.otp) == int(otp_u):
                messages.success(request, "Set New Password.")
                return redirect('password_reset')
            else:
                messages.error(request, "OTP is Invalid.")
                return redirect('Enter_otp')
    else:
        return redirect('forget_password')
    return render(request, "Auth/ForgetPass/enter_otp.html")


def password_reset(request):
    if request.session.has_key('email'):
        email = request.session['email']
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        if request.method == "POST":
            con_password = request.POST.get("con_password")
            if not password:
                messages.error(request, "Enter New Password.")
            elif not con_password:
                messages.error(request, "Enter Confirm Password.")
            elif django_pbkdf2_sha256.verify(password, user.password):
                messages.error(request, "This Password Already Exists, Try New Password.")
            elif password == con_password:
                user.password = password
                user.set_password(password)
                user.save()
                messages.success(request, 'Successfully set you password.')
                return redirect('Login')
            else:
                messages.error(request, "Password and Confirm Password is not same.")
    return render(request, "Auth/ForgetPass/password_reset.html")


def add_numbers(request):
    num1 = 7
    num2 = 5
    return render(request, 'abc.html', {'num1': num1, 'num2': num2})


def add_address(request):
    a_user = request.user
    user = User.objects.get(username=a_user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            division = request.POST.get('division')
            sub_division = request.POST.get('sub_division')
            zipcode = request.POST.get('zipcode')
            d_address = request.POST.get('d_address')
            phone = request.POST.get('d_phone')

            address = multi_address.objects.create(user=user, Division=division, Sub_division=sub_division,
                                                   Zipcode=zipcode, Delivery_Address=d_address, Phone=phone)

    return redirect(UserProfile)


def edit_address(request, id):
    a_user = request.user
    user = User.objects.get(username=a_user.username)
    if user.is_authenticated:
        if request.method == 'POST':
            division = request.POST.get('division')
            sub_division = request.POST.get('sub_division')
            zipcode = request.POST.get('zipcode')
            d_address = request.POST.get('d_address')
            phone = request.POST.get('d_phone')

            address = multi_address.objects.get(id=id)

            address.Division = division
            address.Sub_division = sub_division
            address.Zipcode = zipcode
            address.Delivery_Address = d_address
            address.Phone = phone
            address.save()

    return redirect(UserProfile)


def address_delete(request, id):
    addresses = multi_address.objects.get(id=id)
    addresses.delete()
    return redirect(UserProfile)