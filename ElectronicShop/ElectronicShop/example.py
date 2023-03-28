if pay_meth == "SSL Commerz":
    settings = {'store_id': 'niyam6412dc52e1e89', 'store_pass': 'niyam6412dc52e1e89@ssl', 'issandbox': True}
    sslcommez = SSLCOMMERZ(settings)

    post_body = {}
    # set_urls -----------------------------------------------------------------
    # status_url = request.build_absolute_uri(reverse("ssl_status"))
    post_body['success_url'] = "http://127.0.0.1:8000/Success_Order/"
    post_body['fail_url'] = "http://127.0.0.1:8000/"
    post_body['cancel_url'] = "http://127.0.0.1:8000/"
    # ---------------------------------------------------------------------------

    # set_product_integration---------------------------------------------------
    cat_pro = Cart.objects.filter(user=request.user)
    # cat_pro_name = cat_pro[0].products.all()
    # cat_pro_count = cat_pro[0].products.count()

    post_body['total_amount'] = total_amount
    post_body['currency'] = "BDT"
    post_body['product_category'] = 'Computers Accessories'
    post_body['product_name'] = cat_pro
    post_body['num_of_item'] = 1
    post_body['shipping_method'] = "Sundarban Courier Service"
    post_body['product_profile'] = "general"
    # ---------------------------------------------------------------------------

    # set_customer_info -------------------------------------------------------
    user = request.user

    post_body['cus_name'] = user.get_full_name
    post_body['cus_email'] = user.email
    # --------------------------------------------------------------------------

    # set_shipping_info ------------------------------------------------------

    post_body['cus_add1'] = addr.Delivery_Address
    post_body['cus_city'] = addr.Sub_division
    post_body['cus_country'] = "Bangladesh"
    post_body['cus_phone'] = addr.Phone
    # --------------------------------------------------------------------------

    post_body['tran_id'] = "12345678"
    post_body['emi_option'] = 0
    post_body['multi_card_name'] = ""

    response = sslcommez.createSession(post_body)
    print("---------------------------")
    print(response)
    print("---------------------------")
    #return redirect(response['GatewayPageURL'])