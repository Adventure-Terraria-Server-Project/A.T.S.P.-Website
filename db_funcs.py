###############################################################################
#                                                                             #
'''tShock Database-connection-related features'''                             #
#                                                                             #
###############################################################################
import PIL
import csv
import cymysql
import os
import sys
import urllib.request

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from conf import tshock_db
from datetime import timedelta
from multiprocessing import Event
from multiprocessing import JoinableQueue
from multiprocessing import Process
from multiprocessing import Queue
from time import time

db_host = tshock_db.ip
db_port = tshock_db.port
db = tshock_db.db
db_user = tshock_db.user
db_pw = tshock_db.pw


###############################################################################
#                                                                             #
'''Databse-connect and close'''                                               #
#                                                                             #
###############################################################################


def db_con():
    conn = cymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pw, db=db)
    cur = conn.cursor()
    return conn, cur


def db_close(conn, cur):
    cur.close()
    conn.close()


###############################################################################
#                                                                             #
'''Login thingy with tShock DB'''                                             #
#                                                                             #
###############################################################################


# Requesting username with the ID
def get_user(id):
    conn, cur = db_con()
    cur.execute("SELECT * FROM `Users` WHERE `id` = %s LIMIT 1", (id))
    user = cur.fetchone()
    db_close(conn, cur)
    return user


# Requesting ID with the username
def get_user_by_name(username):
    conn, cur = db_con()
    cur.execute("SELECT * FROM `Users` WHERE `Username` = %s LIMIT 1", (username))
    user = cur.fetchone()
    db_close(conn, cur)
    return user


###############################################################################
#                                                                             #
'''Server User Stats in Dash'''                                               #
#                                                                             #
###############################################################################


def server_stats():
    conn, cur = db_con()
    totaluser = []
    cur.execute("SELECT * FROM `Utils_ServerStatistics`")
    for r in cur.fetchall():
        totaluser.append([r[0] * 1000, r[1]])
    db_close(conn, cur)
    return totaluser


###############################################################################
#                                                                             #
'''Banlists'''                                                                #
#                                                                             #
###############################################################################


def banlist():
    conn, cur = db_con()
    ipban = ''
    nickban = ''
    cur.execute("SELECT * FROM `BannedIP`")
    for r in cur.fetchall():
        btime = r[2] - time()
        if r[2] == 0:
            ipban += '<tr><td>%s</td><td>%s</td><td>%s</td><td></td></tr>' % (r[0], r[3], r[4])
        elif r[2] > time():
            ipban += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (r[0], r[3], r[4], format_timedelta(timedelta(seconds=btime)))

    cur.execute("SELECT * FROM `BannedPlayer`")
    for r in cur.fetchall():
        btime = r[2] - time()
        if r[2] == 0:
            nickban += '<tr><td>%s</td><td>%s</td><td>%s</td><td></td></tr>' % (r[0], r[3], r[4])
        elif r[2] > time():
            nickban += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (r[0], r[3], r[4], format_timedelta(timedelta(seconds=btime)))

    db_close(conn, cur)
    return {'ipban': ipban, 'nickban': nickban}


def dash_banned(user, ip):
    conn, cur = db_con()
    ipban = ''
    nickban = ''
    cur.execute("SELECT * FROM `BannedPlayer` WHERE `Player` = %s", (user))
    for r in cur.fetchall():
        btime = r[2] - time()
        if r[2] == 0:
            nickban += '<tr><td>%s</td><td>%s</td><td>%s</td><td>PermaBan</td></tr>' % (r[0], r[3], r[4])
        elif r[2] > time():
            nickban += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (r[0], r[3], r[4], format_timedelta(timedelta(seconds=btime)))
    cur.execute("SELECT * FROM `BannedIP` WHERE `IP` = '%s'", (ip))
    for r in cur.fetchall():
        btime = r[2] - time()
        if r[2] == 0:
            ipban += '<tr><td>%s</td><td>%s</td><td>%s</td><td>PermaBan</td></tr>' % (r[0], r[3], r[4])
        elif r[2] > time():
            ipban += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (r[0], r[3], r[4], format_timedelta(timedelta(seconds=btime)))

    db_close(conn, cur)
    return nickban, ipban


# Format the ETA to a good readable format
def format_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%sd %sh %sm %ss' % (td.days, hours, minutes, seconds)


###############################################################################
#                                                                             #
'''Get offline Messages'''                                                    #
#                                                                             #
###############################################################################


def msg(user):
    conn, cur = db_con()
    msgs = ''
    count = 0
    cur.execute("SELECT * FROM `MessagePlugin` WHERE `mailTo` = %s", (user))
    for r in cur.fetchall():
        if r[5] == 0:
            msgs += '''<div class="panel panel-warning">
                            <div class="panel-heading"><i class="fa fa-share"></i> %s</div>
                            <div class="panel-body">%s</div>
                        </div>
''' % (r[1], r[3])
            count += 1

    db_close(conn, cur)
    return msgs, count


###############################################################################
#                                                                             #
'''Get banned Items'''                                                        #
#                                                                             #
###############################################################################


