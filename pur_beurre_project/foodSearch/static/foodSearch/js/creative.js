 (function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });
  //
  // let $signIn = $('#modalLogIn');
  // $('#connect').click(function(){
  //   $signIn.modal();
  // });

  // $(".join-form").submit(function(e){
  //   e.preventDefault();
  //   console.log( $( this ).serialize() );
  //   $.ajax({
  //     method:"POST",
  //     data: $(this).serialize(),
  //     url: '/ajax/',
  //   })
  // })

  /* Login form AJAX */
$('#modalLogIn').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	submitBtn.prop('disabled', true);
	$('#no-user-error').css('display', 'none');
	$('#password-error').css('display', 'none');
	e.preventDefault();
	$.ajax({
		url: "login/", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(data){
			var login_response = jQuery.parseJSON(data);
			console.log(login_response);
			if (login_response.user == "nouser"){
				$('#no-user-error').css('display', 'block');
				submitBtn.prop('disabled', false);
			}
			else if (login_response.user == "password wrong") {
				$('#password-error').css('display', 'block');
				submitBtn.prop('disabled', false);
			}
			else if ((login_response.user == "not active") && (login_response.user_phone)) {
				$('#login-modal').modal('hide');
				$('#OTP-modal').modal({backdrop:'static', keyboard:false,show:true});
				$('#verify-user-phone').html(login_response.user_phone);
				document.getElementById(formId).reset();
				submitBtn.prop('disabled', false);
			}
			else {
				if (login_response.login == "Failed") {
					alert("Invalid Login!");
				} else {
					document.getElementById(formId).reset();
					$('#login-modal').modal('hide');
					setTimeout(function() {
					location.reload();
					}, 400);
				}
			}/*./else*/
			submitBtn.prop('disabled', false);
			$('#spinner-login').css('display', 'none');
		},/* end of Success */
		error: function(data) {
			$('#loginModal').modal('hide');
			$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
		}/*  end of error */
	});/*./ajax*/
});

})(jQuery); // End of use strict
