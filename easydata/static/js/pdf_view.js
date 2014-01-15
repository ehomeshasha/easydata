$(function(){
	$(document).on('mouseenter', '.tooltip', function(){
		$(this).animate({opacity: "1.0"}, 100);
	});
	$(document).on('mouseleave', '.tooltip', function(){
		$(this).animate({opacity: "0.4"}, 100);
	});
	$(document).on('click', '.tooltip', function(){
		var linenum = $(this).parent().attr("data-num");
		var page = $(".pn_input").val();
		var pdf_id = $("#pdf_id").val();
		var url = "/pdf/mark_view_line/"+pdf_id+'/'+page+'/'+linenum+'/'
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
	$(document).on('mouseenter', '.row_layer', function(){
		data_num = $(this).attr("data-num")
		var mark_html = '<a href="javascript:;" data-num='+data_num+' class="text-danger mark_link" style="">MARK</a>'
		$(this).addClass("opacity-grey");
		$(this).find(".row_layer_content").html(mark_html)
	});
	$(document).on('mouseleave', '.row_layer', function(){
		$(this).removeClass("opacity-grey");
		$(this).find(".row_layer_content").html("&nbsp;")
	});
	$(document).on('click', '.mark_link', function(e){
		e.preventDefault();
		if($(".hide_data_uid").html() == "None") {
			alert('Please login first');
			location.href="/account/login/?next="+location.href;
		}
		
		var linenum = $(this).attr("data-num");
		var page = $(".pn_input").val();
		var pdf_id = $("#pdf_id").val();
		var url = "/pdf/mark_post/"+pdf_id+'/'+page+'/'+linenum+'/'
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
	$(document).on('click', '.mark_nav_anchor', function(){
		url = $(this).attr("data-href");
		if(url == "") {
			return false;
		}
		$.ajax({
			url: url,
			type: "GET",
			error: function(){alert('try it again');return false;},
			success: function(data) {
				$("#response_modal").html(data);
			}
		});
	});
	$(document).on('click', '.delete_mark', function(){
		var url = jQuery(this).attr("data-href");
		var confirm_msg = 'Are you sure to delete this mark?'
		if(confirm(confirm_msg)) {
			jQuery.ajax({
				url: url,
	            type:'GET',
	            complete :function(){},
	            error: function() { alert('Please try again');},
	            success: function() {
	            	$(".mark_nav li[class*='active'] a").trigger('click');
	            }
			});
		}
	});
});