// $('').addClass('');

$(window).onresize(() => {
   let win = $(this);
   let top_img_div = $('#top-nav-img-div');
   let nav_left = $('#nav-lft');
   let nav_ctr = $('#nav-ctr');
   let nav_right = $('#nav-rgt');
   let nav_img = $('#nav-img');

   if (win.width() < 1562) {
       if ($(top_img_div).hasClass('d-none')) {
           $(top_img_div).removeClass('d-none');
       }
       if ($(nav_left).hasClass('col-4')) {
           $(nav_left).removeClass('col-4').addClass('col');
           $(nav_right).removeClass('col-4').addClass('col');
       }
       $(nav_ctr).addClass('d-none');
       $(nav_img).addClass('d-none');
   }

   if (win.width() > 1561) {
       if($(nav_ctr).hasClass('d-none')) {
           $(nav_ctr).removeClass('d-none');
           $(nav_img).removeClass('d-none');
       }
       if($(nav_left).hasClass('col')) {
           $(nav_left).removeClass('col').addClass('col-4');
           $(nav_right).removeClass('col').addClass('col-4');
       }
       $(top_img_div).addClass('d-none')
   }
});