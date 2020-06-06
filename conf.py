###############################################################################
#                                                                             #
'''A.T.S.P. config file'''                                                    #
#                                                                             #
###############################################################################


debug = True
cookie_duration = 14
name = 'Adventure Terraria Server Project'
secret_key = 'YorpDood'  # create with os.random()
wrong_login = 'Oh Snap! Invalid credentials'
vote_ranking = 'https://terraria-servers.com/api/?object=servers&element=voters&month=current&format=json&limit=5&key=akey'

# motd.txt and rules.txt
rules = '/home/tshock/rules.txt'
motd = '/home/tshock/motd.txt'


# Two possibilities to donate these are only accessable if logged in and on /donate
donate_link = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=CX7G7883ABWQQ'
donate_link2 = 'https://fundrazr.com/campaigns/cXafe'

# Main page image
screenshot_path = 'static/img/screenshots/original'

# RestAPI link
rapi_status = 'http://localhost:port/status?token=tokenandshit'
rapi_players = 'http://localhost:port/V2/server/status?players=true&token=tokenandshit'

# World map
world_map = '/home/tshock/map/'

# Character Render path
char_render = 'static/img/Char Renders/'

# Item ID files
items = 'items.csv'
prefixes = 'prefixes.csv'

# Player statistic link from terraira-servers.com
stats_link = 'https://terraria-servers.com/statistics/chart/daily/players/7/'

# tShock DB
class tshock_db():
    ip = '127.0.0.1'
    port = 3306
    db = 'mainserver'
    user = 'root'
    pw = 'root'


# Website DB
class website_db():
    ip = '127.0.0.1'
    port = 3306
    db = 'website'
    user = 'root'
    pw = 'root'


# Auto generated avatars
class ava():
    bg = 'files/ava_bg.png'
    path = 'static/img/avatars/'
    nick_font = 'fonts/Harabara.ttf'
    bottomtext_font = 'fonts/blocked.ttf'
    bottomtext = 'A.T.S.P. Char'
    nick_size = 20
    bottomtext_size = 11


# Auto generated signatures
class sig():
    bg = 'files/sig_bg.png'
    path = 'static/img/signatures/'
    nick_font = 'fonts/Harabara.ttf'
    nick_size = 20
    group_font = 'fonts/Comfortaa.ttf'
    group_size = 12
