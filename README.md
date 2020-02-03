# Adventure Terraria Server Project - Website

## General
I tried to keep the code pep8 conform via the help of SublimeLinter, but I ignored the max. line-length rule...  
The code is *as is* with some unpublished things.  
You need some work and dependencies to make it run.

### Installation
* Install at least Python 3.2 and VirtualEnv
* Create a virtual environment and install following Python modules via pip (*newer and older version might run, but this is my current setup*)
 * bcrypt 2.0.0
 * cymysql 0.8.1
 * flask 0.10.1
 * flask-login 0.2.11
 * watress 1.1.0
 * httpagentparser 1.7.7
 * itsdangerous 0.24
 * pillow 2.8.1
* Configure and conf.py to your needs
* Put Semantic UI .css files in static/css/
* Put all the fonts of css in static/css/fonts/
* Put JQuery, Semantic UI, moment and highstock in static/js/
* Item-render are needed for the Inventory Parser. Extract the images from the game and put them in static/img/items/
* run ``python app.py``

### Powered by
 * [Flask]
 * [Semantic UI]
 * [Highstock]
 * [Moment]
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
* Fully mobile compatible - can be switched via "Show desktop version" (*UserAgent dependant*)
* Random background images
 * Just throw in your full images in static/img/screenshots/original and the thumbnails are created automagically
* Shows the amount of players currently online
* Shows every player with his character and tooltip (*character renders aren't created with the website*)
* Shows how long it is so Hardmode is activated on the server and to World Reset. index.js handles these
* Shows members of the groups *newadmin*, *admin*, *superadmin*, *vip*, *vip+* and *vip++*
 * VIPs are colored depending on rank
* Some links and fancy colorful buttons :3

### Dash
* Banned items
* Messages you got with the MessagePlugin
* Depending on the logged in user shows ban-data
* Shows staff all the unhandled /report's, use /hreport to hide them
* Player amount statistics, which are collected via a custom plugin
* (*superadmin*) Backup filesizes, which are made and saved in the database via a bash-script

### Ban lists
* Only newadmin and higher
* Uses the database of ExtendedBans
* Character bans
* IP bans
* Shows human readable ETA if not perma-ban
* Hides unbanned entries, either via command or time-based bans

### World Map
* Only supervip, newadmins and higher
* World Map, generated via the [Map] plugin

### Inventory Parser
* Only newadmin and higher
* Inventory of currently online players
* Group, health and mana
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

[Semantic UI]:https://semantic-ui.com/
[Moment]:https://momentjs.com/
[flask]:http://flask.pocoo.org/
[blocked]:http://www.dafont.com/de/blocked.font
[comfortaa]:http://www.dafont.com/de/comfortaa.font
[harabara]:http://www.dafont.com/de/harabara.font
[micro]:http://www.dafont.com/de/micro.font
[MessagePlugin]:https://github.com/Stealownz/MessagePlugin
[reports]:https://tshock.co/xf/index.php?resources/reports.69/
[ExtendedBans]:https://github.com/Stealownz/ExtendedBans
[map]:https://tshock.co/xf/index.php?resources/map.18/
[shortcommands]:https://github.com/Stealownz/ShortCommands
[shorturl]:https://gist.github.com/Nama/c318c92109c8bf5c52c9
[highstock]:http://www.highcharts.com/stock/demo/
