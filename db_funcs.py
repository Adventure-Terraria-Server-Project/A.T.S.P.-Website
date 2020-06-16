###############################################################################
#                                                                             #
'''tShock Database-connection-related features'''                             #
#                                                                             #
###############################################################################


import csv
try:
    import cymysql as Sql
except ImportError:
    import MySQLdb as Sql
import conf

from conf import tshock_db
from datetime import timedelta
from datetime import datetime
from time import time

db_host = tshock_db.ip
db_port = tshock_db.port
db = tshock_db.db
db_user = tshock_db.user
db_pw = tshock_db.pw


###############################################################################
#                                                                             #
'''Database-connect and close'''                                               #
#                                                                             #
###############################################################################


def db_con():
    conn = Sql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pw, db=db, autocommit=True)
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


# Requesting user info
def get_user(username):
    conn, cur = db_con()
    cur.execute('SELECT `Username`,`Usergroup`,`ID` FROM `users` WHERE `Username` = %s LIMIT 1', (username))
    user = cur.fetchone()
    db_close(conn, cur)
    return user


# Requesting user info
def get_user_by_id(id):
    conn, cur = db_con()
    cur.execute('SELECT `Username`,`Usergroup` FROM `users` WHERE `ID` = %s LIMIT 1', (id))
    user = cur.fetchone()
    db_close(conn, cur)
    return user


# Only used for login
def get_login(username):
    conn, cur = db_con()
    cur.execute('SELECT `Username`,`Password` FROM `users` WHERE `Username` = %s LIMIT 1', (username))
    user = cur.fetchone()
    db_close(conn, cur)
    return user


###############################################################################
#                                                                             #
'''Show group permission for superadmin'''                                    #
#                                                                             #
###############################################################################


def group_permissions():
    conn, cur = db_con()
    groups = []
    cur.execute('SELECT * FROM `grouplist`')
    for r in cur.fetchall():
        groups.append(r)
    db_close(conn, cur)
    return groups


###############################################################################
#                                                                             #
'''Banlists'''                                                                #
#                                                                             #
###############################################################################


def banlist():
    conn, cur = db_con()
    ipban = []
    nickban = []
    cur.execute('SELECT * FROM `BannedIP` ORDER BY `BanDate` DESC')
    for r in cur.fetchall():
        btime = r[2] - time()
        banned_time = datetime.utcfromtimestamp(int(r[1])).strftime('%Y.%m.%d %H:%M:%S')
        if r[2] == 0:
            ipban.append((r[0], banned_time, r[3], r[4]))
        elif r[2] > time():
            ipban.append((r[0], banned_time, r[3], r[4], format_timedelta(timedelta(seconds=btime))))

    cur.execute('SELECT * FROM `BannedPlayer` ORDER BY `BanDate` DESC')
    for r in cur.fetchall():
        btime = r[2] - time()
        banned_time = datetime.utcfromtimestamp(int(r[1])).strftime('%Y.%m.%d %H:%M:%S')
        if r[2] == 0:
            nickban.append((r[0], banned_time, r[3], r[4]))
        elif r[2] > time():
            nickban.append((r[0], banned_time, r[3], r[4], format_timedelta(timedelta(seconds=btime))))

    db_close(conn, cur)
    return {'ipban': ipban, 'nickban': nickban}


def dash_banned(user):
    conn, cur = db_con()
    ban = []
    cur.execute('SELECT * FROM `bannedplayer` WHERE `Player` = %s order by `BanDate` DESC', (user))
    r = cur.fetchone()
    if r:
        ban.append(r[0])
        ban.append(r[3])
        ban.append(r[4])
        if r[2] == 0:
            ban.append('PermaBan')
        elif r[2] > time():
            btime = r[2] - time()
            ban.append(format_timedelta(timedelta(seconds=btime)))
        else:
            ban = None

    db_close(conn, cur)
    return ban


# Format the ETA to a good readable format
def format_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{0}d {1}h {2}m {3}s'.format(td.days, hours, minutes, seconds)


###############################################################################
#                                                                             #
'''Get offline Messages'''                                                    #
#                                                                             #
###############################################################################


def msg(user):
    conn, cur = db_con()
    msgs = []
    cur.execute('SELECT `mailFrom`,`mailText` FROM `messageplugin` WHERE `mailTo` = %s and `Seen` = 0', (user))
    for r in cur.fetchall():
        msgs.append([r[0], r[1]])
    db_close(conn, cur)
    return msgs


###############################################################################
#                                                                             #
'''Get banned Items'''                                                        #
#                                                                             #
###############################################################################


def item_bans():
    conn, cur = db_con()
    banned_items = []
    cur.execute('SELECT `ItemName` FROM `ItemBans`')
    for r in cur.fetchall():
        banned_items.append(r[0])
    db_close(conn, cur)
    return banned_items


###############################################################################
#                                                                             #
'''Reports'''                                                                 #
#                                                                             #
###############################################################################


def get_reports():
    conn, cur = db_con()
    cur.execute('SELECT `ReportID`,`UserID`,`ReportedID`,`Message` FROM `Reports` WHERE `state` != 2')
    reports = []
    for r in cur.fetchall():
        userID = get_user_by_id(r[1])[0]
        reportedID = get_user_by_id(r[2])[0] if r[2] != -1 else 'Unknown ID'
        try:
            reports.append([r[0], userID, reportedID, r[3]])
        except TypeError:
            reports.append([r[0], r[1], r[2], r[3]])
    return reports


