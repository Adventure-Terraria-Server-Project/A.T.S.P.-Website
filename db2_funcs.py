###############################################################################
#                                                                             #
'''Website Database-connection-related features'''                            #
#                                                                             #
###############################################################################
import cymysql

from conf import website_db
from datetime import date
from httpagentparser import simple_detect
from time import gmtime
from time import strftime
from time import time

get_browser = simple_detect

db_host = website_db.ip
db_port = website_db.port
db = website_db.db
db_user = website_db.user
db_pw = website_db.pw


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
'''Donation-Page data'''                                                      #
#                                                                             #
###############################################################################


def donate_save(nick):
    conn, cur = db_con()
    time = strftime('%Y.%m.%d - %H:%M:%S', gmtime())
    cur.execute("INSERT INTO `donate` (`time`, `user`) VALUES (%s, %s)", (time, nick))
    conn.commit()
    db_close(conn, cur)


def donate_read():
    conn, cur = db_con()
    cur.execute("SELECT * FROM `donate`")
    nicks = ''
    for r in cur.fetchall():
        nicks += '<span style="color:green">%s</span> <span style="color:blue">%s</span><br>' % (r[0], r[1])

    db_close(conn, cur)
    return nicks


###############################################################################
#                                                                             #
'''Short-URL data'''                                                          #
#                                                                             #
###############################################################################


def shorturl_save(surl, url):
    conn, cur = db_con()
    cur.execute("INSERT INTO `shorturls` (`surl`, `url`) VALUES (%s, %s)", (surl, url))
    conn.commit()
    db_close(conn, cur)


def shorturl_read():
    conn, cur = db_con()
    cur.execute("SELECT * FROM `shorturls`")
    urls = ''
    for r in cur.fetchall():
        urls += '<dt><a href="http://s.yamahi.eu/%s">%s</a></dt><dd>%s</dd>' % (r[0], r[0], r[1])

    db_close(conn, cur)
    return urls


###############################################################################
#                                                                             #
'''Old Worlds'''                                                              #
#                                                                             #
###############################################################################


def get_old_worlds():
    conn, cur = db_con()
    cur.execute("SELECT * FROM `oldworlds` ORDER BY `date` DESC")
    worlds = ''
    for r in cur.fetchall():
        worlds += '<tr><td>%s</td><td>%s</td><td><a class="btn btn-primary" href="static/files/world/%s">Download <span class="glyphicon glyphicon-download-alt"></span></a></td></tr>' % (r[0], r[1], r[1])

    db_close(conn, cur)
    return worlds


###############################################################################
#                                                                             #
'''Server Backup-Size in Dash'''                                              #
#                                                                             #
###############################################################################


def backup_size():
    conn, cur = db_con()
    tserver = []
    dbtshock = []
    dbforum = []
    dbwebsite = []
    htdocs = []
    dbtshock_weekly = []
    cur.execute("SELECT * FROM `backups`")
    for r in cur.fetchall():
        if r[1] == 'tShock files':
            tserver.append([r[0] * 1000, r[2]])
        elif r[1] == 'tShock DB':
            dbtshock.append([r[0] * 1000, r[2]])
        elif r[1] == 'tShock DB Weekly':
            dbtshock_weekly.append([r[0] * 1000, r[2]])
        elif r[1] == 'Forum DB':
            dbforum.append([r[0] * 1000, r[2]])
        elif r[1] == 'Website DB':
            dbwebsite.append([r[0] * 1000, r[2]])
        elif r[1] == 'htdocs':
            htdocs.append([r[0] * 1000, r[2]])
    db_close(conn, cur)
    return (tserver, dbtshock, dbtshock_weekly, dbforum, dbwebsite, htdocs)


###############################################################################
#                                                                             #
'''Website User Stats in Dash'''                                              #
#                                                                             #
###############################################################################


