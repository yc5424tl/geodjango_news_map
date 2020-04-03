
$(document).ready(() => {
    let preTextarea = $('#pre-textarea');
    preTextarea.on({
        'focus': () => {
            if ($(this).textContent.toLowerCase().replace(`<br>`, "").trim().match('Share Your Thoughts!')) {
                $(this).textContent = "";
                $(this).css('color', '#35e8d6');
            }
        },
        'focusout': () => {
            if ($(this).textContent.replace(`<br>`, "").trim().match("")) {
                $(this).text('Share Your Thoughts!');
                $(this).css('color', '#424B54');
            }
        }}
    )
});


