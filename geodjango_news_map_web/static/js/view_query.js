
let preTextarea = $('#pre-textarea');

preTextarea.on('focus', () =>  {
    if($(this).textContent.toLowerCase().replace(`<br>`, "").trim().match('share your thoughts!')) {
        $(this).textContent = "";
        $(this).css('color', '#35e8d6');
    }
});

preTextarea.on('focusout', () => {
    if($(this).textContent.replace(`<br>`, "").trim().match("")) {
        $(this).text('Share Your Thoughts!');
        $(this).css('color', '#424B54');
    }
});