def item_bans():
    conn, cur = db_con()
    b_items = ''
    item_count = 0
    cur.execute("SELECT `ItemName` FROM `ItemBans`")
    for r in cur.fetchall():
        if item_count == 4:
            b_items += '</tr><tr>'
            item_count = 0
        b_items += '<td>%s</td>' % r[0]
        item_count += 1
    db_close(conn, cur)
    return b_items


###############################################################################
#                                                                             #
'''Reports'''                                                                 #
#                                                                             #
###############################################################################


def get_reports():
    conn, cur = db_con()
    cur.execute('SELECT * FROM `Reports`')
    reports = ''
    for r in cur.fetchall():
        userID = get_user(r[1])
        reportedID = get_user(r[2])
        if r[5] != 2:
            reports += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (r[0], userID[1], reportedID[1], r[3])
    return reports


###############################################################################
#                                                                             #
'''Votes'''                                                                   #
#                                                                             #
###############################################################################


def vote(user):
    conn, cur = db_con()
    cur.execute('SELECT `points` FROM `votes` WHERE `user` = %s', (user))
    user_vote = cur.fetchone()
    if user_vote:
        cur.execute('UPDATE `votes` SET points = points + 1, totalpoints = totalpoints + 1, time = UNIX_TIMESTAMP() WHERE `user` = %s', (user))
    else:
        cur.execute('INSERT INTO `votes` (`time`, `user`, `totalpoints`, `points`) VALUES (UNIX_TIMESTAMP(), %s, 1, 1)', (user))
    conn.commit()
    db_close(conn, cur)


def get_votes():
    conn, cur = db_con()
    cur.execute('SELECT `user`, `totalpoints` FROM `votes` ORDER BY `totalpoints` DESC')
    nicks = ''
    for r in cur.fetchall():
        nicks += '<dt>%s</dt><dd>%s</dd>' % (r[1], r[0])
    return nicks


def get_points(user):
    conn, cur = db_con()
    cur.execute('SELECT `points` FROM `votes` WHERE `user` = %s', (user))
    points = cur.fetchone()
    if points:
        points = points[0]
    else:
        points = None
    return points


###############################################################################
#                                                                             #
'''Search for Users'''                                                        #
#                                                                             #
###############################################################################


def search_user(user):
    conn, cur = db_con()
    search = '%' + user + '%'
    cur.execute('SELECT `Username` FROM `Users` WHERE `Username` LIKE %s LIMIT 50', (search))
    results = '<div class="col-md-2">'
    count = 0
    for r in cur.fetchall():
        results += '<a href="/invpars?user=%s">%s</a><br>' % (r[0], r[0])
        count += 1
        if count == 10:
            results += '</div><div class="col-md-2">'
            count = 0
    results += '</div>'
    return results


###############################################################################
#                                                                             #
'''Get Player Inventory'''                                                    #
#                                                                             #
###############################################################################


def get_player_inv(player):
    user_db = get_user_by_name(player)
    if user_db:
        conn, cur = db_con()
        cur.execute('SELECT * FROM `tsCharacter` WHERE `Account` = %s LIMIT 1', (user_db[0]))
        user_info = cur.fetchone()
        user_inv = inv_pars(user_info[5])
        cur.execute('SELECT `Usergroup` FROM `Users` WHERE `ID` = %s', (user_info[0]))
        group = cur.fetchone()
        db_close(conn, cur)
        return {'inv': user_inv, 'health': user_info[2], 'mana': user_info[4], 'group': group[0]}


def inv_pars(inventorystring):
    inventoryentries = inventorystring.split('~')
    inv = ''
    count_inv = 0
    count_row = 0
    count_acc = 0
    items = dict()
    prefixes = dict()

    with open('items.tsv') as itemsfile:
        itemsreader = csv.reader(itemsfile, delimiter=',', quotechar='"')
        for row in itemsreader:
            items.update({row[0]: {'name': row[1]}})

    with open('prefixes.tsv') as prefixfile:
        prefixreader = csv.reader(prefixfile, delimiter='\t', quotechar='"')
        for row in prefixreader:
            prefixes.update({row[0]: {'name': row[1]}})

    for row in inventoryentries:
        itemid, amount, prefixid = row.split(',')
        if count_row < 5:
            if count_inv == 10:
                inv += '</tr><tr>'
                count_inv = 0
                count_row += 1
        elif count_row >= 8:
            if count_inv == 8:
                inv += '</tr><tr>'
                count_inv = 0
        elif count_row == 7:
            if count_inv == 1:
                inv += '</tr><tr>'
                count_inv = 0
                count_row += 1
        elif count_row >= 5:
            if count_inv == 4:
                inv += '</tr><tr>'
                count_inv = 0
                count_row += 1

        if itemid in items.keys():
            inv += '<td><img title="%s%s" src="items/Item_%s.png"><span class="badge">%s</span></td>' % (prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount)
        else:
            inv += '<td></td>'
        count_inv += 1

    return inv


