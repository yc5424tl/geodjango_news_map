// $('').addClass('');

$(document).ready(function() {
    setLayout();
    $(window).resize(function () {
        setLayout();
    })
});

setLayout = function() {
    let top_img_div = $('#top-nav-img-div');
    let top_img_inner_div = $('#top-nav-img-inner-div');
    let top_nav_img = $('#top-nav-img');
    let nav_left = $('#nav-lft');
    let nav_ctr = $('#nav-ctr');
    let nav_right = $('#nav-rgt');
    let nav_img = $('#nav-img');
    let nav = $('nav');

    if ($(window).width() < 1562) {
        nav.css('height', '24vh');
        top_img_div.css('display', 'initial');
        top_img_inner_div.css('display', 'initial');
        top_nav_img.css('display', 'initial');
        nav_ctr.css('display', 'none');
        nav_img.css('display', 'none');
        if (nav_left.hasClass('col-4')) {
            nav_left.removeClass('col-4').addClass('col-auto');
            nav_right.removeClass('col-4').addClass('col-auto');
            nar_ctr.removeClass('col').addClass('col-0');
        }
    }

    else if ($(window).width() > 1561) {
        nav.css('height', '30vh');
        top_img_div.css('display', 'none');
        top_img_inner_div.css('display', 'none');
        top_nav_img.css('display', 'none');
        nav_ctr.css('display', 'initial');
        nav_img.css('display', 'initial');
        if (nav_left.hasClass('col-auto')) {
            nav_left.removeClass('col-auto').addClass('col-4');
            nav_right.removeClass('col-auto').addClass('col-4');
            nav_ctr.removeClass('col-0').addClass('col-4');
        }
    }
};






// setLayout = function() {
//
//     let top_img_div = $('#top-nav-img-div');
//     let nav_left = $('#nav-lft');
//     let nav_ctr = $('#nav-ctr');
//     let nav_right = $('#nav-rgt');
//     let nav_img = $('#nav-img');
//
//     if (window.width() < 1562) {
//         top_img_div.show();
//         nav_ctr.hide();
//         nav_img.css('top', 0);
//         nav_img.hide();
//         if (nav_left.hasClass('col-4')) {
//             nav_right.removeClass('col-4').addClass('col');
//             nav_left.removeClass('col-4').addClass('col');
//         }
//     }
//
//     else if (window.width() > 1561) {
//         top_img_div.hide();
//         nav_ctr.show();
//         nav_img.show();
//         if (nav_img.css('top').equals(0)) {
//             nav_img.css('top', '-12vh');
//         }
//         if (nav_left.hasClass('col')) {
//             nav_right.removeClass('col').addClass('col-4');
//             nav_left.removeClass('col').addClass('col-4');
//
//         }
//     }
// };
//
// $(window).on('resize', setLayout);
// $(document).on('load', setLayout);