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
	
	$("a[href^='#']").each(function(){
		var href = $(this).attr("href").substr(1);
		var word_reg = /^\w+$/;
		if(word_reg.test(href)) {
			var obj = $("#"+href);
			obj.parent().css("position", "relative");
			obj.css("position", "absolute").css("top","-100px");
		}
	});
	
	$('.breadcrumb .addicon').tooltip();
	
	$(".lang_select").click(function(){
		var lang_code = $(this).attr("data-code");
		var uid = $(this).attr("data-uid");
		if(uid != "None") {
			location.href = "/change_account_language/"+uid+"/"+lang_code+"/?next="+location.href
		} else {
			$("#languageSel").val(lang_code);
			$("#lang_select_form").submit();
		}
		
		
		
	});
	$(document).on('change', '.upload_file', function(){
		//var formData = new FormData($('#mark_form')[0]);
		var formData = new FormData();
		var inputfile = $(this);
		var module = $(this).attr("data-module");
		var upload_type = $(this).attr("data-type");
		
		formData.append("module", module);
		formData.append("upload_type", upload_type)
		formData.append("upload_file", document.getElementById($(this).attr("id")).files[0])
		$(this).val("");
		var data_inputid = $(this).attr("data-inputid");
	    $.ajax({
			url: "/ajax_upload/",
			type: "post",
			dataType: 'json',
			data: formData,
			processData: false,
			contentType: false,
			success: function(response) {
				if(response.code == -1) {
					alert(response.msg)
				} else if(response.code == 1) {
					$("#"+data_inputid).val(response.target_savepath);
					inputfile.attr("data-mimetype", response.content_type);
					inputfile.attr("data-name", response.name);
					
				}
			},
			error: function(jqXHR, textStatus, errorMessage) {
				alert('upload failed');return false;
			}
		});
	});
	
	$(".deletelink").click(function(){
		var id = jQuery(this).attr("data-id");
		var type = jQuery(this).attr("data-type");
		var redirect_url = jQuery(this).attr("data-redirect");
		
		if(jQuery(this).attr("data-noslash") == '1') {
			var url = '/'+type+'delete/'+id+'/'
		} else {
			var url = '/'+type+'/delete/'+id+'/'
		}
		
		
		var confirm_msg = 'Are you sure to delete this '+type+'?(cannot be undone)';
		
		if(confirm(confirm_msg)) {
			jQuery.ajax({
				url: url,
	            type:'GET',
	            complete :function(){},
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
	
	
	$(".gotop_btn").click(function(){
		$("html, body").animate({ scrollTop: 0 }, "fast");
		return false;
	});
	/*
	$('#response_modal').on('hidden.bs.modal', function (e) {
		location.href = location.href;
	});*/
	$("#table td").mouseenter(function(){
		$(this).parent().find(".viewmore_td").each(function(){
			var td = $(this).find("div");
			var td0 = td.eq(0);
			var td1 = td.eq(1);
			td0.addClass("hidden");
			td1.removeClass("hidden");
			
		});
	});
	$("#table td").mouseleave(function(){
		$(this).parent().find(".viewmore_td").each(function(){
			var td = $(this).find("div");
			var td0 = td.eq(0);
			var td1 = td.eq(1);
			td1.addClass("hidden");
			td0.removeClass("hidden");
			
		});
	});
});