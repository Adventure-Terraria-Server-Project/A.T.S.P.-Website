// NOTE: this script requires jquery and moment.js

function autoUpdateDurationBars() {
	// Configure the time of hardmode and worldreset here by defining the weekly offset of it starting from sunday 0:00
	// (e.g. if hardmode is on wednesday, 18:00 utc put this: "3 18:00")
	const hardmodeTimeOfWeek = moment.duration("3 19:00");
	const worldResetTimeOfWeek = moment.duration("6 17:00");
	
	function updateBars()
	{
		const now = moment();
		const sundayOfTheWeek = moment(now).startOf("week").add(moment().utcOffset(), "minutes");
		const sundayOfTheNextWeek = moment(sundayOfTheWeek).add(7, "days");
		
		let hardmodeTime = moment(sundayOfTheWeek).add(hardmodeTimeOfWeek);
		let worldResetTime = moment(sundayOfTheWeek).add(worldResetTimeOfWeek);
		// time must be fixed if world reset has already happened on the same day
		if (worldResetTime.isBefore(now))
		{
			worldResetTime = moment(sundayOfTheNextWeek).add(worldResetTimeOfWeek);
			hardmodeTime = moment(sundayOfTheNextWeek).add(hardmodeTimeOfWeek);
		}

		const lastWorldResetTime = moment(worldResetTime).subtract(1, "week");
		const durationSinceReset = moment.duration(now.diff(lastWorldResetTime));
		
		const hardmodeDuration = moment.duration(hardmodeTime.diff(lastWorldResetTime));
		const worldResetDuration = moment.duration(1, "week");
		
		const hardmodeProgress = Math.min(1, durationSinceReset.asMilliseconds() / hardmodeDuration.asMilliseconds()) * 100;
		const worldResetProgress = Math.min(1, durationSinceReset.asMilliseconds() / worldResetDuration.asMilliseconds()) * 100;
		
		$("#hardmodeText").html(formatTimeAsBarString(now, hardmodeTime, "Hardmode is enabled!"));
		$("#worldResetText").html(formatTimeAsBarString(now, worldResetTime, ""));
		$("#hardmodeBar").progress({percent: hardmodeProgress});
		$("#worldResetBar").progress({percent: worldResetProgress});
	}
	
	function formatTimeAsBarString(now, time, overdueString) {
		if (now.isBefore(time))
		{
			const duration = moment.duration(time.diff(now));
			return msToTimeSpanString(duration) + " (at " + time.format("dddd HH:mm") + " in your current timezone)";
		}
		else
		{
			return overdueString;
		}
	}
	
	function msToTimeSpanString(ms) {
		const dayMs = 86400000;
		const hourMs = 3600000;
		const minuteMs = 60000;
		
		var leftMs = ms;
		var days = Math.floor(leftMs / dayMs);
		leftMs -= dayMs * days;
		var hours = Math.floor(leftMs / hourMs);
		leftMs -= hourMs * hours;
		var minutes = Math.floor(leftMs / minuteMs);

		var result = "";
		if (days == 0 && hours == 0 && minutes == 0)
			return "less than one minute!";

		if (days > 0)
			if (days == 1)
				result += "1 day ";
		else
			result += days + " days ";

		if (hours > 0)
			if (hours == 1)
				result += "1 hour ";
		else
			result += hours + " hours ";

		if (minutes > 0)
			if (minutes == 1)
				result += "1 minute ";
			else
				result += minutes + " minutes ";

		return result;
	};
	
	$(document).ready(function() {
		setInterval(updateBars, 5000);
		setTimeout(updateBars, 500);
	});
}
autoUpdateDurationBars();
