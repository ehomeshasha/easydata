
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
		var class_text = $(this).attr("class");
		if(class_text.indexOf("highlighted") != -1) {
			$(this).addClass("default-highlighted");
		} else {
			$(this).addClass("highlighted");
		}
	});
	$(document).on("mouseout", ".line", function(){
		var class_text = $(this).attr("class");
		if(class_text.indexOf("default-highlighted") == -1) {
			$(this).removeClass("highlighted");
		}
	});
	$(document).on("click", ".line", function(){
		if($(".hide_data_uid").html() == "None") {
			alert('Please login first');
			location.href="/account/login/?next="+location.href;
		}
		var class_string = $(this).attr("class");
		var linenum = class_string.substr(class_string.indexOf("number") + 6, 1);
		var code_id = $(this).parent().parent().parent().parent()
		.parent().parent().parent().prev().attr("data-id");
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