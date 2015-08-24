###############################################################################
#                                                                             #
'''A.T.S.P. config file'''                                                    #
#                                                                             #
###############################################################################
debug = True
cookie_duration = 14
name = 'Adventure Terraria Server Project :: 24/7 :: ServerSideCharacter'
# Prefix of all other sites
short_name = 'A.T.S.P. ::'
secret_key = 'YorpDood'  # create with os.random()
wrong_login = '<strong>Oh Snap!</strong> Invalid credentials'

# motd.txt and rules.txt
rules = '/home/atsp/mainserver/tshock/rules.txt'
motd = '/home/atsp/mainserver/tshock/motd.txt'


# Two possibilities to donate, these are only accessable if logged in and on /donate
donate_link = 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=CX7G7883ABWQQ'
donate_link2 = 'https://fundrazr.com/campaigns/cXafe'

# Main page image slider
slider_path = 'static/img/slider/full'
slider_height = 581

# RestAPI link
rapi_status = 'http://localhost:port/status?token=tokenandshit'
rapi_players = 'http://localhost:port/V2/server/status?players=true&token=tokenandshit'

# Logs
serverlog = '/home/atsp/mainserver/ServerLog.txt'
logdir = '/home/atsp/mainserver/tshock/logs/'


# tShock DB
class tshock_db():
    ip = '127.0.0.1'
    port = 3306
    db = 'main_tshock'
    user = 'terraria'
    pw = 'terraria'


# Website DB
class website_db():
    ip = '127.0.0.1'
    port = 3306
    db = 'main_website'
    user = 'http'
    pw = 'http'


# Auto generated avatars
class ava():
    bg = 'files/ava_bg.png'
    nick_font = 'fonts/Harabara.ttf'
    bottomtext_font = 'fonts/blocked.ttf'
    bottomtext = 'A.T.S.P. Char'
    nick_size = 20
    bottomtext_size = 11


# Auto generated signatures
class sig():
    bg = 'files/sig_bg.png'
    nick_font = 'fonts/Harabara.ttf'
    nick_size = 20
    group_font = 'fonts/Comfortaa.ttf'
    group_size = 12