def get_player_inv_sig(player, nick_pos):
    user_db = get_user_by_name(player)
    conn, cur = db_con()
    cur.execute("SELECT * FROM `tsCharacter` WHERE `Account` = %s LIMIT 1", (user_db[0]))
    user_info = cur.fetchone()
    user_inv = inv_pars(user_info[5])
    db_close(conn, cur)
    return inv_pars_sig(user_info[5], player, nick_pos, user_info)


def inv_pars_sig(inventorystring, user, nick_pos, user_info):
    inventoryentries = inventorystring.split('~')
    inv = ''
    items = dict()
    prefixes = dict()

    with open('items.tsv') as itemsfile:
        itemsreader = csv.reader(itemsfile, delimiter=',', quotechar='"')
        for row in itemsreader:
            items.update({row[0]: {'name': row[1]}})

    with open('prefixes.tsv') as prefixfile:
        prefixreader = csv.reader(prefixfile, delimiter='\t', quotechar='"')
        for row in prefixreader:
            prefixes.update({row[0]: {'name': row[1]}})

    im_sig = Image.open('static/img/signatures/%s.png') % user
    # Write User HP
    draw = ImageDraw.Draw(im_sig)
    font = ImageFont.truetype(font='fonts/Comfortaa.ttf', size=12)
    w, h = draw.textsize('%s HP', font=font) % str(user_info[2])
    draw.text(((360 - w) - 10, 69), '%s HP', (0, 0, 0), font=font) % str(user_info[2])
    count = 0
    w = int(nick_pos) - 15
    for row in inventoryentries:
        itemid, amount, prefixid = row.split(',')
        im = Image.open('static/img/items/Item_%s.png') % itemid
        im.thumbnail((15, 15), Image.ANTIALIAS)
        w = w + 17
        im_sig.paste(im, (w, 68), mask=im)
        count += 1
        if count == 5:
            break
    im_sig.save('static/img/signatures/%s.png') % user


###############################################################################
#                                                                             #
'''Playergroups from MySQL to show VIPs and staff'''                          #
#                                                                             #
###############################################################################


def lgroups():
    conn, cur = db_con()
    '''List groups with players from MySQL DB'''
    nickcount = 0
    viplist = ''
    g_colors = {'vip': '#3ec0ff', 'vip+': '#35ab75', 'vip++': '#ff9c00', 'supervip': '#467dff'}
    cur.execute("SELECT * FROM `Users` WHERE `Usergroup` LIKE '%vip%'")
    for r in cur.fetchall():
        if nickcount == 4:
            viplist += '</tr><tr>'
            nickcount = 0
        viplist += '<td style="color:%s">%s</td>' % (g_colors.get(r[4], '#467dff'), r[1])
        nickcount += 1
    if nickcount != 4:
        while nickcount < 4:
            viplist += '<td></td>'
            nickcount += 1

    nickcount = 0
    newadminlist = ''
    cur.execute("SELECT * FROM `Users` WHERE `Usergroup` = 'newadmin'")
    for r in cur.fetchall():
        if nickcount == 5:
            newadminlist += '</tr><tr>'
            nickcount = 0
        # If you can be sure, that the nicknames in these groups are exactly the same, then use these lines
        # newadminlist += '<td><a href="https://terrariaforum.yamahi.eu/profile/%s">%s</a></td>' % urllib.request.pathname2url(r[1]), r[1]
        # Else:
        newadminlist += '<td class="text-warning">%s</a></td>' % r[1]
        nickcount += 1
    if nickcount != 5:
        while nickcount < 5:
            newadminlist += '<td></td>'
            nickcount += 1

    nickcount = 0
    adminlist = ''
    cur.execute("SELECT * FROM `Users` WHERE `Usergroup` = 'admin'")
    for r in cur.fetchall():
        if nickcount == 5:
            adminlist += '</tr><tr>'
            nickcount = 0
        # adminlist += '<td><a href="https://terrariaforum.yamahi.eu/profile/%s">%s</a></td>' % urllib.request.pathname2url(r[1]), r[1]
        adminlist += '<td class="text-danger">%s</a></td>' % r[1]
        nickcount += 1
    if nickcount != 5:
        while nickcount < 5:
            adminlist += '<td></td>'
            nickcount += 1

    nickcount = 0
    sadminlist = ''
    cur.execute("SELECT * FROM `Users` WHERE `Usergroup` = 'superadmin'")
    for r in cur.fetchall():
        if nickcount == 5:
            sadminlist += '</tr><tr>'
            nickcount = 0
        # sadminlist += '<td><a href="https://terrariaforum.yamahi.eu/profile/%s">%s</a></td>' % urllib.request.pathname2url(r[1]), r[1]
        sadminlist += '<td>%s</a></td>' % r[1]
        nickcount += 1
    if nickcount != 5:
        while nickcount < 5:
            sadminlist += '<td></td>'
            nickcount += 1

    groups = {'vips': viplist, 'newadmins': newadminlist, 'admins': adminlist, 'superadmins': sadminlist}

    db_close(conn, cur)
    return groups
