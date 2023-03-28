from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from xhtml2pdf import pisa

from .models import *
from django.contrib import messages
from account.views import home
from account.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string, get_template
from django.contrib.auth.models import User
# from cart.cart import Cart

# For Paginator--------------------------------------
from django.core.paginator import Paginator

# For Searching--------------------------------------
from django.db.models import Q

# Paypal--------------------------------------------
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# For SSL Commerz----------------------------------
from sslcommerz_lib import SSLCOMMERZ


# from paypal.standard.forms import PayPalPaymentsForm


# Create your views here.
def Products_Details(request, id):
    user = request.user
    # Cat Product Show-------------------------------------------------------
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)[:2]
        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        save_money = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == user]
        # print("Cart Object: ",cart_products)

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.products.Special_Price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
    # --------------------------------------------------------------------------
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------
    cat = Categoriys.objects.all()
    pro = Products.objects.get(id=id)
    all_pro = Products.objects.all()[:5]
    related_products = Products.objects.filter(Category=pro.Category)[:6]
    # cat_logo = Categoriys.objects.filter()
    data = {
        "cat": cat,
        "count": count,
        "cat_prod": cat_prod,
        "total_amount": total_amount,
        "pro": pro,
        "all_pro": all_pro,
        "related_products": related_products,
        "count_wish": count_wish,
    }
    return render(request, "Products/Product-Detailes.html", data)


def Products_Category_Show(request, category_id):
    user = request.user
    # Cart Product Show ---------------------------------------------------------------
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)[:2]
        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        save_money = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == user]
        # print("Cart Object: ",cart_products)

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.products.Special_Price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
    # -------------------------------------------------------------------------------
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------
    cat = Categoriys.objects.all()
    pro = Products.objects.all()
    brand = Brand.objects.all()

    # cat = Categoriys.objects.filter(id=category_id)
    brandID = request.GET.get("brand_id")
    # print(brandID)
    pro = Products.objects.filter(Category=category_id)

    paginator = Paginator(pro, 12)  # Show 25 contacts per page.
    a = paginator.count
    # print("Total Products =", a)
    page_number = request.GET.get('page')
    # print("Page Number =",page_number)
    page_obj = paginator.get_page(page_number)
    # print("Next =", page_obj)
    nums = "a" * page_obj.paginator.num_pages
    return render(request, 'Products/Products_Category_Show.html', locals())


def Search_Products_results(request):
    user = request.user
    # Cart Product Show ---------------------------------------------------------------
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)[:2]
        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        save_money = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == user]
        # print("Cart Object: ",cart_products)

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.products.Special_Price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
    # -------------------------------------------------------------------------------
    # Category and Brand Show--------------------------------------
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
    cat = Categoriys.objects.all()
    brand = Brand.objects.all()
    # --------------------------------------------------------------
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------
    if request.method == "GET":
        query = request.GET.get("search")
        if query:
            query_set = (Q(Category__Category_Name__icontains=query)) | (
                Q(Product_Brand__Brand_Name__icontains=query)) | (Q(Product_Name__icontains=query))
            page_obj = Products.objects.filter(query_set).distinct()
            # Pagination ---------------------------------------------------------------------
            pro = Products.objects.filter(query_set).distinct()

            paginator = Paginator(pro, 12)  # Show 25 contacts per page.
            a = paginator.count
            # print("Total Products =", a)
            page_number = request.GET.get('page')
            # print("Page Number =",page_number)
            page_obj = paginator.get_page(page_number)
            # print("Next =", page_obj)
            nums = "a" * page_obj.paginator.num_pages
            # ---------------------------------------------------------------------------------
        else:
            page_obj = []
    # return render(request, 'Products/Search_products_result.html', locals())

    return render(request, 'Products/Products_Category_Show.html', locals())


