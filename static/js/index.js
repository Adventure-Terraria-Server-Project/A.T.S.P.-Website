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
    if (dayOfWeek == 6) // Sunday?
        if (now.getUTCHours() < 21)
            daysUntilSunday = 0;
        else
            daysUntilSunday = 6;
        else
            daysUntilSunday = 6 - dayOfWeek;

    var sundayOfTheWeek = dayOfMonth + daysUntilSunday;
    var fridayOfTheWeek = sundayOfTheWeek - 2;

    var isInvalidOverride = (typeof pbars_resetTimeOverride === 'undefined' || pbars_resetTimeOverride < now);
    if (typeof pbars_hardmodeTimeOverride === 'undefined' || isInvalidOverride)
        var hardmodeDate = new Date(now.getUTCFullYear(), now.getUTCMonth(), fridayOfTheWeek, 0, 0, 0, 0);
    else
        var hardmodeDate = pbars_hardmodeTimeOverride;
    if (typeof pbars_resetTimeOverride === 'undefined' || isInvalidOverride)
        var resetDate = new Date(now.getUTCFullYear(), now.getUTCMonth(), sundayOfTheWeek, 21, 0, 0, 0);
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

    //document.getElementById("hardmodeBar").style.width = pbars_hardmodePercentage + "%";
    //document.getElementById("worldResetBar").style.width = pbars_resetPercentage + "%";

    var hardmodeTimeSpanString;
    if (pbars_hardmodePercentage == 100)
        hardmodeTimeSpanString = "Hardmode is enabled!";
    else
        hardmodeTimeSpanString = pbars_MsToTimeSpanString(timeUntilHardmodeMs);

    $("#hardmodeBar").progress({percent: pbars_hardmodePercentage});
    $("#worldResetBar").progress({percent: pbars_resetPercentage});
    document.getElementById("hardmodeText").innerHTML = hardmodeTimeSpanString;
    document.getElementById("worldResetText").innerHTML = pbars_MsToTimeSpanString(timeUntilResetMs);
}

$(document).ready( function() {
    //pbars_Refresh();>
    setInterval(pbars_Refresh, 5000);
    setTimeout(pbars_Refresh, 500);
});
