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

// ------Progress Bars
// One-Time overwrite for special times
//var pbars_lastResetTime = new Date("May 6, 2013 16:00:00");
//var pbars_hardmodeTimeOverride = new Date("May 17, 2013 16:00:00");
//var pbars_resetTimeOverride = new Date("May 19, 2013 16:00:00");

var DayMs = 86400000;
var HourMs = 3600000;
var MinuteMs = 60000;

var pbars_hardmodePercentage;
var pbars_resetPercentage;

function pbars_MsToTimeSpanString(ms) {
    var leftMs = ms;
    var days = Math.floor(leftMs / DayMs);
    leftMs -= DayMs * days;
    var hours = Math.floor(leftMs / HourMs);
    leftMs -= HourMs * hours;
    var minutes = Math.floor(leftMs / MinuteMs);

    var string = "";
    if (days == 0 && hours == 0 && minutes == 0)
        return "less than one minute remaining!";

    if (days > 0)
        if (days == 1)
            string += "1 day ";
    else
        string += days + " days ";

    if (hours > 0)
        if (hours == 1)
            string += "1 hour ";
    else
        string += hours + " hours ";

    if (minutes > 0)
        if (minutes == 1)
            string += "1 minute ";
        else
            string += minutes + " minutes ";

    string += "remaining";

    return string;
};

function pbars_Refresh() {
    var now = new Date();
    var dayOfWeek = now.getUTCDay();
    var dayOfMonth = now.getUTCDate();
    var daysUntilSunday;
    if (dayOfWeek == 0) // Sunday?
        if (now.getUTCHours() < 18)
            daysUntilSunday = 0;
        else
            daysUntilSunday = 7;
        else
            daysUntilSunday = 7 - dayOfWeek;

    var sundayOfTheWeek = dayOfMonth + daysUntilSunday;
    var fridayOfTheWeek = sundayOfTheWeek - 3;

    var isInvalidOverride = (typeof pbars_resetTimeOverride === 'undefined' || pbars_resetTimeOverride < now);
    if (typeof pbars_hardmodeTimeOverride === 'undefined' || isInvalidOverride)
        var hardmodeDate = new Date(now.getUTCFullYear(), now.getUTCMonth(), fridayOfTheWeek, 12, 0, 0, 0);
    else
        var hardmodeDate = pbars_hardmodeTimeOverride;
    if (typeof pbars_resetTimeOverride === 'undefined' || isInvalidOverride)
        var resetDate = new Date(now.getUTCFullYear(), now.getUTCMonth(), sundayOfTheWeek, 18, 0, 0, 0);
    else
        var resetDate = pbars_resetTimeOverride;

    var nowMs = now.getTime() + (now.getTimezoneOffset() * MinuteMs);
    var timeUntilHardmodeMs = hardmodeDate.getTime() - nowMs;
    var timeUntilResetMs = resetDate.getTime() - nowMs;

    if (typeof pbars_lastResetTime === 'undefined' || isInvalidOverride) {
        pbars_hardmodePercentage = Math.min(100 - ((timeUntilHardmodeMs / (DayMs * 5)) * 100), 100);
        pbars_resetPercentage = Math.min(100 - ((timeUntilResetMs / (DayMs * 7)) * 100), 100);
    } else {
        pbars_hardmodePercentage = Math.min(100 - ((timeUntilHardmodeMs / (hardmodeDate.getTime() - pbars_lastResetTime.getTime())) * 100), 100);
        pbars_resetPercentage = Math.min(100 - ((timeUntilResetMs / (resetDate.getTime() - pbars_lastResetTime.getTime())) * 100), 100);
    }
    
    document.getElementById("hardmodeBar").style.width = pbars_hardmodePercentage + "%";
    document.getElementById("worldResetBar").style.width = pbars_resetPercentage + "%";

    var hardmodeTimeSpanString;
    if (pbars_hardmodePercentage == 100)
        hardmodeTimeSpanString = "Hardmode is enabled!";
    else
        hardmodeTimeSpanString = pbars_MsToTimeSpanString(timeUntilHardmodeMs);
    
    document.getElementById("hardmodeText").innerHTML = hardmodeTimeSpanString;
    document.getElementById("worldResetText").innerHTML = pbars_MsToTimeSpanString(timeUntilResetMs);
}

$(document).ready( function() {
    //pbars_Refresh();>
    setInterval(pbars_Refresh, 5000);
    setTimeout(pbars_Refresh, 500);
    custom();
});
