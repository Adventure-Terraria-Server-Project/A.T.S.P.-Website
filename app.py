#!/usr/bin/env python
###############################################################################
#                                                                             #
'''A.T.S.P. Site Controller'''                                                #
#                                                                             #
###############################################################################
import PIL
import bcrypt
import conf
import os
import re
import urllib.request

from PIL import Image
from datetime import date
from datetime import timedelta
from db2_funcs import backup_size
from db2_funcs import donate_read
from db2_funcs import donate_save
from db2_funcs import get_old_worlds
from db2_funcs import get_visit
from db2_funcs import save_visit
from db2_funcs import shorturl_read
from db2_funcs import shorturl_save
from db_funcs import banlist
from db_funcs import dash_banned
from db_funcs import get_player_inv
from db_funcs import get_reports
from db_funcs import get_user
from db_funcs import get_user_by_name
from db_funcs import item_bans
from db_funcs import lgroups
from db_funcs import msg
from db_funcs import search_user
from db_funcs import server_stats
from flask import Flask
from flask import escape
from flask import flash
from flask import json
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask.ext.login import LoginManager
from flask.ext.login import UserMixin
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from itsdangerous import URLSafeTimedSerializer
from more_funcs import avatar
from more_funcs import online_invpars
from more_funcs import parselogs
from more_funcs import player_list
from more_funcs import readirclogs
from more_funcs import signature
from more_funcs import sliderc
from time import gmtime
from time import strftime
from time import time

'''Inits'''
app = Flask(__name__)
app.debug = conf.debug
login_manager = LoginManager()
login_manager.init_app(app)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=conf.cookie_duration)
login_manager.login_view = '/'
login_manager.setup_app(app)
app.secret_key = conf.secret_key
login_serializer = URLSafeTimedSerializer(app.secret_key)

with open('today.txt', 'w') as today:
    now = date.isoformat(date.today()), int(time())
    print(now, file=today)

name = conf.name
short_name = conf.short_name


###############################################################################
#                                                                             #
'''Shared Code which is used on every site'''                                 #
#                                                                             #
###############################################################################


def get_data(page):
    # Mobile or Desktop?
    mobiles = ('iPhone', 'IPod', 'Android', 'BlackBerry', 'Windows Phone')
    ua = str(request.user_agent)
    if any(word in ua for word in mobiles):
        mobile_user = True
    else:
        mobile_user = False

    # Get active session (Nick and Group)
    user_id_grp = get_group(current_user.get_id())
    user = user_id_grp[0]

    # Check if staff
    if user_id_grp[1] in ('newadmin', 'admin', 'superadmin'):
        user_staff = True
    else:
        user_staff = False

    # Track site visit & Get "Recent Online" List
    ip = request.environ['REMOTE_ADDR']
    referrer = request.referrer or 'No Referrer'
    recents = save_visit({'user': user, 'page': page, 'ip': ip, 'referrer': referrer, 'ua': ua, 'mobile': mobile_user})

    return {'user': user_id_grp, 'staff': user_staff, 'mobile': mobile_user, 'recents': recents}


###############################################################################
#                                                                             #
'''The front "index" page'''                                                  #
#                                                                             #
###############################################################################


@app.route('/', methods=['GET', 'POST'])
def index():
    slider = sliderc()

    # Playercount, Playerlist
    player = player_list()

    # MySQL Groups
    groups = lgroups()

    # Get User-Info and Recent Online Users
    user_data = get_data('index')

    if request.method == 'POST':
        user = User.get_by_username(request.form['username'])
        password = request.form['password'].encode('utf-8')
        hashed = user.password.encode('utf-8')
        if user and bcrypt.hashpw(password, hashed) == hashed:
            login_user(user, remember=True)
            flash('You were successfully logged in')
            return redirect(url_for('dash', _scheme='https', _external='True'))
        else:
            flash(conf.wrong_login)

    return render_template('main.tpl', user_data=user_data, name=name, p_count=player['p_count'], p_list=player['p_list'], groups=groups, slider=slider)


###############################################################################
#                                                                             #
'''Dashboard for logged in members'''                                         #
#                                                                             #
###############################################################################


@app.route('/dash')
@login_required
def dash():
    name = '%s DashBoard' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('dash')

    stats_server = server_stats()
    web_stats = get_visit()

    b_items = item_bans()
    reports = get_reports()
    backups = backup_size()

    nickban, ipban = dash_banned(user_data['user'][0], request.headers.get('X-Forward-For'))
    msgs, count = msg(user_data['user'][0])

    return render_template('dash.tpl', user_data=user_data, name=name, stats_server=stats_server, b_items=b_items, nickban=nickban, ipban=ipban, msgs=msgs, count=count, backups=backups, reports=reports, web_stats=web_stats)


###############################################################################
#                                                                             #
'''Ban-lists for staff-members'''                                             #
#                                                                             #
###############################################################################