###############################################################################
#                                                                             #
'''Search for Users'''                                                        #
#                                                                             #
###############################################################################


def search_user(user):
    conn, cur = db_con()
    results = []
    search = '%{}%'.format(user)
    cur.execute('SELECT `Username` FROM `Users` WHERE `Username` LIKE %s LIMIT 50', (search))
    for r in cur.fetchall():
        results.append(r[0])
    return results


###############################################################################
#                                                                             #
'''Get Player Inventory'''                                                    #
#                                                                             #
###############################################################################


def get_player_inv(username):
    user = get_user(username)
    if user:
        conn, cur = db_con()
        cur.execute('SELECT `Inventory`,`MaxHealth`,`MaxMana` FROM `tsCharacter` WHERE `Account` = %s LIMIT 1', (user[2]))
        user_info = cur.fetchone()
        if user_info:
            user_inv = inv_pars(user_info[0])
        else:
            return None
        group = user[1]
        db_close(conn, cur)
        return {'inv': user_inv, 'health': user_info[1], 'mana': user_info[2], 'group': group}


def inv_pars(inventorystring):
    inventoryentries = inventorystring.split('~')
    items = {}
    prefixes = {}
    inv = {
        'inv': [],
        'coins': [],
        'ammo': [],
        'armor': [],
        'vanity': [],
        'dye': [],
        'equipment': [],
        'eqdye': [],
        'piggy': [],
        'safe': [],
        'trash': '',
        'forge': [],
        'void': [],
    }

    with open(conf.items) as itemsfile:
        itemsreader = csv.reader(itemsfile, delimiter=',', quotechar='"')
        for row in itemsreader:
            items.update({row[0]: {'name': row[1]}})

    with open(conf.prefixes) as prefixfile:
        prefixreader = csv.reader(prefixfile, delimiter=',', quotechar='"')
        for row in prefixreader:
            prefixes.update({row[0]: {'name': row[1]}})

    for count_inv, row in enumerate(inventoryentries):
        itemid, amount, prefixid = row.split(',')
        if count_inv <= 50:
            try:
                inv['inv'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['inv'].append(0)
        elif count_inv <= 53:
            try:
                inv['coins'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['coins'].append(0)
        elif count_inv <= 58:
            try:
                inv['ammo'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['ammo'].append(0)
        elif count_inv <= 68:
            try:
                inv['armor'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['armor'].append(0)
        elif count_inv <= 78:
            try:
                inv['vanity'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['vanity'].append(0)
        elif count_inv <= 88:
            try:
                inv['dye'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['dye'].append(0)
        elif count_inv <= 93:
            try:
                inv['equipment'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['equipment'].append(0)
        elif count_inv <= 98:
            try:
                inv['eqdye'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['eqdye'].append(0)
        elif count_inv <= 138:
            try:
                inv['piggy'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['piggy'].append(0)
        elif count_inv <= 178:
            try:
                inv['safe'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['safe'].append(0)
        elif count_inv == 179:
            try:
                inv['trash'] = (prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount)
            except KeyError:
                inv['trash'] = 0
        elif count_inv <= 220:
            try:
                inv['forge'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['forge'].append(0)
        else:
            try:
                inv['void'].append((prefixes.get(prefixid, {}).get('name', ''), items[itemid]['name'], itemid, amount))
            except KeyError:
                inv['void'].append(0)

    return inv


###############################################################################
#                                                                             #
'''Playergroups from MySQL to show VIPs and staff'''                          #
#                                                                             #
###############################################################################


def lgroups():
    conn, cur = db_con()
    viplist = list()
    g_colors = {'vip': 'blue', 'vip+': 'green', 'vip++': 'orange', 'supervip': 'violet'}
    cur.execute('SELECT `Username`,`Usergroup` FROM `Users` WHERE `Usergroup` in ("vip", "vip+", "vip++", "supervip")')
    for r in cur.fetchall():
        viplist.append([g_colors.get(r[1], '#467dff'), r[0]])

    builderlist = []
    cur.execute('SELECT `Username` FROM `Users` WHERE `Usergroup` in ("builder", "trustedbuilder")')
    for r in cur.fetchall():
        builderlist.append(r[0])

    newadminlist = []
    cur.execute('SELECT `Username` FROM `Users` WHERE `Usergroup` = "newadmin"')
    for r in cur.fetchall():
        newadminlist.append(r[0])

    adminlist = []
    cur.execute('SELECT `Username` FROM `Users` WHERE `Usergroup` in ("admin", "admin+")')
    for r in cur.fetchall():
        adminlist.append(r[0])

    sadminlist = []
    cur.execute('SELECT `Username` FROM `Users` WHERE `Usergroup` = "superadmin"')
    for r in cur.fetchall():
        sadminlist.append(r[0])

    db_close(conn, cur)
    return {
        'vips': viplist,
        'builder': builderlist,
        'newadmins': newadminlist,
        'admins': adminlist,
        'superadmins': sadminlist,
    }
