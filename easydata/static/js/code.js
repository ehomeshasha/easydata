
SyntaxHighlighter.complete = function(callback){

  (function recountHighlightedElements() {
    setTimeout(function () {
      highlightedElements = $('.syntaxhighlighter');
      elementsToBeHighlighted = $("pre[class*='brush:']").length;
      if (highlightedElements.length < elementsToBeHighlighted) {
          recountHighlightedElements();
      } else {
          callback();
      }
    }, 200);
  })();

};



$(function(){
	$(document).on("mouseover", ".line", function(){
		var class_string = $(this).attr("class");
		if(class_string.indexOf("highlighted") != -1) {
			$(this).addClass("default-highlighted");
		} else {
			$(this).addClass("highlighted");
		}
		var linenum = class_string.substr(class_string.indexOf("number") + 6, 1);
		var code_info = $(this).parent().parent().parent().parent().parent().parent().parent().parent().next()
		var mark_links = code_info.find(".code_info_wrapper .mark_link")
		var mark_link = code_info.find(".code_info_wrapper[line_num='"+linenum+"'] .mark_link")
		mark_links.addClass("hidden");
		mark_link.removeClass("hidden");
	});
	
	$(document).on("mouseout", ".line", function(){
		var class_string = $(this).attr("class");
		if(class_string.indexOf("default-highlighted") == -1) {
			$(this).removeClass("highlighted");
		}
		
	});
	$(document).on("click", ".mark_link", function(){
		if($(".hide_data_uid").html() == "None") {
			alert('Please login first');
			location.href="/account/login/?next="+location.href;
		}
		//var class_string = $(this).parent().attr("class");
		var linenum = $(this).parent().attr("line_num");
		var code_id = $(this).parent().attr("code_id");
		var url = "/code/mark_post/"+code_id+'/'+linenum+'/'
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
	
	SyntaxHighlighter.complete(function(){
		$(".command_help").remove();
		$(".toolbar").addClass("no-background");
		$(".syntaxhighlighter").each(function(){
			var code_info = $(this).parent().parent().next();
			var code_body = $(this).parent().parent();
			var code_id = code_body.attr("code_id");
			
			code_info.css("height", $(this).css("height"));
			var lines = $(this).find(".line");
			//lines.append("<div class='mark_link_wrapper'><a href='javascript:;' class='mark_link'><img src='' style='width:10px;height:10px;' /></a></div>")
			for(i=1;i<=lines.length;i++) {
				code_info.append("<div class='code_info_wrapper' code_id='"+code_id+"' line_num='"+i+"'><a href='javascript:;' class='mark_link hidden'>mark</a></div>");
				var line_height = $(this).find(".number"+i).css("height");
				var code_info_wrapper = code_info.find(".code_info_wrapper[line_num='"+i+"']");
				code_info_wrapper.css("height", line_height).css("line-height", line_height);
				code_info_wrapper.append(code_body.find(".hidden_mark_view .mark_wrapper[line_num='"+i+"']").html());
			}
			
			
			
		});
		//var code_id = $(".toolbar").parent().parent().prev().attr("data-id");
		//$(".code_info").css("height", $(".code_body").css("height"));
		
		//$(".line").append('<a href="javascript:;" code_id='+code_id+' class="mark_link_text mark_link hidden" style="">MARK</a>');
		/*
		$(".mark_wrapper").each(function(){
			var line_num = $(this).attr("line_num");
			$(".number"+line_num).append($(this).html());
		});*/
	});
	
	
	//$(document).on('dblclick', '.syntaxhighlighter', function(){
	//	$(".mark_link, .mark_view").css("display", "none");
	//});
	
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
	
	$(document).on('click', '.mark_view', function(){
		var linenum = $(this).attr("line_num");
		var code_id = $(this).attr("code_id");
		var url = "/code/mark_view_line/"+code_id+'/'+linenum+'/'
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