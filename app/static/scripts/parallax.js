var scrollBanner = function() {

    // alert("work")
    /** Get the scroll position of the page */
    scrollPos = $(this).scrollTop();

    /** Scroll and fade out the banner text */
    $bannerText.css({
        'padding-bottom' : 30 + ( scrollPos / 3 ) + "px",
        'opacity' : 1 - ( scrollPos / 400 ),
        '-ms-filter' : 'progid:DXImageTransform.Microsoft.Alpha(Opacity=' + 1 - ( scrollPos / 400 ) + ')'
    });

    /** Scroll the background of the banner */
    $homeBanner.css({
        'top' : ( scrollPos / 2 ) + "px"
    });
};

function parallax(func) {
    $window=$(window)
    $homeBanner=$('.homeBanner')
    $bannerText=$('.bannerText')
    $window.scroll(function () {
        scrollBanner();
    })};

addLoadEvent(parallax)
