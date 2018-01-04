var view = $(window).height();                // Window height
var item = 0;
var running = 0;
function load() {
    next_url = "/get_worlds/" + item;
    $.ajax({
        url: next_url,
        cache: false,
        async: false,
        success: function( html ) {
            $( "tbody.infinite-scroll" ).append( html );
            item += 20;
        }
    });
    running = 0;
}

// While scrolling check if the end is reached to load new entries
$(window).scroll(function() {
    html_size = $(document).height();
//    if ($(this).scrollTop() >= (html_size - view) ) {
//console.log('document - view ', (html_size - view) * 0.8 );
//console.log($(window).scrollTop());
//console.log(running);
    if ((html_size - view) * 0.8 <= $(window).scrollTop() && running == false && $("tbody").hasClass("infinite-scroll") == true) {
        running = true;
        load();
    }
});

// While for the start - till there is enough content to scroll
do {
    if ($("tbody").hasClass("infinite-scroll")) {
        load();
    } else {
        break;
    }
    html_size = $(document).height();
}
while ( html_size <= view );
