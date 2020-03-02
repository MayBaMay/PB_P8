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

  // SAVE FAVORITE
  $('.favoriteForm').submit(function(e){
    let form = $(this)
    let wachlist = $(this).hasClass("wachlist")
    e.preventDefault();
    $.ajax({
      url: "/load_favorite/", // the file to call
      type: "POST", // GET or POST
      data: $(this).serialize(),
      })
      .done(function(data) {
        let favorite_response = jQuery.parseJSON(data);
        console.log(favorite_response);
        console.log(favorite_response.substitute_id)
        console.log(favorite_response.product_id)
        console.log(favorite_response.favorite)
        let submit = form.find('button')
        if (wachlist){
          form.parent(".prodbox").remove()
        }
        else{
          if(favorite_response.favorite == true){
          submit.html("<span class='fas fa-floppy-o'></span> Retirer ce produit de mes favoris")
          }
        else{
          submit.html("<span class='fas fa-floppy-o'></span> Sauvegarder")
          }
        }

      })
    })

    $('.return').on('click', function(e){
      window.location.replace(document.referrer);
    })

    $('.load').on('click', function(e){
      let borderLoader = $('<div id="borderLoader"></div>');
      let loader = $('<div id="loader"></div>');
      loader.append(createLoader());
      borderLoader.append(loader);
      $('body').append(borderLoader);


  })

})(jQuery); // End of use strict

function createLoader(){
  return $(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto; background: rgb(255, 255, 255) none repeat scroll 0% 0%; display: block; shape-rendering: auto;" width="200px" height="200px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
  <path fill="none" stroke="#345a61" stroke-width="8" stroke-dasharray="42.76482137044271 42.76482137044271" d="M24.3 30C11.4 30 5 43.3 5 50s6.4 20 19.3 20c19.3 0 32.1-40 51.4-40 C88.6 30 95 43.3 95 50s-6.4 20-19.3 20C56.4 70 43.6 30 24.3 30z" stroke-linecap="round" style="transform:scale(0.8);transform-origin:50px 50px">
    <animate attributeName="stroke-dashoffset" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0;256.58892822265625"></animate>
  </path>`);
}
