// $('').addClass('');

$(window).onresize(() => {
   let win = $(this);
   let top_img_div = $('#top-nav-img-div');
   let nav_left = $('#nav-lft');
   let nav_ctr = $('#nav-ctr');
   let nav_right = $('#nav-rgt');
   let nav_img = $('#nav-img');

   if (win.width() < 1562) {
       $(top_img_div).show();
       $(nav_ctr).hide();
       $(nav_img).hide();
       if ($(nav_left).hasClass('col-4')) {
           $(nav_left).removeClass('col-4').addClass('col');
           $(nav_right).removeClass('col-4').addClass('col');
       }
   }

   if (win.width() > 1561) {
       $(top_img_div).hide();
       $(nav_ctr).show();
       $(nav_img).show();
       if($(nav_left).hasClass('col')) {
           $(nav_left).removeClass('col').addClass('col-4');
           $(nav_right).removeClass('col').addClass('col-4');
       }
   }
});