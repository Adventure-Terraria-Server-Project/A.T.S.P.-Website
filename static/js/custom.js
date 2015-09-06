function custom() {
    // ------Tooltips
    $(".btn, .irc").tooltip({'placement': 'top', 'trigger': 'hover', 'container': 'body'});
    $("img").tooltip({'placement': 'bottom', 'trigger': 'hover'});
    $("#hardmodeText, #worldResetText").tooltip({'placement': 'right', 'trigger': 'hover'});
    $(".hardmode").tooltip({'placement': 'bottom', 'trigger': 'hover', 'title' : function() { hard = Math.floor(pbars_hardmodePercentage) + " %"; return hard;}});
    $(".worldreset").tooltip({'placement': 'bottom', 'trigger': 'hover', 'title' : function() { reset = Math.floor(pbars_resetPercentage) + " %"; return reset;}});
    
    // ------bottombar Animations
    $("#bottombar").css("bottom", "0px");
    setInterval(function () {
        $("#bottombar").css("bottom", "-30px");
    },
    10000);

    // ------Move to Top
    $('#toTop').click(function() {
        $('body,html').animate({scrollTop:0},700);
    });
    $('#toBottom').click(function() {
        var p = $( "div.col-md-11" );
        $('body,html').animate({scrollTop: + $( document ).height() },700);
    });
    
    //Cookie for modal
    //var cookiearray = document.cookie.split("; ");
    //if (cookiearray.indexOf("atsp=showed") == -1)
    //{
    //  $('#mainModal').modal();
    //  var a = new Date();
    //  a = new Date(a.getTime() +1000*60*60*24*3); // 3 Days
    //  document.cookie = 'atsp=showed; expires='+a.toGMTString()+';';
    //}
}

$(document).ready( function() {
    custom();
});
