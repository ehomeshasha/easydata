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
});