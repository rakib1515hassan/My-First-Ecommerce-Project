$(document).ready(function(){
//	$(".ajaxLoader").hide();
	// Product Filter Start
	$(".filter-checkbox").on('click',function(){
		var _filterObj={};
		$(".filter-checkbox").each(function(index,ele){  //Call Back Function
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});

		});

        console.log(_filterObj)
		// Run Axios Ajax
		 axios.get(`/filter-data`,{params : _filterObj})
		 .then(res=>{
		 $("#filteredProducts").html('');
		 $("#filteredProducts").html(res.data.page_obj);
		 }).catch(err=> { console.log(err)})

	});
	// End

	// Filter Product According to the price
	$("#maxPrice").on('blur',function(){
		var _min=$(this).attr('min');
		var _max=$(this).attr('max');
		var _value=$(this).val();
		console.log(_value,_min,_max);
		if(_value < parseInt(_min) || _value > parseInt(_max)){
			alert('Values should be '+_min+'-'+_max);
			$(this).val(_min);
			$(this).focus();
			$("#rangeInput").val(_min);
			return false;
		}
	});
	// End
});