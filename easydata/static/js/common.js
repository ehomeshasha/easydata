var digit_regex = /^\d+$/

function is_empty(obj) {
	if(typeof(redirect_url) == "undefined" || redirect_url = null || redirect_url == "") {
		return true;
	}
	return false;
}
function closeAlertMessageBox(delay) {
   var alert = $(".message_box").alert();
   window.setTimeout(function() { alert.alert('close') }, delay);
}

$(function(){
	
	$(".deletelink").click(function(){
		var id = jQuery(this).attr("data-id");
		var type = jQuery(this).attr("data-type");
		var redirect_url = jQuery(this).attr("data-redirect");
		var url = '/'+type+'/delete/'+id+'/'
		var confirm_msg = 'Are you sure to delete this '+type+'?'
		
		if(confirm(confirm_msg)) {
			jQuery.ajax({
				url: url,
	            type:'GET',
	            complete :function(){},
	            dataType: 'json', 
	            error: function() { alert('Please try again');},
	            
	            success: function() {
	            	if(is_empty) {
	            		location.href = location.href;
	            	} else {
	            		location.href = redirect_url;
	            	}
	            }
			});
		}
	});
	$(".pn_form").submit(function(){
		var pn_input = $(this).find(".pn_input").val();
		var pn = parseInt($(this).find(".maxpn").html().substr(1));
		if(!digit_regex.test(pn_input) || parseInt(pn_input) < 1 || parseInt(pn_input) > pn) {
			alert('Invalid pagenumber input')
			return false;
		}
		var data_mpurl = $(this).attr("data-mpurl");
		var url = data_mpurl + pn_input + '/'
		location.href = url
		return false;
	});
	$(".prev_btn, .next_btn").click(function(){
		var data_mpurl = $(this).parent().attr("data-mpurl");
		var num = $(this).attr("data-num")
		var url = data_mpurl + num + '/'
		location.href = url
	});
	$('[data-toggle="modal"]').bind('click',function(e) {
		
		e.preventDefault();
		var url = $(this).attr('data-href');
		if (url.indexOf('#') == 0) {
			$('#response_modal').modal('open');
		} else {
			$.get(url, function(data) {
	                        $('#response_modal').html(data);
	                        $('#response_modal').modal();
			}).success(function() {
				$('#response_modal input:text:visible:first').focus();
			});
		}
	});
	
});