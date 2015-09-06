###############################################################################
#                                                                             #
'''More non-Database functions'''                                             #
#                                                                             #
###############################################################################
import PIL
import conf
import os
import re
import sys
import urllib.request

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from db_funcs import get_player_inv
from db_funcs import get_player_inv_sig
from db_funcs import get_user_by_name
from flask import json
from random import shuffle
from textwrap import dedent
from time import time

global recents
recents = dict()

###############################################################################
#                                                                             #
'''Thumbnail creator for Flexslider'''                                        #
#                                                                             #
###############################################################################


def sliderc():
    slider = '                            <div class="carousel-inner">'
    indicator = ''
    count = 0

    imagelist = os.listdir(conf.slider_path)
    shuffle(imagelist)
    for files in imagelist:
        if files.endswith('.jpg'):
            if not count:
                active = 'active'
                indiactive = 'class="active"'
            thumb = imageres(files)
            indicator += '                                <li data-target="#carousel" data-slide-to="%s" %s></li>\n' % (count, indiactive)
            slider += dedent('''
                             <div class="item %s">
                                 <a href="slider/full/%s" target="_blank"><img alt="Screenshot" src="slider/%s" ></a>
                             </div>
                             ''') % (active, files, thumb)
            count += 1
            active = ''
            indiactive = ''

    indicator += '                            </ol>\n'
    return indicator + slider


def imageres(imagename):
    imgpath = conf.slider_path
    if not os.path.isfile(os.path.join(imgpath, '..', 't_%s' % imagename)):
        baseheight = conf.slider_height
        img = Image.open(os.path.join(imgpath, imagename))
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        img.save(os.path.join(imgpath, '..', 't_%s' % imagename), quality=95)
    return 't_%s' % imagename


###############################################################################
#                                                                             #
'''Avatar creator'''                                                          #
#                                                                             #
###############################################################################


def avatar(user):
    im = Image.open(conf.ava.bg)
    draw = ImageDraw.Draw(im)
    # Write User Nick
    size = conf.ava.nick_size
    font = ImageFont.truetype(font=conf.ava.font, size=size)
    w, h = draw.textsize(user, font=font)
    while w >= 97:
        size -= 1
        font = ImageFont.truetype(font=conf.ava.font, size=size)
        w, h = draw.textsize(user, font=font)
    draw.text(((100 - w) / 2, 3), user, (230, 6, 6), font=font)
    # Write bottomtext
    font = ImageFont.truetype(font=conf.ava.bottomtext_font, size=conf.ava.bottomtext_size)
    bottomtext = conf.ava.bottomtext
    w, h = draw.textsize(bottomtext, font=font)
    draw.text(((100 - w) / 2, (100 - h) - 10), bottomtext, (50, 100, 10), font=font)
    # Paste Char img
    imp = Image.open('static/img/Char Renders/%s.png' % user)
    x, y = imp.size
    l, r = (int((100 - x) / 2), 25)
    x, y = (x + l, y + r)
    im.paste(imp, box=(l, r, x, y), mask=imp)
    im.save('static/img/avatars/%s.png' % user)


###############################################################################
#                                                                             #
'''Signature creator'''                                                       #
#                                                                             #
###############################################################################


def signature(user):
    user_grp = get_user_by_name(user)
    im = Image.open(conf.sig.bg)
    # Write User Nick
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font=conf.sig.nick_font, size=conf.sig.nick_size)
    w, h = draw.textsize(user, font=font)
    draw.text(((360 - w) / 2, 42), user, (0, 100, 255), font=font)
    nick_w = (360 - w) / 2
    # Paste Char img
    imp = Image.open('static/img/Char Renders/%s.png' % user)
    x, y = imp.size
    l, r = (int((360 - w) / 2) - x - 10, 27)
    x, y = (x + l, y + r)
    im.paste(imp, box=(l, r, x, y), mask=imp)
    # Write User Group
    font = ImageFont.truetype(font=conf.sig.group_font, size=conf.sig.group_size)
    group = user_grp[4].replace('vip', 'VIP').replace('default', 'Regular Player').replace('newadmin', 'Moderator').replace('admin', 'Admin').replace('superAdmin', 'Super Admin')
    w, h = draw.textsize(group, font=font)
    draw.text(((360 - w) - 10, (95 - h) - 3), group, (0, 0, 0), font=font)
    im.save('static/img/signatures/%s.png' % user)
    # Paste Inventory
    get_player_inv_sig(user, nick_w)


###############################################################################
#                                                                             #
'''Playercount, Playerlist'''                                                 #
#                                                                             #
###############################################################################


# Show on Index
def player_list():
    try:
        p_list = ''
        j_data = urllib.request.urlopen(conf.rapi_status).read().decode('utf-8')
        p_count = json.loads(j_data)
        p_list1 = p_count.get('players').split(',')
        for i in p_list1:
            p_ltemp = i.lstrip(' ')
            if os.path.exists(r'static/img/Char Renders/%s.png' % p_ltemp):
                p_list += '<span class="render" style="whitespace: nowrap"><img alt="Character Picture" title="{0}" src="Char%20Renders/{1}.png"></span>'.format(p_ltemp, p_ltemp)
            else:
                p_list += '<span class="render" style="whitespace: nowrap"><img title="%s" src="guest.png"></span>' % p_ltemp
        player = {'p_count': p_count, 'p_list': p_list}
    except:
        player = {'p_count': False, 'p_list': False}
    return player


