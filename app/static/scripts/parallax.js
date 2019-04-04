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

var scrollPic = function() {
    sTop = $(this).scrollTop();
    sHgt = $window.height();
    sPics = $sPics

    sPics.each(function (){
        sPic = $(this)
        sPic.css({
          'object-fit': "cover",
        })
        xImg = $(this).children("img");
        xHgt = $(this).height();
        xTop = $(this).offset().top;

        if (xTop > (sTop+sHgt)) {
            xImg.css({
              'position' : "relative",
              'top': 0 + "px",
            });
        };

        if ( xTop <= (sTop + sHgt) && xTop > (sTop+sHgt-xHgt) ) {
            xImg.css({
              'position' : "relative",
              'top': - (xHgt - (sTop + sHgt - xTop))/2  + "px",
            });
        };

        if (xTop <= (sTop+sHgt-xHgt) && xTop > sTop ) {
            xImg.css({
              'position' : "relative",
              'top': 0 + "px",
            });
        };

        if (xTop <= sTop && xTop > (sTop-xHgt) ) {
            xImg.css({
              'position' : "relative",
              'top': + (sTop - xTop)/2  + "px",
            });
        };

        if (xTop <= (xTop-xHgt)) {
            xImg.css({
              'position' : "relative",
              'top': 0 + "px",
            });
        };
    })
};

function parallax(func) {
    $window=$(window);
    $homeBanner=$('.homeBanner');
    $bannerText=$('.bannerText');
    $sPics=$('.sPic');
    $window.scroll(function () {
        scrollBanner();
        scrollPic();
    })};

addLoadEvent(parallax);
