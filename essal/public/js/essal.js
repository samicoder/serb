


frappe.ready(function() {


   $('.register-form').on('submit', function(e){

         e.preventDefault();
  });

   $(window).on("hashchange", function() {

       if(["#signup"].indexOf(window.location.hash)!= -1){

            $('[data-path="login"] .nav-login-btn').removeClass('hide')
        }
    });

     var price_slider = $("#users-no-slider").slider();
      $("#users-no-slider").on("slide", function(slideEvt) {
        $("#users-no-slider-val").val(slideEvt.value);
      });


    /**
   $("li[data-label='المميزات'] > a").click(function(e) {
       e.preventDefault();
       console.log('clicked')
      scrollToAnchor('features');
   });
   **/


   function scrollToAnchor(aid){
       var aTag = $("a[name='"+ aid +"']");
       $('html,body').animate({scrollTop: aTag.offset().top},'slow');
   }



   $( ".month-plan" ).on( "click", function( event ) {
       var me = this;
      //event.preventDefault();
        $( this ).addClass( "plan-active" );
        $(".year-plan").removeClass("plan-active")
        $(".startup-plan").removeClass("plan-active")

    });
    $( ".year-plan" ).on( "click", function( event ) {
        var me = this;
      //event.preventDefault();
        $( this ).addClass( "plan-active" );
        $(".month-plan").removeClass("plan-active")
        $(".startup-plan").removeClass("plan-active")

    });
     $( ".startup-plan" ).on( "click", function( event ) {
        var me = this;
      //event.preventDefault();
        $( this ).addClass( "plan-active" );
        $(".month-plan").removeClass("plan-active")
        $(".year-plan").removeClass("plan-active")

    });


    $("#users-no-slider").on("slide", function(slideEvt) {

        $("#users-no-slider-val").val(slideEvt.value);
        getPriceValue(slideEvt.value)

    });

    $('#users-no-slider-val').on('input',function(e){

        console.log($(this).val())

        var input_val = parseInt($(this).val()?$(this).val():"1")
         if(input_val<1){
            $(this).val("1")
            input_val = 1;
        }
        if(input_val>30){
            $(this).val("30")
            input_val = 30;
        }
        price_slider.slider('setValue',input_val )
        getPriceValue(input_val)
    });




});

var getPriceValue = function(users_no){

        if (!users_no){
            users_no = 1
        }

        var month_price = users_no * 20;
        var year_price = 20 *12*users_no;

        if (users_no % 3 ==0){
            month_price = users_no * 10;
            year_price = 10 *12*users_no;
        }
        $('.month-plan .total-price').text(month_price)


        var price_without_discount = year_price
        var year_price = price_without_discount - (0.1 * price_without_discount)
        $('.year-plan .total-price').text( year_price)

        $('.year-discount .discount-value').text(0.1 * price_without_discount)


        var price_without_discount = year_price
        var year_price = price_without_discount - (0.1 * price_without_discount)
        $('.year-plan .total-price').text( year_price)

        $('.year-discount .discount-value').text(0.1 * price_without_discount)

        /* Subscription */
        var link_month = document.getElementById("subscribe-monthly").href;
        var link_year = document.getElementById("subscribe-year").href;

        num_m = "month" + link_month.split('month')[1];
        link_month = link_month.replace(num_m, "month" + month_price);

        num_y = "year" + link_year.split('year')[1];
        link_year = link_year.replace(num_y, "year" + year_price);

        document.getElementById("subscribe-monthly").href = link_month;
        document.getElementById("subscribe-year").href = link_year;

}

