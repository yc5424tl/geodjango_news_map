
let preTextarea = $('#pre-textarea');

preTextarea.on('focus', () =>  {
    if($(this).text().toLowerCase().match('share your thoughts!')) {
        $(this).text('');
        $(this).css('color', 'var(--aux-accent-6)');
    }
});

preTextarea.on('focusout', () => {
    if($(this).text().match('')) {
        $(this).text('Share Your Thoughts!');
        $(this).css('color', 'var(--main-grey)');
    }
});