@app.route('/bans')
@login_required
def bans():
    name = '%s Ban lists' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('bans')

    if user_data['staff']:
        bans = banlist()
        return render_template('bans.tpl', user_data=user_data, name=name, ipbans=bans['ipban'], nickbans=bans['nickban'])
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Inventory Parser for staff-members'''                                      #
#                                                                             #
###############################################################################


@app.route('/invpars', methods=['GET', 'POST'])
@login_required
def invpars():
    name = '%s Inventory Parser' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('invparser')

    inventory = None
    search_nick = None
    if request.method == 'POST':
        search_nick = request.form['nick']
    elif request.args.get('user'):
        search_nick = request.args.get('user')
    if search_nick:
        inventory = get_player_inv(search_nick)
        if not inventory:
            flash('<strong>Oh Snap!</strong> User not found.')

    if user_data['staff']:
        if search_nick:
            player = search_nick
        else:
            player = online_invpars()
        return render_template('invpars.tpl', user_data=user_data, name=name, p_list=player, inventory=inventory)
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''User Search'''                                                             #
#                                                                             #
###############################################################################


@app.route('/searchuser', methods=['GET', 'POST'])
@login_required
def suser():
    name = '%s User Searcher' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('searchuser')

    result = None
    if request.method == 'POST':
        search_nick = request.form['nick']
        result = search_user(search_nick)
        if not result:
            flash('<strong>Oh Snap!</strong> No user found.')
            return redirect(url_for('searchuser', _scheme='https', _external='True'))
    if user_data['staff']:
        return render_template('searchuser.tpl', user_data=user_data, name=name, result=result)
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Log-Parser for staff-members'''                                            #
#                                                                             #
###############################################################################


@app.route('/logs')
@login_required
def logs():
    name = '%s Logs' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('logs')

    if user_data['staff']:
        logs = parselogs()
        return render_template('logs.tpl', user_data=user_data, name=name, logs=logs)
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Logs from kirika/IRC'''                                                    #
#                                                                             #
###############################################################################


@app.route('/irclogs')
@login_required
def irclogs():
    name = '%s IRC Logs' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('irclogs')

    if user_data['staff']:
        logs = readirclogs()
        return render_template('irclogs.tpl', user_data=user_data, name=name, logs=logs)
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Edit/show /motd and /rules'''                                              #
#                                                                             #
###############################################################################


@app.route('/motd-rules')
@login_required
def motd_rules():
    name = '%s MOTD and Rules' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('motdrules')

    moru = {'rules': '', 'motd': ''}
    if user_data['user'][1] not in ['admin', 'superadmin']:
        with open(conf.rules, 'r') as rules:
            for r_line in rules:
                moru['rules'] += r_line[13:] + '<br>'
        with open(conf.motd, 'r') as motd:
            for m_line in motd:
                moru['motd'] += m_line[13:] + '<br>'
        staff = False
    else:
        with open(conf.rules, 'r') as rules:
            for r_line in rules:
                moru['rules'] += r_line
        with open(conf.motd, 'r') as motd:
            for m_line in motd:
                moru['motd'] += m_line
        staff = True
    return render_template('motdrule.tpl', user_data=user_data, name=name, moru=moru, staff=staff)


@app.route('/motd_rules', methods=['POST'])
def save():
    with open(conf.rules, 'w') as rules:
        rules.write(request.form['rules'])
    with open(conf.motd, 'w') as motd:
        motd.write(request.form['motd'])
    flash('<span class="glyphicon glyphicon-floppy-saved"></span> Files has been saved')
    return redirect(url_for('dash', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''URL-Shortener Config'''                                                    #
#                                                                             #
###############################################################################


@app.route('/shorturl')
def surl():
    name = '%s URL Shortener' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('shorturl')

    if user_data['user'][1] not in ['admin', 'superadmin']:
        staff = False
    else:
        staff = True

    urls = shorturl_read()

    return render_template('shorturl.tpl', user_data=user_data, name=name, staff=staff, url_config=urls)


