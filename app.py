#!/usr/bin/env python
###############################################################################
#                                                                             #
'''A.T.S.P. Site Controller'''                                                #
#                                                                             #
###############################################################################


import bcrypt
import re
import conf
import os
import time
from datetime import timedelta
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from flask_assets import Environment
from flask_optimize import FlaskOptimize
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from itsdangerous import URLSafeTimedSerializer
from waitress import serve

from db2_funcs import backup_size
from db2_funcs import donate_read
from db2_funcs import donate_save
from db2_funcs import get_old_worlds
from db2_funcs import shorturl_read
from db2_funcs import shorturl_save
from db_funcs import banlist
from db_funcs import dash_banned
from db_funcs import get_login
from db_funcs import get_player_inv
from db_funcs import get_reports
from db_funcs import item_bans
from db_funcs import lgroups
from db_funcs import msg
from db_funcs import search_user
from db_funcs import group_permissions
from more_funcs import *

'''Inits'''
app = Flask(__name__)
app.debug = conf.debug
login_manager = LoginManager()
login_manager.init_app(app)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=conf.cookie_duration)
login_manager.login_view = '/'
login_manager.setup_app(app)
assets = Environment(app)
assets.init_app(app)
app.config['ASSETS_DEBUG'] = False
flask_optimize = FlaskOptimize()
app.secret_key = conf.secret_key
login_serializer = URLSafeTimedSerializer(app.secret_key)

name = conf.name


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

    votes = voters()

    # Get active session (Nick and Group)
    user_id_grp = get_group(current_user.get_id())

    # Check if staff
    if user_id_grp[1] in ('newadmin', 'admin', 'admin+', 'superadmin'):
        user_staff = True
    else:
        user_staff = False

    return {'user': user_id_grp, 'staff': user_staff, 'mobile': mobile_user, 'votes': votes}


###############################################################################
#                                                                             #
'''The front "index" page'''                                                  #
#                                                                             #
###############################################################################


@app.route('/', methods=['GET', 'POST'])
@flask_optimize.optimize(cache=False)
def index():
    image = banner_image()

    # Playerlist
    player = player_list()

    # Groups
    groups = lgroups()

    # Get User-Info and Recent Online Users
    user_data = get_data('index')

    if request.method == 'POST':
        user = User.get_login(request.form['username'])
        password = request.form['password'].encode('utf-8')
        if user:
            hashed = user.password.encode('utf-8')
            if user and bcrypt.hashpw(password, hashed) == hashed:
                login_user(user, remember=True)
                flash('You were successfully logged in')
                return redirect(url_for('dash', _scheme='https', _external='True'))
            else:
                flash(conf.wrong_login)
        else:
            flash(conf.wrong_login)

    return render_template('index.html', user_data=user_data, name=name, player_list=player, groups=groups, image=image)


###############################################################################
#                                                                             #
'''Dashboard for logged in members'''                                         #
#                                                                             #
###############################################################################


@app.route('/dash')
@login_required
@flask_optimize.optimize(cache=False)
def dash():
    # Get User-Info and Recent Online Users
    user_data = get_data('dash')

    banned_items = item_bans()

    reports = None
    backups = None
    permissions = None
    if user_data['staff']:
        reports = get_reports()
    if user_data['user'][1] == 'superadmin':
        backups = backup_size()
        permissions = group_permissions()

    bans = dash_banned(user_data['user'][0])
    msgs = msg(user_data['user'][0])

    return render_template('dash.html', user_data=user_data, name=name, banned_items=banned_items, bans=bans, msgs=msgs, backups=backups, reports=reports, permissions=permissions, stats_link=conf.stats_link)


###############################################################################
#                                                                             #
'''Ban-lists for staff-members'''                                             #
#                                                                             #
###############################################################################


@app.route('/bans')
@login_required
@flask_optimize.optimize(cache=False)
def bans():
    # Get User-Info and Recent Online Users
    user_data = get_data('bans')

    if user_data['staff']:
        bans = banlist()
        return render_template('bans.html', user_data=user_data, name=name, ipbans=bans['ipban'], nickbans=bans['nickban'])
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Inventory Parser for staff-members'''                                      #
#                                                                             #
###############################################################################


@app.route('/invpars')
@login_required
@flask_optimize.optimize(cache=False)
def invpars():
    # Get User-Info and Recent Online Users
    user_data = get_data('invparser')

    if user_data['staff'] and request.args.get('user'):
        search_nick = request.args.get('user')
        inv = get_player_inv(search_nick)
        if not inv:
            flash('Oh Snap! User not found.')
            return redirect(url_for('searchuser', _scheme='https', _external='True'))
        else:
            player = search_nick
            return render_template('invpars.html', user_data=user_data, name=name, p_list=player, inv=inv)
    return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''User Search'''                                                             #
