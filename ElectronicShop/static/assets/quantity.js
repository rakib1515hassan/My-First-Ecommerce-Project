$('.plus-cart').click(function(){
    var id = $(this).attr("data-id").toString();
//    var eml = this.parentNode.parentNode.children[1]
//    console.log(eml)
    $.ajax({
        type: "GET",
        url: "/plus_cart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log(data)
//            eml.innerText = data.quantity
            document.getElementById("quantity" + id).innerText = data.quantity
            document.getElementById("pro_total_price" + id).innerText = data.total_price
//            document.getElementById("myDIV").childNodes.length;=data.total_price
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount


        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("data-id").toString();
//    var eml = this.parentNode.parentNode.children[1]
//    console.log(id)
    $.ajax({
        type: "GET",
        url: "/minus_cart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log(data)
//            document.getElementById("pro_total_price").innerText = data.total_price
//            eml.innerText = data.quantity
            document.getElementById("quantity" + id).innerText = data.quantity
            document.getElementById("pro_total_price" + id).innerText = data.total_price
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    });
});

$('.remove-cart').click(function(){
    var id = $(this).attr("data-id").toString();
    var eml = this
    console.log(id)
    $.ajax({
        type: "GET",
        url: "/remove_cart",
        data: {
            prod_id: id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            eml.parentNode.parentNode.remove()
        }
    });
});

//$('.eye-products').click(function(){
//    var id = $(this).attr("data-id").toString();
////    var eml = this
//    console.log(id)
//    $.ajax({
//        type: "GET",
//        url: "/eye_products",
//        data: {
//            prod_id: id
//        },
//        success: function(data){
//            console.log(data)
//            document.getElementById('Image').src = data.Image
//            document.getElementById("P_N").innerText = data.P_N
//            document.getElementById("P_Sp").innerText = "Price: "+ data.P_Sp +"TK"
//            document.getElementById("P_De").innerText = data.P_De
//            document.getElementById("P_B").innerText = data.P_B
//            document.getElementById("P_C").innerText = data.P_C
//            document.getElementById("prod_id").innerText = data.prod_id
//            add_to = document.getElementById("prod_id").innerHTML = parseInt(data.prod_id)
////            add_to_cart = document.getElementById("prod_id").innerHTML = "<a class="btn btn-dark" href="{% url 'Add_To_Cart' add_to_cart %}">Add To Cart</a>"
//
//            console.log(data.prod_id)
//            console.log(typeof(add_to))
//        }
//    });
//});



