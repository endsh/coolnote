+ function ($) {
  "use strict";

  $(function () {
    $(".search-input").focus(function(){
  		$(".search-input").animate({width:'250px'}, 150);
  	});
  	$(".search-input").blur(function(){
  		$(".search-input").animate({width:'200px'}, 150);
  	});
  	window.onscroll = function(){
  		var t = document.documentElement.scrollTop || document.body.scrollTop;
  		if (t > 10) {
  			$(".navbar-fixed-top").addClass('fixed');
  			$(".navbar-fixed-top .btn-login").addClass('active');
  		} else {
  			$(".navbar-fixed-top").removeClass('fixed');
  			$(".navbar-fixed-top .btn-login").removeClass('active');
  		}
  	}
  })
} (jQuery);