#                                                                             #
###############################################################################


@app.route('/searchuser', methods=['GET', 'POST'])
@login_required
@flask_optimize.optimize(cache=False)
def searchuser():
    # Get User-Info and Recent Online Users
    user_data = get_data('searchuser')

    result = None
    if request.method == 'POST':
        search_nick = request.form['nick']
        result = search_user(search_nick)
        if not result:
            flash('Oh Snap! No user found.')
            return redirect(url_for('searchuser', _scheme='https', _external='True'))
    if user_data['staff']:
        return render_template('searchuser.html', user_data=user_data, name=name, result=result)
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Edit/show /motd and /rules'''                                              #
#                                                                             #
###############################################################################


@app.route('/motd-rules')
@flask_optimize.optimize(cache=False)
def motd_rules():
    # Get User-Info and Recent Online Users
    user_data = get_data('motdrules')

    moru = {'rules': list(), 'motd': list()}
    if user_data['user'][1] not in ['admin', 'superadmin']:
        with open(conf.rules, 'r') as rules:
            for r_line in rules:
                moru['rules'].append(r_line[13:])
        with open(conf.motd, 'r') as motd:
            for m_line in motd:
                moru['motd'].append(m_line[13:])
        staff = False
    else:
        with open(conf.rules, 'r') as rules:
            for r_line in rules:
                moru['rules'].append(r_line)
        with open(conf.motd, 'r') as motd:
            for m_line in motd:
                moru['motd'].append(m_line)
        staff = True
    return render_template('motdrule.html', user_data=user_data, name=name, moru=moru, staff=staff)


@app.route('/motd_rules', methods=['POST'])
def save():
    with open(conf.rules, 'w') as rules:
        rules.write(request.form['rules'].replace('\r', ''))
    with open(conf.motd, 'w') as motd:
        motd.write(request.form['motd'].replace('\r', ''))
    flash('Files has been saved')
    return redirect(url_for('dash', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''URL-Shortener Config'''                                                    #
#                                                                             #
###############################################################################


@app.route('/shorturl')
@flask_optimize.optimize(cache=False)
def surl():
    # Get User-Info and Recent Online Users
    user_data = get_data('shorturl')

    if user_data['user'][1] not in ['admin', 'superadmin']:
        staff = False
    else:
        staff = True

    urls = shorturl_read()

    return render_template('shorturl.html', user_data=user_data, name=name, staff=staff, url_config=urls)


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
@flask_optimize.optimize(cache=False)
def oldworlds():
    # Get User-Info and Recent Online Users
    user_data = get_data('oldworlds')

    return render_template('oldworlds.html', user_data=user_data, name=name)


@app.route('/get_worlds/<int:item>')
@flask_optimize.optimize(cache=False)
def getworlds(item):
    worlds = get_old_worlds(item)
    return render_template('oldworlds_item.html', worlds=worlds)


###############################################################################
#                                                                             #
'''Donate'''                                                                  #
#                                                                             #
###############################################################################


@app.route('/donate')
@flask_optimize.optimize(cache=False)
def donate():
    # Get User-Info and Recent Online Users
    user_data = get_data('donate')

    donated = None
    if user_data['staff']:
        donated = donate_read()

    return render_template('donate.html', user_data=user_data, name=name, donated=donated)


@app.route('/donate_paypal')
@login_required
@flask_optimize.optimize(cache=False)
def donate_paypal():
    # Get User-Info and Recent Online Users
    user_data = get_data('donate_paypal')

    donate_save(user_data['user'][0])

    return redirect(conf.donate_link)


