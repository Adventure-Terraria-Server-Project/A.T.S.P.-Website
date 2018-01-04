###############################################################################
#                                                                             #
'''Website Database-connection-related features'''                            #
#                                                                             #
###############################################################################


import cymysql

from conf import website_db
from time import gmtime
from time import strftime

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
    cur.execute('INSERT INTO `donate` (`time`, `user`) VALUES (%s, %s)', (time, nick))
    conn.commit()
    db_close(conn, cur)


def donate_read():
    conn, cur = db_con()
    cur.execute('SELECT * FROM `donate` ORDER BY `time` DESC LIMIT 20')
    nicks = list()
    for r in cur.fetchall():
        nicks.append([r[0], r[1]])

    db_close(conn, cur)
    return nicks


###############################################################################
#                                                                             #
'''Short-URL data'''                                                          #
#                                                                             #
###############################################################################


def shorturl_save(surl, url):
    conn, cur = db_con()
    cur.execute('INSERT INTO `shorturls` (`surl`, `url`) VALUES (%s, %s)', (surl, url))
    conn.commit()
    db_close(conn, cur)


def shorturl_read():
    conn, cur = db_con()
    cur.execute('SELECT * FROM `shorturls`')
    urls = list()
    for r in cur.fetchall():
        urls.append([r[0], r[0], r[1]])

    db_close(conn, cur)
    return urls


###############################################################################
#                                                                             #
'''Old Worlds'''                                                              #
#                                                                             #
###############################################################################


def get_old_worlds(item):
    conn, cur = db_con()
    sql = 'SELECT * FROM `oldworlds` ORDER BY `date` DESC LIMIT {0}, {1}'.format(item, 20)
    cur.execute(sql)
    worlds = cur.fetchall()

    db_close(conn, cur)
    return worlds


###############################################################################
#                                                                             #
'''Server Backup-Size in Dash'''                                              #
#                                                                             #
###############################################################################


def backup_size():
    conn, cur = db_con()
    dbtshock = []
    tserver = []
    htdocs = []
    cur.execute('SELECT * FROM `backups`')
    for r in cur.fetchall():
        if r[1] == 'db':
            dbtshock.append([r[0] * 1000, r[2]])
        elif r[1] == 'tserver':
            tserver.append([r[0] * 1000, r[2]])
        elif r[1] == 'htdocs':
            htdocs.append([r[0] * 1000, r[2]])

    db_close(conn, cur)
    return (dbtshock, tserver, htdocs)
