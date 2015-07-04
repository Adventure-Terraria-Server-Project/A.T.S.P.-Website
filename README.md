# Adventure Terraria Server Project - Website

## General
I tried to keep the code pep8 conform via the help of SublimeLinter, but I ignored the max. line-length rule...
The code is *as is* and I just removed some code I can't publish.
You need some work and dependencies to make it run.

### Installation
* Install at least Python 3.2 and VirtualEnv
* Create a virtual environment and install following Python modules via pip
 * bcrypt
 * cymysql
 * flask
 * flask-login
 * gunicorn
 * httpagentparser
 * itsdangerous
 * pillow
* Configure settings.py and conf.py to your needs
* Put bootstrap and fontawesome .css files in static/css/
* Put all the fonts of css in static/css/fonts/
* Put JQuery, bootstrap and highstock in static/js/
* Item-render are needed for the Inventory Parser. Extract the images from the game and put them in static/img/items/
* run ``gunicorn -c settings.py app:app``

### Used projects
 * [Flask]
 * [Bootstrap]
   * [custom version]
   * Removed features to keep it smaller. My own version has other modifications, too
 * [FontAwesome]
 * [Highstock]
 * Dozen of other things
 * Magic


### Fonts
  * [Blocked]
  * [Comfortaa]
  * [Harabara]
  * [Micro]

### tShock plugins
* [MessagePlugin]
* [Reports]
* [ExtendedBans]
* [Map]
* [ShortCommands]
* Custom A.T.S.P. plugins I can't share

## Features
### Main Page
* Thumbnail-Slider powered by bootstrap
 * Just throw in your full images in static/img/slider/full and the thumbnails are created automagically
* Shows the amount of players currently online
* Shows every player with his character and tooltip (*character renders aren't created with the website*)
* Shows how long it is so Hardmode is activated on the server and to World Reset. The custom.js handles these
* Shows members of the groups *newadmin*, *admin*, *superadmin*, *vip*, *vip+*, *vip++* and *vip.Something*
 * VIPs are colored depending on rank
* Some links and fancy colorful buttons :3
* Every page: Shows the users on the bottom, which were online on the website today

### Dash
* Banned items
* Messages you got with the MessagePlugin
* Depending on the logged in user and client-IP shows ban-data
* Shows staff all the unhandled /report's, use /hreport to hide them
* Player amount statistics, which are collected via a custom plugin
* Website visit-statistics, which make a huge MySQL-database load - **Take care**
* (*superadmin*) Backup filesizes, which are made and saved in the database via a bash-script

### Logs
* Only newadmin and higher
* Parses the actual log file and ServerLog.txt and seperates the content to several tabs for better readability
 * If the log-file is larger than 3000kb, log file isn't parsed

### IRC Logs
* Only newadmin and higher
* Logs of last three days from the admin channel and query of the IRC bot [kirika]

### Ban lists
* Only newadmin and higher
* Uses the database of ExtendedBans
* Character bans
* IP bans
* Shows human readable ETA if not perma-ban
* Hides unbanned entries, either via command or time-based bans

### World Map
* Only supervip, vip.Something and newadmins and higher
* World Map, generated via the Map plugin

### World Map VIP
* Only vip++
* Cropped version of the World Map, only surface

### Inventory Parser
* Only newadmin and higher
* Inventory of currently online players
* Group, IP, health and mana
* Enter a exact username to see the inventory of a offline user

### User Searcher
* Only newadmin and higher
* Search for users with a pattern, doesn't cares about case
* Clicking on a user leads you to the inventory parser, showing the inventory, health, mana and group of the player
* Results are limited to 50, to avoid possible timeouts

### MotD & Rules
* Shows motd.txt and rules.txt
* Writable for group admin and higher

### URL Shortener
* All short URLs
* Group admin and higher can directly add new short URLs on the page
* [shorturl] is a external flask application

### Avatar & Signature / Embed
* Uses character images to create everywhere-usable avatars and signatures for every player

### Ranking of Votes
* Collected votes of users in a ranking
* Votes aren't done on the website

### Old Worlds
* Download links of previous worlds
* They are added during the Apocalypse via a bash-script to the folder and database

[bootstrap]:http://getbootstrap.com/
[FontAwesome]:http://fortawesome.github.io/Font-Awesome/
[flask]:http://flask.pocoo.org/
[blocked]:http://www.dafont.com/de/blocked.font
[comfortaa]:http://www.dafont.com/de/comfortaa.font
[harabara]:http://www.dafont.com/de/harabara.font
[micro]:http://www.dafont.com/de/micro.font
[MessagePlugin]:https://github.com/Stealownz/MessagePlugin
[reports]:https://tshock.co/xf/index.php?resources/reports.69/
[ExtendedBans]:https://github.com/Stealownz/ExtendedBans
[map]:https://tshock.co/xf/index.php?resources/map.18/
[custom version]:http://getbootstrap.com/customize/?id=0f13f92733d84602050c
[shortcommands]:https://github.com/Stealownz/ShortCommands
[kirika]:https://github.com/Nama/kirika/
[shorturl]:https://gist.github.com/Nama/c318c92109c8bf5c52c9
[highstock]:http://www.highcharts.com/stock/demo/
