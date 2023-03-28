$(document).on('click',".add-wishlist",function(){
     var pid = $(this).attr('data-product').toString();
	 console.log("Wish Product ID = ",pid)

     $.ajax({
         type: "GET",
         url:"/add_wish_list",
         data:{
            pid : pid
         },
         success: function(data){
         console.log("Total Wish=", data.wish_count)
         console.log("Wish list Status: ",data)
//         document.getElementById("wish_count").innerHTML = data.wish_count
         Wish_Count()
//         $('.wish_count').html(data.wish_count);
         }
     });
});

function Wish_Count(){
    $.ajax({
        method: "GET",
        url: "/Wish_Count",
        success: function(data){
           $('.wish_count').html(data.wish_count);
        }
    })
}

//$('#wish_delete').click(function(){
//    var id = $(this).attr("data-id").toString();
//    console.log(eml)
//    $.ajax({
//        type: "GET",
//        url: "/plus_cart",
//        data: {
//            prod_id: id
//        },
//        success: function(data){
//            console.log(data)
////            eml.innerText = data.quantity
//            document.getElementById("quantity" + id).innerText = data.quantity
//            document.getElementById("pro_total_price" + id).innerText = data.total_price
////            document.getElementById("myDIV").childNodes.length;=data.total_price
//            document.getElementById("amount").innerText = data.amount
//            document.getElementById("total_amount").innerText = data.total_amount
//
//
//        }
//    });
//});