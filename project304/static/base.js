const toggleDropdownMobile = () => {
    let hamburger = $('#dropdown-mobile');
    if (hamburger.hasClass('show')) {
        hamburger.animate({opacity:0}, 300);
        setTimeout(() =>{
            hamburger.removeClass('show');
        }, 300);
    } else {
        hamburger.addClass('show');
        hamburger.animate({opacity:1}, 300);
    }
}

$('#clickbox1').on('click', () => {
    $('#dropdown-mobile').removeClass('show');
    $('#profile-layer').fadeToggle(300);
})
$('#clickbox2').on('click', () => {
    $('#dropdown-mobile').removeClass('show');
    $('#profile-layer').fadeToggle(300);
})

$('#hamburger').on('click', () => {
    $('#profile-layer').hide();
    toggleDropdownMobile();
})