@app.route('/shorturl', methods=['POST'])
def save_url():
    surl = request.form['surl']
    url = request.form['url']
    if re.compile('^\w+$').match(surl) and url:
        shorturl_save(surl, url)
    else:
        flash('Incorrect URL. Only letters, digits and _.')
    return redirect(url_for('surl', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Old Worlds'''                                                              #
#                                                                             #
###############################################################################


@app.route('/oldworlds')
def oldworlds():
    name = '%s Old Worlds' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('oldworlds')

    worlds = get_old_worlds()

    return render_template('oldworlds.tpl', user_data=user_data, name=name, worlds=worlds)


###############################################################################
#                                                                             #
'''Donate'''                                                                  #
#                                                                             #
###############################################################################


@app.route('/donate')
def donate():
    name = '%s Donate' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('donate')

    donated = donate_read()

    return render_template('donate.tpl', user_data=user_data, name=name, donated=donated)


@app.route('/donate_paypal')
@login_required
def donate_paypal():
    # Get User-Info and Recent Online Users
    user_data = get_data('donate_paypal')

    donate_save(user_data['user'][0])

    return redirect(conf.donate_link)


@app.route('/donate_fundrazr')
@login_required
def donate_fundrazr():
    # Get User-Info and Recent Online Users
    user_data = get_data('donate_fundrazr')

    donate_save(user_data['user'][0])

    return redirect(conf.donate_link2)


###############################################################################
#                                                                             #
'''World Map'''                                                               #
#                                                                             #
###############################################################################


@app.route('/world-map')
@login_required
def show_world():
    # Get User-Info and Recent Online Users
    user_data = get_data('world')

    if user_data['user'][1] == 'supervip' or user_data['staff']:
        return send_from_directory('/home/atsp/mainserver/map/', 'world-now.png')
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''World Map for VIP'''                                                       #
#                                                                             #
###############################################################################


@app.route('/world-map-vip')
@login_required
def show_world_crop():
    # Get User-Info and Recent Online Users
    user_data = get_data('worldvip')

    if user_data['user'][1] == 'vip++':
        if os.path.getmtime('files/world-now-vip.png') < time() - 600:
            wmim = Image.open('/home/atsp/mainserver/map/world-now.png')
            wmim.crop((0, 0, 8400, 800)).save('files/world-now-vip.png')
        return send_from_directory('files/', 'world-now-vip.png')
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Avatar'''                                                                  #
#                                                                             #
###############################################################################


@app.route('/avatar/<user>')
def create_ava(user):
    if os.path.exists('static/img/avatars/' + user + '.png'):
        if os.path.exists('static/img/Char Renders/' + user + '.png') and os.path.getmtime('static/img/avatars/' + user + '.png') < time() - 6000:
            avatar(user)
        return send_from_directory('static/img/avatars/', user + '.png')
    else:
        try:
            # Get active session
            user_id_grp = get_group(current_user.get_id())
            if user_data['user'][0] in [user, 'Yama']:
                avatar(user)
                return send_from_directory('static/img/avatars/', user + '.png')
        except:
            pass
    return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Signature'''                                                               #
#                                                                             #
###############################################################################


@app.route('/signature/<user>')
def create_sig(user):
    if os.path.exists('static/img/signatures/%s.png') % user:
        if os.path.exists('static/img/Char Renders/%s.png') % user and os.path.getmtime('static/img/signatures/%s.png') % user < time() - 6000:
            signature(user)
        return send_from_directory('static/img/signatures/', '%s.png') % user
    else:
        try:
            # Get active session
            user_id_grp = get_group(current_user.get_id())
            if user_data['user'][0] in [user, 'Yama']:
                signature(user)
                return send_from_directory('static/img/signatures/', user + '.png')
        except:
            pass
    return redirect(url_for('not_found', _scheme='https', _external='True'))

###############################################################################
#                                                                             #
'''View for Avatar and Signature'''                                           #
#                                                                             #
###############################################################################


@app.route('/embed')
@login_required
def embed():
    name = '%s Embed' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('embed')

    ava = 'https://yamahi.eu/avatar/%s' % user_data['user'][0]
    sig = 'https://yamahi.eu/signature/%s' % user_data['user'][0]

    return render_template('avsig.tpl', user_data=user_data, name=name, sig=sig, ava=ava)


###############################################################################
#                                                                             #
'''User logout'''                                                             #
#                                                                             #
###############################################################################


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash('You were successfully logged out')
    return redirect(url_for('index', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Get the active session to check permissions for other functions'''         #
#                                                                             #
###############################################################################


def get_group(id):
    if current_user.get_id():
        user_grp = get_user(current_user.get_id())[4]
        user_name = get_user(current_user.get_id())[1]
    else:
        user_grp = None
        user_name = 'Login'
    return user_name, user_grp


###############################################################################
#                                                                             #
'''Flask-Login thingys'''                                                     #
#                                                                             #
###############################################################################


class User(UserMixin):
    """User Class for flask-Login"""
    def __init__(self, userid, password):
        self.id = userid
        self.password = password

    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)

    @staticmethod
    def get(userid):
        try:
            userdb = get_user(userid)
            return User(userdb[0], userdb[2])
        except:
            return None

    @staticmethod
    def get_by_username(username):
        try:
            userdb = get_user_by_name(username)
            return User(userdb[0], userdb[2])
        except:
            return None


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@login_manager.token_loader
def load_token(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()

    # Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age=max_age)

    # Find the User
    user = User.get(data[0])

    # Check Password and return user or None
    if user and data[1] == user.password:
        return user
    return None


###############################################################################
#                                                                             #
'''ErrorHandler'''                                                            #
#                                                                             #
###############################################################################


def not_found_code(status):
    name = '%s 404' % conf.short_name

    # Get User-Info and Recent Online Users
    user_data = get_data('404')

    return render_template('404.tpl', user_data=user_data, name=name), status


@app.route('/404')
def not_found():
    return not_found_code(404)


@app.errorhandler(404)
def page_not_found(error):
    return not_found_code(404)


@login_manager.unauthorized_handler
def unauthorized():
    return not_found_code(401)
