!function(t,o,i,l){"use strict";t("#js-grid-full-width").cubeportfolio({filters:"#js-filters-full-width",loadMore:"#js-loadMore-full-width",loadMoreAction:"auto",layoutMode:"mosaic",sortToPreventGaps:!0,defaultFilter:"*",animationType:"fadeOutTop",gapHorizontal:0,gapVertical:0,gridAdjustment:"responsive",mediaQueries:[{width:1500,cols:5},{width:1100,cols:4},{width:800,cols:3},{width:480,cols:2},{width:320,cols:1}],caption:"zoom",displayType:"lazyLoading",displayTypeSpeed:100,lightboxDelegate:".cbp-lightbox",lightboxGallery:!0,lightboxTitleSrc:"data-title",lightboxCounter:'<div class="cbp-popup-lightbox-counter">{{current}} of {{total}}</div>'})}(jQuery,window,document);

function pages_function2(){

	$(".hover-effect").click(function(event) {
						var captions="https://www.youtube.com/embed/"+$(this).data("videoid");
						$(".video_idss").attr("src",captions);
					});

					$(".btn-video-play").click(function(event) {
						var captions="https://www.youtube.com/embed/"+$(this).data("videoid");
						$(".video_idss").attr("src",captions);
					});

					$(".caption-btn").click(function(event) {
						$(".text-data").html($(this).data('narration'));
					});
					$(".description-btn").click(function(event) {
						$(".text-data-desc").html($(this).data('description'));
					});
}


function pages_function1(){

	$("#wikitopbtn").click(function(){scrollToBottom('section1')});
					$("#videostopbtn").click(function(){scrollToBottom('section2')});
					$("#newstopbtn").click(function(){scrollToBottom('section3')});
					$("#imagestopbtn").click(function(){scrollToBottom('section4')});
					$("#twittertopbtn").click(function(){scrollToBottom('section5')});
					$("#wikibtn2").click(function(){scrollToBottom('section1')});
					$("#videobtn2").click(function(){scrollToBottom('section2')});
					$("#newsbtn2").click(function(){scrollToBottom('section3')});
					$("#imagebtn2").click(function(){scrollToBottom('section4')});
					$("#twitterbtn2").click(function(){scrollToBottom('section5')});
					function scrollToBottom(id){
						div_height = $("#"+id).height();
						div_offset = $("#"+id).offset().top;
						window_height = $(window).height();
						$('html,body').animate({
							scrollTop: div_offset-window_height+div_height
						},'slow');
					}

					jQuery.fn.animateAuto = function(prop, speed, callback){
						var elem, height, width;
						return this.each(function(i, el){
							el = jQuery(el), elem = el.clone().css({"height":"auto","width":"auto"}).appendTo("body");
							height = elem.css("height"),
							width = elem.css("width"),
							elem.remove();

							if(prop === "height")
								el.animate({"height":height}, speed, callback);
							else if(prop === "width")
								el.animate({"width":width}, speed, callback);
							else if(prop === "both")
								el.animate({"width":width,"height":height}, speed, callback);
						});
					}
					var clicks=0;
					$("#readmore").click(function(){
						if(clicks==0){
							clicks=1;
							$(this).text("Read Less");
							$("#content").css("height", "auto");
						}
						else{
							clicks=0;
							$(this).text("Read More");
							$("#content").css("height","400px");

						}
					});
}				