def get_visit():
    conn, cur = db_con()
    sql = 'SELECT distinct `time` FROM `stats`'
    cur.execute(sql)
    tables = ('user', 'mobile', 'browser', 'page')
    times = []
    guest = []
    users = []
    mobile = []
    desktop = []
    firefox = []
    chrome = []
    ie = []
    opera = []
    other_browsers = []
    index = []
    dash = []
    bans = []
    invparser = []
    searchuser = []
    logs = []
    irclogs = []
    motdrules = []
    shorturl = []
    votes = []
    donate = []
    donate_paypal = []
    donate_fundrazr = []
    terrariaservers = []
    tserverweb = []
    world = []
    worldvip = []
    embed = []
    error = []
    result_time = cur.fetchall()
    for table in tables:
        for time in result_time:
            time = time[0]
            times.append(time)
            sql = 'SELECT distinct {0} FROM `stats` WHERE time = %s'.format(table)
            params = time
            cur.execute(sql, params)
            if table == 'user':
                result_user = cur.fetchall()
                visits_guest = int()
                visits_user = int()
                for user in result_user:
                    sql = 'SELECT `user`,count(*) FROM `stats` WHERE `time` = %s AND `user` = %s'
                    params = (time, user[0])
                    cur.execute(sql, params)
                    if user[0] == 'Login':
                        visits_guest += cur.fetchone()[1]
                    else:
                        visits_user += cur.fetchone()[1]
                guest.append([time * 1000, visits_guest])
                users.append([time * 1000, visits_user])
            elif table == 'mobile':
                result_mobile = cur.fetchall()
                visits_mobile = int()
                visits_desktop = int()
                for device in result_mobile:
                    sql = 'SELECT `mobile`,count(*) FROM `stats` WHERE `time` = %s AND `mobile` = %s'
                    params = (time, device[0])
                    cur.execute(sql, params)
                    if device[0] == '1':
                        visits_mobile += cur.fetchone()[1]
                    else:
                        visits_desktop += cur.fetchone()[1]
                mobile.append([time * 1000, visits_mobile])
                desktop.append([time * 1000, visits_desktop])
            elif table == 'browser':
                result_browser = cur.fetchall()
                visits_firefox = int()
                visits_chrome = int()
                visits_ie = int()
                visits_opera = int()
                visits_other = int()
                for browser in result_browser:
                    sql = 'SELECT `browser`,count(*) FROM `stats` WHERE `time` = %s AND `browser` = %s'
                    params = (time, browser)
                    cur.execute(sql, params)
                    if 'Firefox' in browser[0]:
                        visits_firefox += cur.fetchone()[1]
                    elif 'Chrome' in browser[0]:
                        visits_chrome += cur.fetchone()[1]
                    elif 'Internet Explorer' in browser[0]:
                        visits_ie += cur.fetchone()[1]
                    elif 'Opera' in browser[0]:
                        visits_opera += cur.fetchone()[1]
                    else:
                        visits_other += cur.fetchone()[1]
                firefox.append([time * 1000, visits_firefox])
                chrome.append([time * 1000, visits_chrome])
                ie.append([time * 1000, visits_ie])
                opera.append([time * 1000, visits_opera])
                other_browsers.append([time * 1000, visits_other])
            elif table == 'page':
                result_page = cur.fetchall()
                visits_index = int()
                visits_dash = int()
                visits_bans = int()
                visits_invparser = int()
                visits_searchuser = int()
                visits_logs = int()
                visits_irclogs = int()
                visits_motdrules = int()
                visits_shorturl = int()
                visits_votes = int()
                visits_donate = int()
                visits_donate_paypal = int()
                visits_donate_fundrazr = int()
                visits_terrariaservers = int()
                visits_tserverweb = int()
                visits_world = int()
                visits_worldvip = int()
                visits_embed = int()
                visits_error = int()
                for page in result_page:
                    sql = 'SELECT `page`,count(*) FROM `stats` WHERE `time` = %s AND `page` = %s'
                    params = (time, page)
                    cur.execute(sql, params)
                    if page[0] == 'index':
                        visits_index += cur.fetchone()[1]
                    elif page[0] == 'dash':
                        visits_dash += cur.fetchone()[1]
                    elif page[0] == 'bans':
                        visits_bans += cur.fetchone()[1]
                    elif page[0] == 'invparser':
                        visits_invparser += cur.fetchone()[1]
                    elif page[0] == 'searchuser':
                        visits_searchuser += cur.fetchone()[1]
                    elif page[0] == 'logs':
                        visits_logs += cur.fetchone()[1]
                    elif page[0] == 'irclogs':
                        visits_irclogs += cur.fetchone()[1]
                    elif page[0] == 'motdrules':
                        visits_motdrules += cur.fetchone()[1]
                    elif page[0] == 'shorturl':
                        visits_shorturl += cur.fetchone()[1]
                    elif page[0] == 'votes':
                        visits_votes += cur.fetchone()[1]
                    elif page[0] == 'donate':
                        visits_donate += cur.fetchone()[1]
                    elif page[0] == 'donate_paypal':
                        visits_donate_paypal += cur.fetchone()[1]
                    elif page[0] == 'donate_fundrazr':
                        visits_donate_fundrazr += cur.fetchone()[1]
                    elif page[0] == 'terrariaservers':
                        visits_terrariaservers += cur.fetchone()[1]
                    elif page[0] == 'tserverweb':
                        visits_tserverweb += cur.fetchone()[1]
                    elif page[0] == 'world':
                        visits_world += cur.fetchone()[1]
                    elif page[0] == 'worldvip':
                        visits_worldvip += cur.fetchone()[1]
                    elif page[0] == 'embed':
                        visits_embed += cur.fetchone()[1]
                    elif page[0] == '404':
                        visits_error += cur.fetchone()[1]
                index.append([time * 1000, visits_index])
                dash.append([time * 1000, visits_dash])
                bans.append([time * 1000, visits_bans])
                invparser.append([time * 1000, visits_invparser])
                searchuser.append([time * 1000, visits_searchuser])
                logs.append([time * 1000, visits_logs])
                irclogs.append([time * 1000, visits_irclogs])
                motdrules.append([time * 1000, visits_motdrules])
                shorturl.append([time * 1000, visits_shorturl])
                votes.append([time * 1000, visits_votes])
                donate.append([time * 1000, visits_donate])
                donate_paypal.append([time * 1000, visits_donate_paypal])
                donate_fundrazr.append([time * 1000, visits_donate_fundrazr])
                terrariaservers.append([time * 1000, visits_terrariaservers])
                tserverweb.append([time * 1000, visits_tserverweb])
                world.append([time * 1000, visits_world])
                worldvip.append([time * 1000, visits_worldvip])
                embed.append([time * 1000, visits_embed])
                error.append([time * 1000, visits_error])
    db_close(conn, cur)
    return {'guest': guest, 'users': users, 'desktop': desktop, 'mobile': mobile, 'firefox': firefox, 'chrome': chrome, 'ie': ie, 'opera': opera, 'other': other_browsers, 'index': index, 'dash': dash, 'bans': bans, 'invparser': invparser, 'searchuser': searchuser, 'logs': logs, 'irclogs': irclogs, 'motdrules': motdrules, 'shorturl': shorturl, 'votes': votes, 'donate': donate, 'donate_paypal': donate_paypal, 'donate_fundrazr': donate_fundrazr, 'terrariaservers': terrariaservers, 'tserverweb': tserverweb, 'world': world, 'worldvip': worldvip, 'embed': embed, 'error': error}