# Filter Data---------------------------------------------------------------------------------------
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Products.objects.all().order_by('id').distinct()

    if len(categories) > 0:
        allProducts = allProducts.filter(Category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(Product_Brand__id__in=brands).distinct()

    page_obj = render_to_string('Products/Products_Container.html', {'page_obj': allProducts})
    return JsonResponse({'page_obj': page_obj})


def Add_To_Cart(request, id):
    user = request.user
    # prod = Products.objects.get(id=id)
    if user.is_authenticated:
        prod = Products.objects.get(id=id)
        if prod:
            if Cart.objects.filter(Q(user=user) & Q(products=prod)).exists():
                messages.success(request, "Products is already exist in your Cart.")
                return redirect('home')
            else:
                add_cart = Cart(user=user, products=prod)
                add_cart.save()
    return redirect('home')


def Show_Cart(request):
    user = request.user
    cat = Categoriys.objects.all()
    cart = Cart.objects.all()
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)
        # print(cat_prod)

        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        save_money = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == user]
        # print("Cart Object: ",cart_products)

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.products.Special_Price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------

    return render(request, 'Products/Add_To_Cart/cart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(products=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_products:
            temp_amount = (p.quantity * p.products.Special_Price)
            amount = amount + temp_amount
        data = {
            # 'save': c.save,
            'quantity': c.quantity,
            'total_price': c.total_price,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_products:
            temp_amount = (p.quantity * p.products.Special_Price)
            amount = amount + temp_amount
        data = {
            # 'save': c.save,
            'quantity': c.quantity,
            'total_price': c.total_price,
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
    return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        cart_products = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_products:
            temp_amount = (p.quantity * p.products.Special_Price)
            amount = amount + temp_amount
        data = {
            'amount': amount,
            'total_amount': amount + shipping_amount,
        }
    return JsonResponse(data)


def eye_products(request):
    # if request.method =='GET':
    #     prod_id = request.GET['prod_id']
    #     print("Products id = ",prod_id)
    #     eye = Products.objects.get(id=prod_id)
    #     # print(eye.Product_Name)
    #     data ={
    #         "Image": eye.Image.url,
    #         "P_N": eye.Product_Name,
    #         "P_M": eye.Product_Model,
    #         "P_B": eye.Product_Brand.Brand_Name,
    #         "P_C": eye.Category.Category_Name,
    #         "P_Sp": eye.Special_Price,
    #         "P_Re": eye.Regular_Price,
    #         "P_De": eye.Product_Details,
    #         "prod_id": prod_id,
    #     }
    return JsonResponse(data)


def payment(request):
    cat = Categoriys.objects.all()
    user = request.user
    addresses = multi_address.objects.filter(user=request.user)

    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)
        # print(cat_prod)

        amount = 0.00
        shipping_amount = 100.00
        total_amount = 0.00
        save_money = 0.00
        quantity = 1

        cart_products = [p for p in Cart.objects.all() if p.user == user]
        # print("Cart Object: ", cart_products)

        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.products.Special_Price)
                amount = amount + temp_amount
                total_amount = amount + shipping_amount
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------
    # data = {
    #     'addresses': addresses,
    #     'total_amount': total_amount,
    #     'amount': amount,
    #     'quantity': p.quantity ,
    # }
    return render(request, "Products/Add_To_Cart/checkout.html", locals())


def payment_done(request):
    user = request.user
    if request.method == "POST":
        addr_id = request.POST.get("address_id")
        pay_meth = request.POST.get("pay_method")
        # print("Our Address id = ", addr_id)
        # print("Your Pyment Method = ", pay_meth)
        if addr_id:
            addr = multi_address.objects.get(id=addr_id)
            # print("Our Address = ",addr)
            carts = Cart.objects.filter(user=user)
            # print("Our Products = ", carts)

            # Calculate ALl Products Total Price--------------------------------------------------
            amount = 0.00
            shipping_amount = 100.00
            total_amount = 0.00
            save_money = 0.00
            quantity = 1

            cart_products = [p for p in Cart.objects.all() if p.user == user]
            # print("Cart Object: ", cart_products)

            if cart_products:
                for p in cart_products:
                    temp_amount = (p.quantity * p.products.Special_Price)
                    amount = amount + temp_amount
                    total_amount = amount + shipping_amount
            # ---------------------------------------------------------------------------------------

            # Cash On Delivery--------------------------------------------------------------------------
            if pay_meth == "Cash On Delivery":
                if carts:
                    for c in carts:
                        Order(user=user, Delivery_address=addr, Order_Products=c.products, quentity=c.quantity,
                              Order_Confirm=True, Status="Accepted",
                              Pyment_Method="Cash On Delivery").save()
                        # print("All Products Price: ", Order.All_Produt_Price)
                        c.delete()
                    return redirect('Compleate_Pyment')
                else:
                    # print("Yor Products is not found.")
                    return redirect('home')
            # -------------------------------------------------------------------------------------------

            # SSL Commerz-------------------------------------------------------------------------------
            elif pay_meth == "SSL Commerz":
                # print("--------------------My Prement Method is SSL Commerz-------------")
                txn_id = 'TK_' + str(uuid.uuid4().hex)
                country ="Bangladesh"
                sslcz = SSLCOMMERZ(
                    {'store_id': 'niyam6412dc52e1e89', 'store_pass': 'niyam6412dc52e1e89@ssl', 'issandbox': True})
                total_amounts = request.GET.get('totalAmu')
                # print(total_amounts)

                if carts:
                    for c in carts:
                        Order(user=user, Delivery_address=addr, Order_Products=c.products, quentity=c.quantity,
                              Status="Accepted",
                              Pyment_Method="SSL Commerz").save()
                        c.delete()

                data = {

                    # set_urls -----------------------------------------------------------------
                    'success_url': "http://127.0.0.1:8000/Success_Order/",
                    'fail_url': "http://127.0.0.1:8000/fail_order/",
                    'cancel_url': "http://127.0.0.1:8000/fail_order/",
                    # ---------------------------------------------------------------------------

                    # set_product_integration---------------------------------------------------
                    'total_amount': total_amount,
                    'currency': "BDT",
                    'product_category': "Computers Accessories",
                    'product_name': "Computers Accessories",
                    'num_of_item': 1,
                    'shipping_method': "NO",
                    'product_profile': "general",
                    # ---------------------------------------------------------------------------

                    # set_customer_info --------------------------------------------------------
                    'cus_name': user.get_full_name,
                    'cus_email': user.email,
                    # ---------------------------------------------------------------------------

                    # set_shipping_info --------------------------------------------------------
                    'cus_add1': "customer address",
                    'cus_city': "Dhaka",
                    'cus_country': country,
                    'cus_phone': "01515612682",
                    # --------------------------------------------------------------------------

                    'tran_id': txn_id,
                    'emi_option': "0",
                    'multi_card_name': "",

                }

                response = sslcz.createSession(data)
                # print("---------------------------")
                # print(response)
                # print("---------------------------")
                return redirect(response['GatewayPageURL'])


        else:
            print("Yor Address is not found.")
    return redirect('payment')


# @csrf_exempt
# def ssl_status(request):
# if request.method=="post" or request.method=="POST":
#     pyment_data = request.POST
#     sta = request.pyment_data['ssl_status']
#     if sta == "VALID":
#         val_id = pyment_data['val_id']
#         val_id = pyment_data['tran_id']
#         return HttpResponseRedirect(reverse('ssl_complete', kwargs={'val_id': val_id, 'tran_id': tran_id}))
# return render(request, "abc.html")
#
#
# def ssl_complete(request, val_id, tran_id):
#     return HttpResponse("val_id: ", val_id)

@csrf_exempt
def Success_Order(request):
    txn_id = request.POST.get('tran_id')
    print("Payment Trangection ID =",txn_id)
    # Check if the payment is successful
    # if status == 'VALID' and payment_info.get('status') == 'VALID':
    #     # Get the user details from the payment information
    #     user_id = payment_info.get('user_id')
    #     print("User ID =",user_id)
    #     user_email = payment_info.get('value_a')
    #     print("Email = ",user_email)
    # user= request.user
    # carts = Cart.objects.filter(user=user)
    # if carts:
    #     for c in carts:
    #         Order(user=user, Delivery_address=addr, Order_Products=c.products, quentity=int(c.quantity), Order_Confirm=True,
    #               Status="Accepted",
    #               Pyment_Method="SSL Commerz").save()
    #         c.delete()
    return redirect("Compleate_Pyment")


@csrf_exempt
def fail_order(request):
    return redirect(payment)


def Compleate_Pyment(request):
    user = request.user
    Order_Product= None
    amount = 0.00
    shipping_amount = 100.00
    total_amu = 0.00
    save_money = 0.00
    quantity = 1
    count_pro = 0
    address = None
    if user.is_authenticated:
        count = Cart.objects.filter(user=user).count()
        cat_prod = Cart.objects.filter(user=user)[:2]
        order = [p for p in Order.objects.all() if p.user == user]

    if user.is_authenticated and order:
        Order_Product = Order.objects.filter(user=user)
        # Calculate ALl Products Total Price--------------------------------------------------
        order_pro = [p for p in Order.objects.all() if p.user == user]
        if order_pro:
            for p in order_pro:
                temp_amount = (p.quentity * p.Order_Products.Special_Price)
                amount = amount + temp_amount
                total_amu = amount + shipping_amount
                count_pro = count_pro + 1

        # Address Object--------------------------------------------------
        address = Order.objects.filter(user=user)
    # ----------------------------------------------------
    if user.is_authenticated:
        cat = Categoriys.objects.all()
    # ----------------------------------------------------
    # Wish List Show------------------------------------------------
    if user.is_authenticated:
        count_wish = wishlist.objects.filter(user=user).count()
    # ---------------------------------------------------------------
    data = {
        "cat": cat,
        "Order_Product": Order_Product,
        "amount": amount,
        "shipping_amount": shipping_amount,
        "total_amu": total_amu,
        "count_pro": count_pro,
        "address": address,
        "count": count,
        "cat_prod": cat_prod,
        "count_wish": count_wish,
    }
    return render(request, "Products/Add_To_Cart/order-success.html", data)


def add_wish_list(request):
    if request.method == 'GET':
        prod_id = request.GET['pid']
        # print("------------------------------------")
        # print("Wish List ID = ", prod_id)
        # print("------------------------------------")
    users = request.user
    if users.is_authenticated:
        pro_wish = Products.objects.get(id=prod_id)
        print(pro_wish)
        if pro_wish:
            if wishlist.objects.filter(Q(user=users) & Q(product=pro_wish)).exists():
                messages.success(request, "Products is already exist in your Wishlist.")
                data = {
                    'result': "already exist"
                }
                return JsonResponse(data)
            else:
                pro_wish_list = wishlist(user=users, product=pro_wish)
                pro_wish_list.save()
                wish_count = wishlist.objects.filter(user=users).count()
                data = {
                    'result': "Successfully add",
                    'wish_count': wish_count,
                }
                return JsonResponse(data)
    return redirect('home')


def wish_delete(request, id):
    w_obj = wishlist.objects.get(Q(product=id) & Q(user=request.user))
    w_obj.delete()
    return redirect("UserProfile")


def Wish_Count(request):
    users = request.user
    wish_count = wishlist.objects.filter(user=users).count()
    data = {
        'wish_count': wish_count,
    }
    return JsonResponse(data)


def abc(request):
    return render(request, "abc.html")


def CartPDF(request):
    user = request.user
    if user.is_authenticated:
        cat_prod = Cart.objects.filter(user=user)

        template_path = 'Products/Add_To_Cart/PDFformate/cardPdf.html'
        context = {'cat_prod': cat_prod}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = filename="card_report.pdf"
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

        # print(cat_prod)
    return render(request, 'Products/Add_To_Cart/PDFformate/cardPdf.html',locals())


def render_pdf_view(request):
    template_path = 'user_printer.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