# Show in Inventory Parser for staff
def online_invpars():
    try:
        j_data = urllib.request.urlopen(conf.rapi_players).read().decode('utf-8')
        p_list1 = json.loads(j_data).get('players')
        p_list = ''
        p_id = 0
        for i in p_list1:
            if os.path.exists(r'static/img/Char Renders/%s.png' % i['nickname']) and i['group'] != 'guest':
                p_list += dedent('''
                                 <div class="panel panel-default">
                                     <div class="panel-heading" data-toggle="collapse" data-parent="#pinv" data-target="#%s">
                                         <h4 class="panel-title">
                                             <div class="row">
                                                 <div class="col-md-6 text-center">
                                                     <img  src="Char Renders/%s.png">
                                                 </div>
                                                 <div class="col-md-6">
                                                     <p class="text-warning"><span class="text-danger glyphicon glyphicon-heart"></span> %s <span class="text-primary glyphicon glyphicon-star"></span> %s <i class="text-info fa fa-users"></i> %s</p>
                                                     <p class="text-warning"><span class="text-success glyphicon glyphicon-user"></span> %s <span class="text-success glyphicon glyphicon-globe"></span> %s</p>
                                                 </div>
                                             </div>
                                         </h4>
                                     </div>
                                     <div id="%s" class="panel-collapse collapse">
                                         <div class="panel-body">
                                             <table class="table table-bordered"><tr>%s</tr></table>
                                         </div>
                                     </div>
                                 </div>
                                 ''') % (str(p_id), i['nickname'], str(get_player_inv(i['nickname'])['health']), str(get_player_inv(i['nickname'])['mana']), i['group'], i['nickname'], i['ip'], str(p_id), str(get_player_inv(i['nickname'])['inv']))
                p_id += 1
        player = p_list
    except:
        player = False
    return player


###############################################################################
#                                                                             #
'''Parse the logs for /logs'''                                                #
#                                                                             #
###############################################################################


def parsevar(line, kword):
    msg_kwords = ("hax", "hack", "glitch", "bug", "ban", "kick", "kik", "admin", "staff", "mod", "invedit", "cheat", "dupe", "grief", "player edit", "inventory edit", "invis", "noclip", "invhealth", "client", "suspi", "spawn", "one hit", "terion", "yama", "tony", "steal", "santa", "stark", "slash", "crust", "alej", "eagle", "joffrey", "detect", "figure", "check", "notice")
    if any(word in line.lower() for word in msg_kwords):
        return '<strong><font style="color: red">' + line.replace('<', '&#60;').replace('>', '&#62;') + '</font></strong><br>'
    else:
        return line.replace('<', '&#60;').replace('>', '&#62;') + '<br>'


def parselogs():
    log = {'tshock': '', 'utils': '', 'imanager': '', 'ptrace': '', 'log': '', 'commands': '', 'slog': ''}
    serverlog = conf.serverlog
    if os.path.getsize(serverlog) < 3000000:
        with open(serverlog, 'r') as sl:
            slog = open(serverlog)
            log['slog'] += slog.read().replace('<', '&#60;').replace('>', '&#62;').replace('\n', '<br>')
    else:
        log['slog'] = '<h1 class="text-danger">Logfile too big!</h1>'
    logdir = conf.logdir
    logfile = sorted(os.listdir(logdir)).pop()
    if os.path.getsize(logdir + logfile) < 3000000:
        with open(logdir + logfile, 'r') as logf:
            for line in logf:
                try:
                    if line[22:].startswith('TShock:'):
                        log['tshock'] += parsevar(line, 'TShock')
                    elif line[22:].startswith('Utils'):
                        log['utils'] += parsevar(line, 'Utils')
                    elif line[22:].startswith('ItemManager'):
                        log['imanager'] += parsevar(line, 'ItemManager')
                    elif line[22:].startswith('PluginTrace'):
                        log['ptrace'] += parsevar(line, 'PluginTrace')
                    elif line[22:].startswith('Log'):
                        log['log'] += parsevar(line, 'Log')
                    elif line[22:].startswith('Commands'):
                        log['commands'] += parsevar(line, 'Commands')
                except:
                    pass
    else:
        log['tshock'] = '<h1 class="text-danger">Logfile too big!</h1>'
    return log


###############################################################################
#                                                                             #
'''Read the logs from kirika'''                                               #
#                                                                             #
###############################################################################


def readirclogs():
    logs = {'1': '', '2': '', '3': '', '0': ''}
    tmp_log = ''
    logpath = '/home/kirika/scripts/ybot/logs/'
    loglist = sorted(os.listdir(logpath))
    for i in range(len(loglist)):
            log = open(logpath + loglist[i])
            logs[i] = log.read()
    return logs