def save_visit(user_data):
    today = open('today.txt')
    today = list(today.readline())
    if today[0] != date.isoformat(date.today()):
        with open('today.txt', 'w') as today:
            print((date.isoformat(date.today()), int(time())), file=today)
        today = date.isoformat(date.today()), int(time())
    browser = get_browser(user_data['ua'])
    tables = ('user', 'browser', 'page', 'referrer', 'time', 'ip')
    conn, cur = db_con()
    sql = 'INSERT INTO `stats` (`time`, `user`, `referrer`, `browser`, `page`, `ip`, `mobile`) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    params = (today[1], user_data['user'], user_data['referrer'], browser[1], user_data['page'], '"' + user_data['ip'] + '"', user_data['mobile'])
    cur.execute(sql, params)
    conn.commit()

    # Return recent online User (this day)
    sql = 'SELECT distinct `user` FROM `stats` WHERE FROM_UNIXTIME(`time`, %s) = FROM_UNIXTIME(%s, %s)'
    params = ('%Y-%M-%D', today[1], '%Y-%M-%D')
    cur.execute(sql, params)
    recents = ''
    for r in cur.fetchall():
        if r[0] != 'Login':
            recents += r[0] + ', '
    recents = recents[0:-2]
    db_close(conn, cur)
    return recents
