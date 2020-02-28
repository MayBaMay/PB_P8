 (function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      let target = $(this.hash);
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
  let navbarCollapse = function() {
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

  // show modalLogIn
  $('.connection').click(function(){
    // hide other modals
    $('#modalNotConnected').modal('hide');
    $('#modalRegister').modal('hide');
    // reset modalLogIn
    let loginform = $('#loginform').attr('id');
    document.getElementById(loginform).reset();
    $('#no-user-error').css('display', 'none');
    $('#password-error').css('display', 'none');
    // show modalLogIn
    $('#modalLogIn').modal('show');
  });

  // submit modal login
  $('#loginform').submit(function(e){
    let formId = $(this).attr('id');
    let submitBtn = $(this).find('input[type=submit]');
    $('#no-user-error').css('display', 'none');
    $('#password-error').css('display', 'none');
    e.preventDefault();
    $.ajax({
      url: "/login/", // the file to call
      type: "POST", // GET or POST
      data: $(this).serialize(), // get the form data
      success: function(data){
        let login_response = jQuery.parseJSON(data);
        console.log(login_response);
        if (login_response.user == "success"){
          document.location.reload(true);
          $('#modalLogIn').modal('hide');
        }
        else if (login_response.user == "password wrong") {
          $('#password-error').css('display', 'block');
          submitBtn.prop('disabled', false);
           }
        else{
          $('#no-user-error').css('display', 'block');
          document.getElementById(formId).reset();
        }
      }
    })
  })

  $('#disconnection').click(function(){
    $('#modalLogOut').modal('show');
  });

  $('#registration').click(function(){
    $('#modalLogIn').modal('hide');
    let formId = $('#registerForm').attr('id');
    document.getElementById(formId).reset();
    $('#username-error').css('display', 'none');
    $('#modalRegister').modal('show');

  });

  $('#registerForm').submit(function(e){
    let formId = $(this).attr('id');
    let submitBtn = $(this).find('input[type=submit]');
    $('#username-error').css('display', 'none');
    e.preventDefault();
    $.ajax({
      url: "/register/", // the file to call
      type: "POST", // GET or POST
      data: $(this).serialize(), // get the form data
      success: function(data){
        let register_response = jQuery.parseJSON(data);
        console.log(register_response);
        if (register_response.user == "success"){
          document.location.reload(true);
          $('#modalRegister').modal('hide');
        }
        else if (register_response.user == "already in DB") {
          $('#username-error').css('display', 'block');
          submitBtn.prop('disabled', false);
           }
        else{
          $('#no-user-error').css('display', 'block');
        }
      }
    })
  })

  $('#NotConnected').click(function(){
    $('#modalNotConnected').modal('show');
  });

})(jQuery); // End of use strict