@app.route('/donate_fundrazr')
@login_required
@flask_optimize.optimize(cache=False)
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
    user_data = get_data('world-map')

    if user_data['user'][1] in ['vip', 'vip+', 'vip++', 'supervip', 'builder'] or user_data['staff']:
        return send_from_directory(conf.world_map, 'world-now.png')
    else:
        return redirect(url_for('not_found', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''Avatar'''                                                                  #
#                                                                             #
###############################################################################


@app.route('/avatar/<user>')
def create_ava(user):
    if os.path.exists(os.path.join(conf.ava.path, '{0}.png'.format(user))):
        if os.path.exists(os.path.join(conf.char_render, '{0}.png'.format(user))) and os.path.getmtime(os.path.join(conf.ava.path, '{0}.png'.format(user))) < time.time() - 6000:
            avatar(user)
        return send_from_directory(conf.ava.path, '{0}.png'.format(user))
    else:
        try:
            # Get active session
            user_id_grp = get_group(current_user.get_id())
            if user_id_grp[0] in [user, 'Yama']:
                avatar(user)
                return send_from_directory(conf.ava.path, '{0}.png'.format(user))
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
    if os.path.exists(os.path.join(conf.sig.path, '{0}.png'.format(user))):
        if os.path.exists(os.path.join(conf.char_render, '{0}.png'.format(user))) and os.path.getmtime(os.path.join(conf.sig.path, '{0}.png'.format(user))) < time.time() - 6000:
            signature(user)
        return send_from_directory(conf.sig.path, '{0}.png'.format(user))
    else:
        try:
            # Get active session
            user_id_grp = get_group(current_user.get_id())
            if user_id_grp[0] in [user, 'Yama']:
                signature(user)
                return send_from_directory(conf.sig.path, '{0}.png'.format(user))
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
@flask_optimize.optimize(cache=False)
def embed():
    # Get User-Info and Recent Online Users
    user_data = get_data('embed')

    create_ava(user_data['user'][0])
    create_sig(user_data['user'][0])

    ava = url_for('create_ava', _scheme='https', _external='True', user=user_data['user'][0])
    sig = url_for('create_sig', _scheme='https', _external='True', user=user_data['user'][0])

    return render_template('avsig.html', user_data=user_data, name=name, sig=sig, ava=ava)


###############################################################################
#                                                                             #
'''Privacy Policy'''                                                          #
#                                                                             #
###############################################################################


@app.route('/privacy-policy')
def policy():
    # Get User-Info and Recent Online Users
    user_data = get_data('policy')

    return render_template('policy.html', user_data=user_data, name=name)


###############################################################################
#                                                                             #
'''User logout'''                                                             #
#                                                                             #
###############################################################################


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You were successfully logged out')
    return redirect(url_for('index', _scheme='https', _external='True'))


###############################################################################
#                                                                             #
'''robots.txt'''                                                              #
#                                                                             #
###############################################################################


@app.route('/robots.txt')
def robots():
    return send_from_directory('static/', 'robots.txt')


###############################################################################
#                                                                             #
'''Get the active session to check permissions for other functions'''         #
#                                                                             #
###############################################################################


def get_group(id):
    active_user = current_user.get_id()
    if active_user:
        userdb = get_user(active_user)
        user_name = userdb[0]
        user_grp = userdb[1]
    else:
        user_grp = None
        user_name = None
    return user_name, user_grp


###############################################################################
#                                                                             #
'''Flask-Login thingys'''                                                     #
#                                                                             #
###############################################################################


class User(UserMixin):
    '''User Class for flask-Login'''
    def __init__(self, userid, password):
        self.id = userid
        self.password = password

    def get_auth_token(self):
        '''Encode a secure token for cookie'''
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)

    @staticmethod
    def get(userid):
        try:
            userdb = get_user(userid)
            return User(userdb[0], userdb[1])
        except:
            return None

    @staticmethod
    def get_login(username):
        try:
            userdb = get_login(username)
            return User(userdb[0], userdb[1])
        except:
            return None


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


###############################################################################
#                                                                             #
'''ErrorHandler'''                                                            #
#                                                                             #
###############################################################################


def not_found_code(status):
    # Get User-Info and Recent Online Users
    user_data = get_data('404')

    return render_template('404.html', user_data=user_data, name=name), status


@app.route('/404')
@flask_optimize.optimize(cache=False)
def not_found():
    return not_found_code(404)


@app.errorhandler(404)
def page_not_found(error):
    return not_found_code(404)


@login_manager.unauthorized_handler
def unauthorized():
    return not_found_code(401)


if __name__ == '__main__':
    serve(app, port=8010, threads=10)
