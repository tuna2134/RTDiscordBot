import os
import requests
import random
import string
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def file_list(path):
    file_name_list = []
    files = os.listdir(path)
    for p in files:
        file = Path(p).stem
        file_name_list.append(file)
    return file_name_list

def randomname(n):#ランダムな文字列ましーん
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def GET_Url(access_token, longUrl):#url短縮
    url = 'https://api-ssl.bitly.com/v3/shorten'
    query = {
            "access_token": access_token,
            "longUrl": longUrl
            }
    r = requests.get(url,params=query).json()['data']['url']
    return r

def make_pic():#認証画像作るやつ
    patht = "RT/server/pic/"
    im = Image.open("desk.png")
    back = im.copy()
    draw = ImageDraw.Draw(back)
    fnt = ImageFont.truetype('generic.otf', 70)
    ran = randomname(8)
    draw.text((200,170), str(ran), fill=(0,0,0), font=fnt)
    back.save(f'{patht}{ran}.png')
    return ran