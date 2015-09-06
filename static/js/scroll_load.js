var html_size = document.body.clientHeight;   // HTML content size
var view = $(window).height();                // Window height
var item = 0;
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
};
do {
    load();
    html_size = document.body.clientHeight;
}
while ( html_size <= view );
$(window).scroll(function() {
    html_size = document.body.clientHeight;
    view = $( window ).height();
    if($(this).scrollTop() >= (html_size - view)*0.90 ) {
        load();
    }
});
