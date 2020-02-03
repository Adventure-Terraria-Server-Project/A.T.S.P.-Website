###############################################################################
#                                                                             #
'''More non-Database functions'''                                             #
#                                                                             #
###############################################################################


import conf
import os
import time
import pickle
import urllib.request

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageEnhance
from db_funcs import get_user
from flask import json


###############################################################################
#                                                                             #
'''Make the banner for index'''                                               #
#                                                                             #
###############################################################################


def banner_image():
    imagelist = os.listdir(conf.screenshot_path)
    for files in imagelist:
        if files.endswith('.jpg'):
            blur(files)
    return imagelist


def blur(imagename):
    imgpath = conf.screenshot_path
    if not os.path.isfile(os.path.join(imgpath, '..', 'b_' + imagename)):
        img = Image.open(os.path.join(imgpath, imagename))
        img = img.filter(ImageFilter.GaussianBlur(2))
        img = ImageEnhance.Color(img).enhance(0.3)
        img.save(os.path.join(imgpath, '..', 'b_' + imagename), quality=70)


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
    font = ImageFont.truetype(font=conf.ava.nick_font, size=size)
    w, h = draw.textsize(user, font=font)
    while w >= 97:
        size -= 1
        font = ImageFont.truetype(font=conf.ava.nick_font, size=size)
        w, h = draw.textsize(user, font=font)
    draw.text(((100 - w) / 2, 3), user, (230, 6, 6), font=font)
    # Write bottomtext
    font = ImageFont.truetype(font=conf.ava.bottomtext_font, size=conf.ava.bottomtext_size)
    bottomtext = conf.ava.bottomtext
    w, h = draw.textsize(bottomtext, font=font)
    draw.text(((100 - w) / 2, (100 - h) - 10), bottomtext, (50, 100, 10), font=font)
    # Paste Char img
    imp = Image.open(os.path.join(conf.char_render, '{0}.png'.format(user)))
    x, y = imp.size
    l, r = (int((100 - x) / 2), 25)
    x, y = (x + l, y + r)
    im.paste(imp, box=(l, r, x, y), mask=imp)
    im.save(os.path.join(conf.ava.path, '{0}.png'.format(user)))


###############################################################################
#                                                                             #
'''Signature creator'''                                                       #
#                                                                             #
###############################################################################


def signature(user):
    user_grp = get_user(user)[1]
    im = Image.open(conf.sig.bg)
    # Write User Nick
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font=conf.sig.nick_font, size=conf.sig.nick_size)
    w, h = draw.textsize(user, font=font)
    draw.text(((360 - w) / 2, 42), user, (0, 100, 255), font=font)
    # Paste Char img
    imp = Image.open(os.path.join(conf.char_render, '{0}.png'.format(user)))
    x, y = imp.size
    l, r = (int((360 - w) / 2) - x - 10, 27)
    x, y = (x + l, y + r)
    im.paste(imp, box=(l, r, x, y), mask=imp)
    # Write User Group
    font = ImageFont.truetype(font=conf.sig.group_font, size=conf.sig.group_size)
    group = user_grp.replace('vip', 'VIP') \
        .replace('vip+', 'VIP+') \
        .replace('vip++', 'VIP++') \
        .replace('supervip', 'SuperVIP') \
        .replace('default', 'Regular Player') \
        .replace('newadmin', 'Moderator') \
        .replace('admin', 'Admin') \
        .replace('superAdmin', 'Executive')
    w, h = draw.textsize(group, font=font)
    draw.text(((360 - w) - 10, (95 - h) - 3), group, (0, 0, 0), font=font)
    im.save(os.path.join(conf.sig.path, '{0}.png'.format(user)))


###############################################################################
#                                                                             #
'''Playerlist'''                                                              #
#                                                                             #
###############################################################################


def player_list():
    try:
        player_list = list()
        j_data = urllib.request.urlopen(conf.rapi_players).read().decode('utf-8')
        p_list1 = json.loads(j_data).get('players')
        for i in p_list1:
            player = i['nickname']
            if os.path.exists(os.path.join(conf.char_render, '{0}.png'.format(player))):
                player_list.append((player, player))
            else:
                player_list.append((player, 'guest'))
    except:
        player_list = False
    return player_list


###############################################################################
#                                                                             #
'''Most voters list'''                                                        #
#                                                                             #
###############################################################################


def voters():
    votes = None
    modified_time = os.path.getmtime('data.pickle')
    if (time.time() - modified_time) // 3600 > 12:
        headers = {'content-type': 'application/json',
                   'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.1'}
        req = urllib.request.Request(url=conf.vote_ranking, headers=headers)
        with urllib.request.urlopen(req) as j_data:
            encoding = j_data.info().get_content_charset('utf-8')
            data = j_data.read().decode(encoding)
            try:
                votes = json.loads(data).get('voters')
                with open('data.pickle', 'wb') as f:
                    pickle.dump(votes, f, pickle.HIGHEST_PROTOCOL)
            except KeyError:
                with open('data.pickle', 'rb') as f:
                    votes = pickle.load(f)

    if not votes:
        with open('data.pickle', 'rb') as f:
            votes = pickle.load(f)
    return votes
