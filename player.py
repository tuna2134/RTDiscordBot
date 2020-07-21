# -*- coding: utf-8 -*-
import discord
import re
import os
import glob
import sys
import asyncio
import time
import requests
import random
import string
import youtube_dl
import pathlib
import aiohttp
import json
import emoji
from urllib import parse
from bs4 import BeautifulSoup
from discord import Webhook, AsyncWebhookAdapter
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator
from urllib.parse import urlparse
from pathlib import Path
from discord.ext import commands
from datetime import datetime, date, timedelta

print('Now Loading...')

pr = "rt!"

casfo = glob.glob("./nglist" + "/*")
nopas = "./nglist"
testf = []
for file in casfo: # ファイル一覧
    prii = file.lstrip(nopas)
    pri = prii.rstrip(".txt")
    pr = prai.rstrip("/")
    testf.append(pr)

with open("RT/level.json",mode="r") as f:
    levels = json.load(f)
with open("RT/emojis.json",mode="r") as f:
    emojis = json.load(f)

# Jishaku
team_id = [667319675176091659,634763612535390209,693025129806037003]
class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id in team_id:
            return True
        return await super().is_owner(user)

#プリフィックスとか
bot = MyBot(command_prefix=pr)
bot.load_extension("jishaku")
bot.load_extension('dispander')
bot.remove_command("help")

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

noul = [7, 8, 9]
nodl = [25, 24, 23]

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#翻訳のやつ
translator = Translator()
bname = "RT test"

gc = "RT/server/gc/"

def extract_emojis(str):
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

class Google:
    def __init__(self):
        self.GOOGLE_SEARCH_URL = 'https://www.google.co.jp/search'
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'})

    def Search(self, keyword, type='text', maximum=100):
        print('Google', type.capitalize(), 'Search :', keyword)
        result, total = [], 0
        query = self.query_gen(keyword, type)
        while True:
            html = self.session.get(next(query)).text
            links = self.get_links(html, type)

            if not len(links):
                print('-> No more links')
                break
            elif len(links) > maximum - total:
                result += links[:maximum - total]
                break
            else:
                result += links
                total += len(links)

        print('-> Finally got', str(len(result)), 'links')
        return result

    def query_gen(self, keyword, type):
        page = 0
        while True:
            if type == 'text':
                params = parse.urlencode({
                    'q': keyword,
                    'num': '100',
                    'filter': '0',
                    'start': str(page * 100)})
            elif type == 'image':
                params = parse.urlencode({
                    'q': keyword,
                    'tbm': 'isch',
                    'filter': '0',
                    'ijn': str(page)})

            yield self.GOOGLE_SEARCH_URL + '?' + params
            page += 1

    def get_links(self, html, type):
        soup = BeautifulSoup(html, 'lxml')
        if type == 'text':
            elements = soup.select('.rc > .r > a')
            links = [e['href'] for e in elements]
        elif type == 'image':
            elements = soup.select('.rg_meta.notranslate')
            jsons = [json.loads(e.get_text()) for e in elements]
            links = [js['ou'] for js in jsons]
        return links

def line(s, line_number):
    return s.splitlines()[line_number - 1]

def makeli(id):
    for s in range(8):
        s = s + 1
        os.mkdir(f"RT/server/rea/{id}/{s}")

def file_list(path):#ファイルの名前リストを作るやつ
    file_name_list = []
    files = os.listdir(path)
    for p in files:
        file = Path(p).stem
        file_name_list.append(file)
    return file_name_list

def randomname(n):#ランダムな文字列を作るやつ
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def vse(mes):
    if True:
        eve = "None"
        pic = "None"
        tran = "None"
        if (os.path.exists(f"RT/server/eve/{mes.guild.id}.txt")):
            with open(f"RT/server/eve/{mes.guild.id}.txt") as f:
                eve = f.read()
            f.close()
        pas = "RT/server/pic/" + str(mes.guild.id) + ".txt"
        if (os.path.exists(pas)):
            pic = "True"
        else:
            pic = "False"
        if (os.path.exists(f"RT/server/tran/{mes.guild.id}.txt")):
            with open(f"RT/server/tran/{mes.guild.id}.txt") as f:
                tran = f.read()
            f.close()
        try:
            cha = discord.utils.get(mes.guild.text_channels, name="長文置き場-rt")
        except AttributeError:
            pass
        if cha is None:
            cha = "False"
        else:
            cha = "True"
        if (os.path.exists(f"RT/server/welcome/id/{mes.guild.id}.txt")):
            wel = "True"
        else:
            wel = "False"
        if eve != "True":
            eve = "False"
        if pic != "False":
            pic = "True"
        if tran != "True":
            tran = "False"
        embed = discord.Embed(
            title="RT機能ON/OFF表ー",
            description="RTの機能がONかOFF確認\nTrueはONです",
            color=0x0066ff)
        embed.add_field(
            name="全員メンション禁止",
            value=f"**{eve}**\n1番目のリアクションでON/OFFを切り替えれます")
        embed.add_field(
            name="翻訳",
            value=f"**{tran}**\n2番目のリアクションでON/OFFを切り替えれます")
        embed.add_field(
            name="長文コンパクト",
            value=f"**{cha}**\n`長文置き場-rt`というチャンネルを作るとONになります。")
        embed.add_field(
            name="ウェルカムメッセージ",
            value=f"**{wel}**\n`rt!here [送信するメッセージ]`\nで実行した場所にWelcomeメッセを設定\n`rt!heredel`で削除ができます")
        embed.add_field(
            name="画像認証",
            value=f"**{pic}**\n`rt!cpic [役職名/False]`で変更できます\n役職名でいれた役職が認証した人につけられます\nFalseにするとオフになります")
        return embed
  
def GET_Url(access_token, longUrl):#短縮URLを作るやつ
    url = 'https://api-ssl.bitly.com/v3/shorten'
    query = {
            "access_token": access_token,
            "longUrl": longUrl
            }
    r = requests.get(url,params=query).json()['data']['url']
    return r

def make_pic():#認証用画像を作るやつ
    patht = "RT/server/pic/"
    im = Image.open("RT/desk.png")
    back = im.copy()
    draw = ImageDraw.Draw(back)
    fnt = ImageFont.truetype('RT/generic.otf', 70)
    ran = randomname(8)
    draw.text((200,170), str(ran), fill=(0,0,0), font=fnt)
    back.save(f'{patht}{ran}.png')
    return ran

class Music(commands.Cog):
    @bot.command(pass_context=True)
    async def play(ctx, url):
        global voice_client
        try:
            await ctx.voice_client.disconnect()
        except AttributeError:
            pass
        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            voice_client = await discord.VoiceChannel.connect(bot.get_channel(ctx.message.author.voice.channel.id))
            ctx.voice_client.play(player, after=lambda e: print('エラー!: %s' % e) if e else None)
        await ctx.send('再生中: {}'.format(player.title))

    @bot.command(pass_context=True)
    async def dis(ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("再生終了。")

@bot.event
async def on_ready():
    global bname
    print("RT起動完了！")
    activity = discord.Activity(
        name=f"rt!help|{len(bot.guilds)}サーバー", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    bname = bot.user.name

@bot.event
async def on_member_remove(member):
    path = f"RT/server/remove/id/{member.guild.id}.txt"
    pathh = f"RT/server/remove/text/{member.guild.id}.txt"
    if (os.path.exists(path)):
        with open(path) as f:
            idd = f.read()
        with open(pathh) as f:
            text = f.read()
        f.close()
        channel = bot.get_channel(int(idd))
        await channel.send(f"{member.mention},{text}")

@bot.event
async def on_member_join(member):
    path = f"RT/server/welcome/id/{member.guild.id}.txt"
    pathh = f"RT/server/welcome/text/{member.guild.id}.txt"
    patht = f"RT/server/pic/{member.guild.id}.txt"
    if (os.path.exists(patht)):
        name = make_pic()
        patht = f"RT/server/pic/{name}.png"
        if os.path.exists(f"RT/server/pic/{member.guild.id}") != True:
            os.mkdir("RT/server/pic/" + str(member.guild.id))
            print("made!")
        pathtt = f"RT/server/pic/{member.guild.id}/{member.id}.txt"
        if (os.path.exists("RT/server/pic/image.png")):
            os.remove("RT/server/pic/image.png")
        with open(pathtt, mode="w") as f:
            f.write(name)
        os.rename(patht, "RT/server/pic/image.png")
        try:
            cha = discord.utils.get(member.guild.text_channels, name="認証-rt")
        except AttributeError:
            cha = "None"
        if cha != "None":
            file = discord.File('RT/server/pic/image.png', filename="image.png")
            embed = discord.Embed(title="画像認証",
                description="この画像にある文字を入力してください。",
                color=0x0066ff)
            embed.set_image(url="attachment://image.png")
            embed.set_footer(text=member.guild.name)
            await cha.send(member.mention)
            await cha.send(file=file, embed=embed)
        os.remove("RT/server/pic/image.png")
        f.close()
    print("Welcom Messeage")
    if (os.path.exists(path)):
        print("GO")
        with open(path) as f:
            idd = f.read()
        with open(pathh) as f:
            text = f.read()
        f.close()
        channel = bot.get_channel(int(idd))
        await asyncio.sleep(1)
        await channel.send(f"{member.mention},{text}")

@bot.event
async def on_guild_join(guild):
    activity = discord.Activity(
        name=f"rt!help | {len(bot.guilds)}サーバー", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def on_guild_remove(guild):
    activity = discord.Activity(
        name=f"rt!help | {len(bot.guilds)}サーバー", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def on_command_error(ctx,error):
  if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    embed=discord.Embed(title="すみません...",description="コマンドが見つかりませんでした。",color=0x00ffff)
    await ctx.send(embed=embed)
    print(f"log:{ctx.author.name}が存在しないコマンドを実行しました")
  elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
    embed=discord.Embed(title="エラー",description="引数が足りません。helpコマンドを見直してみてください。",color=0x00ff00)
    await ctx.send(embed=embed)
    print(f"log:{ctx.author.name}が引数の足りないコマンドを実行しました。")
  else:
    e = discord.Embed(title=":warning:エラー",description="すみません！\n例外エラーが発生しました。",color=0xff0000)
    e.add_field(name="エラー内容",value=f"```{error}```")
    await ctx.channel.send(embed=e)

@bot.command()
async def helptest(ctx):
    await pages.start(ctx)

#ここからコマンド
@bot.command()
async def help(ctx):
    pass
"""
        await mes.add_reaction("<:1_~1:726052719324037230")
        await mes.add_reaction("<:2_~1:726052719114190880")
        await mes.add_reaction("<:3_~1:726052719441215518")
        await mes.add_reaction("<:4_~1:726052719504261253")
        await mes.add_reaction("<:5_~1:726052719340683264")
        await mes.add_reaction("<:6_~1:726052719328100432")
        await mes.add_reaction("<:7_~1:726052719030304839")
<:up2:728789094297108580
<:down2:728789094410223686
<:hidari:731730013329817600
<:migi:731730012943941683
"""

@bot.command()
async def testMK(ctx):
    tes = __file__.replace("main.py", "")
    print(tes)
    os.mkdir(f"{tes}testt")
    await ctx.send("ok")
  
@bot.command()
async def testPic(ctx):
        name = make_pic()
        pathtt = "RT/server/pic/"
        await ctx.send("画像認証用の画像を生成しました。")
        await ctx.send(file=discord.File(f'{pathtt}{name}.png'))
        os.remove(f"{pathtt}{name}.png")

@bot.command()
async def ping(ctx):
        starttime = time.time()
        msg = await ctx.send("測定中...")
        ping = (time.time() - starttime) * 1000
        messsag = f"{ping}ms"
        await msg.edit(content=messsag)

    
@bot.command()
async def ngadd(ctx, arg):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            sID = ctx.guild.id
            if str(sID) in str(testf):
                ngtxt = f"RT/nglist/{sID}.txt"
            else:#もしまだngリストファイルがなかったら
                await ctx.send("NGリストファイルを作っています...")
                ngtxt = f"RT/nglist/{sID}.txt"
                f = open(ngtxt, "w")
                f.close()
                testf.append(sID)
            with open(ngtxt) as f:
                nglist = f.read().splitlines()
            nglist = [a for a in nglist if a != '']
            word = arg
            print('add:' + str(word))
            print('NGワードを追加します')
            with open(ngtxt, mode='a') as f:
                f.write('\n' + str(word))
            with open(ngtxt) as f:
                nglist = f.read().splitlines()
            print('追加しました')
            await ctx.send('NGワードを追加したよ。')
            await ctx.message.delete()
            f.close()
        else:#管理者じゃなかったら
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def nglist(ctx,arg):
    if True:
        ngtxt = f"RT/nglist/{ctx.guild.id}.txt"
        if (os.path.exists(ngtxt)):
            with open(ngtxt) as f:
                nglist = f.read().splitlines()
            f.close()
            lis = [a for a in nglist if a != '']
            title = "NGワード一覧"
            ngg = arg
            pa = int(ngg)
            no = len(lis)
            embed = discord.Embed(title=title,description=f"{pa}ページ目 NGワードの数:{no}",color=0x4682b4)
            c = 0
            cc = 0
            if pa > 1:
                ccc = pa*10
                c = ccc - 10
            while True:
                try:
                    naiy = lis[c]
                except IndexError:
                    await ctx.send(f"{pa}ページ目はまだありません")
                    return
                c = c + 1
                embed.add_field(name=str(c),value=f"||{naiy}||")
                if c == pa * 10 or c == len(lis):
                    break
            await ctx.send(embed=embed)
        else:
            await ctx.send("まだNGワードが登録されていません。")

@bot.command()
async def ngdel(ctx, arg):
  dword = arg
  if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            ngtxt = f"RT/nglist/{ctx.guild.id}.txt"
            if (os.path.exists(ngtxt)):
                with open(ngtxt) as f:
                    nglist = f.read().splitlines()
                print(nglist)
                f.close()
            else:
                await ctx.send("NGリストファイルがまだ作られていません。\n`rt!ngadd [NGワード]`コマンドでNGワードを追加してください。")
                await ctx.message.delete()
                return
            nglist = [a for a in nglist if a != '']
            true = dword in nglist
            if True == true:
                s = dword
                with open(ngtxt, 'r+') as f:  # 上書き
                    d = f.readlines()
                    f.seek(0)
                    for l in d:
                        if s not in l:
                            f.write(l)
                            f.truncate()
                with open(ngtxt) as f:
                    nglist = f.read().splitlines()
            await ctx.send('NGワードをリストから削除しました。')
            f.close()
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def tran(ctx, arg):
    if True:
        if ctx.author.guild_permissions.administrator or ctx.author.id in team_id:
            at = arg
            if (os.path.exists(f"RT/server/tran/{ctx.guild.id}.txt")):
                with open(f"RT/server/tran/{ctx.guild.id}.txt") as d:
                    a = d.read()
                d.close()
                if at == a:
                    await ctx.send(f"既に翻訳機能は`{at}`になっています。")
                    return
            if at == "True" or at == "False":
                with open(f"RT/server/tran/{ctx.guild.id}.txt", mode="w") as f:
                    f.write(at)
                await ctx.send(f"翻訳機能を{at}にしました。")
                f.close()
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def baneve(ctx, arg):
    if True:
        if ctx.author.guild_permissions.administrator or ctx.author.id in team_id:
            at = arg
            paa = f"RT/server/eve/{ctx.guild.id}.txt"
            if (os.path.exists(paa)):
                with open(paa) as d:
                    a = d.read()
                d.close()
                if at == a:
                    await ctx.send(f"既にevryone禁止機能は`{at}`になっています。")
                    return
            if at == "True" or at == "False":
                with open(paa, mode="w") as f:
                    f.write(at)
                await ctx.send(f"evryone禁止機能を`{at}`にしました。")
                f.close()
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def gooddm(ctx, arg):
    if True:
        at = arg
        paa = f"RT/profile/good/{ctx.author.id}.txt"
        if (os.path.exists(paa)):
            with open(paa) as d:
                a = d.read()
            d.close()
            if at == a:
                await ctx.send(f"既にいいね通知機能は`{at}`になっています。")
                return
        if at == "True" or at == "False":
            with open(paa, mode="w") as f:
                f.write(at)
            await ctx.send(f"いいね通知機能を`{at}`にしました。")
            f.close()
        return

@bot.command()
async def heredel(ctx):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            path = f"RT/server/welcome/id/{ctx.guild.id}.txt"
            pathh = f"RT/server/welcome/text/{ctx.guild.id}.txt"
            if (os.path.exists(path)):
                os.remove(path)
                os.remove(pathh)
                await ctx.send("ウェルカムメッセージ機能をオフにしました。")
            else:
                await ctx.send("ウェルカムメッセージはまだ登録されていません。")
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def here(ctx, arg):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            await ctx.send("設定中...")
            text = arg
            text = text.replace("$", "\n")
            path = f"RT/server/welcome/id/{ctx.guild.id}.txt"
            pathh = f"RT/server/welcome/text/{ctx.guild.id}.txt"
            with open(path, mode="w") as f:
                f.write(str(ctx.channel.id))
            with open(pathh, mode="w") as f:
                f.write(text)
            f.close()
            await ctx.send("ウェルカムメッセージを設定しました。")
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def cpic(ctx, arg):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            await ctx.send("設定中...")
            text = arg
            path = f"RT/server/pic/{ctx.guild.id}.txt"
            if text == "False":
                if (os.path.exists(path)):
                    os.remove(path)
                    await ctx.send("画像認証をオフにしました。")
                else:
                    await ctx.send("画像認証は既にオフです。")
            else:
                te = []
                for role in ctx.guild.roles:
                    te.append(role.name)
                if text in te:
                    with open(path, mode="w") as f:
                        f.write(str(text))
                    f.close()
                    await ctx.send("画像認証を設定しました。\n認証用に`認証-rt`というチャンネルがない場合作成してください。")
                else:
                    await ctx.send("その役職はありません。")
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.command()
async def menum(ctx, arg):
    async with ctx.typing():
        if arg in ["New", "False"]:
            if arg == "False":
                with open(f"RT/server/rea2/{ctx.author.id}.txt", mode="w") as f:
                    f.write(arg)
                f.close()
                kek = f"メニュー設定を`{arg}`にしました。"
            if arg == "New":
                ra = randomname(4)
                with open(f"RT/server/rea2/{ctx.author.id}.txt", mode="w") as f:
                    f.write(ra)
                f.close()
                os.mkdir(f"RT/server/rea/{ra}")
                for s in range(8):
                    s = s + 1
                    fa = pathlib.Path(f"RT/server/rea/{ra}/{s}.txt")
                    fa.touch()
                kek = f"メニュー設定ファイルを設定名`{ra}`で作成しました。\n:one: :two: ...のﾘｱｸｼｮﾝで設定が終わったら`rt!menuv {ra}`と実行してください。"
        else:
            kek = "引数にはNewまたはFalseを入れてください。"
    await ctx.send(kek)
    
@bot.command()
async def menus(ctx, arg):
    async with ctx.typing():
        if (os.path.exists(f"RT/server/rea/{arg}/")):
            with open(f"RT/server/rea2/{ctx.author.id}.txt", mode="w") as f:
                f.write(arg)
            f.close()
            kek = f"メニュー設定対象を`{arg}`にしました。"
        else:
            kek = f"その設定名のファイルはありませんでした。"
    await ctx.send(kek)

@bot.command()
async def menuv(ctx, arg):
    ke = 0
    async with ctx.typing():
        if (os.path.exists(f"RT/server/rea2/{ctx.author.id}.txt")):
            with open(f"RT/server/rea2/{ctx.author.id}.txt") as f:
                k = f.read()
            f.close()
            if k == "False":
                kek = f"メニュー設定が`False`になっています。\n`rt!menum New`と実行してください。"
            else:
                if (os.path.exists(f"RT/server/rea/{arg}/1.txt")):
                    with open(f"RT/server/rea/{arg}/1.txt") as f:
                        kek = f.read()
                        ke = 1
                    f.close()
                    if kek == "" or kek is None:
                        ke = 0
                        kek = f"まだメッセージが設定されていません。\n:one: :two: などのリアクションを自分のメッセージにつけて設定してください。"
                else:
                    kek = "メニュー設定対象名が間違っています。"
        else:
            kek = f"メニュー設定ファイルがありません。\n`rt!menum New`と実行してください。"
    if ke == 0:
        await ctx.send(kek)
    else:
        mes = await ctx.send(kek)
        async with ctx.typing():
            await mes.add_reaction("<:1_:726043030708158543")
            await mes.add_reaction("<:2_:726043030364356718")
            await mes.add_reaction("<:3_:726043030473146408")
            await mes.add_reaction("<:4_:726043030590586970")
            await mes.add_reaction("<:5_:726043030343123036")
            await mes.add_reaction("<:6_:726043030498574376")
            await mes.add_reaction("<:7_:726043030221750293")
            await mes.add_reaction("<:8_:726043030515220580")
        messs = await ctx.send("ﾒﾆｭｰﾒｯｾｰｼﾞ作成完了\n(数秒後このﾒｯｾｰｼﾞは消えます)")
        await asyncio.sleep(3)
        await messs.delete()

@bot.command()
async def makee(ctx,arg,arg2):
    e = discord.Embed(title=arg,description=arg2,color=0x00ff00)
    await ctx.send(embed=e)

@bot.command()
async def makeg(ctx):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            with ctx.channel.typing():
                if (os.path.exists(f"RT/server/gc/{ctx.channel.name}.txt")):
                    await ctx.channel.send("このチャンネル名のグローバルチャットは既にあります。\n他の名前を使ってください。")
                    return
                aru = re.compile(r'[\\/:*?"<>|]+').search(ctx.channel.name)
                if aru:
                    await ctx.send(r'チャンネル名に \\/:*?"<>| の文字は使えません。')
                    return
                print("グローバルチャットを作成します")
                with open(f"RT/server/gc/{ctx.channel.name}.txt", mode="w") as f:
                    f.write(str(ctx.channel.id))
                with open(f"RT/server/gc2/{ctx.channel.name}.txt", mode="w") as f:
                    f.write(str(ctx.message.author.id))
                f.close()
            await ctx.send(f"このチャンネルをグローバルチャットにしました。\nチャンネル名は変更しないでください。\n他のサーバーでこのグローバルチャットに接続するには`rt!cng {ctx.channel.name}`と実行してください。")

@bot.command()
async def cng(ctx, arg):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            name = arg
            if (os.path.exists(f"RT/server/gc/{name}.txt")):
                with open(f"RT/server/gc/{name}.txt", mode="a") as f:
                    ok = f.write(f"\n{ctx.channel.id}")
                f.close()
                await ctx.message.channel.edit(name=name)
            else:
                await ctx.send("そのグローバルチャットはありません。")
                return
            with open(f"RT/server/gc/{name}.txt") as f:
                l_strip = [s.strip() for s in f.readlines()]
            await ctx.send("このチャンネルをグローバルチャットとリンクしました。\nチャンネル名は変更しないでください。")
            for w in l_strip:
                if w is None:
                    continue
                channel = bot.get_channel(int(w))#client
                embed = discord.Embed(
                    title="お知らせ",
                    description=f"グローバルチャットに\n`{ctx.guild.name}`というサーバーが接続しました。",
                    color=0xffd900)
                await channel.send(embed=embed)
            f.close()

@bot.command()
async def delgc(ctx):
    async with ctx.typing():
        if (os.path.exists(f"RT/server/gc2/{ctx.channel.name}.txt")):
            with open(f"RT/server/gc2/{ctx.channel.name}.txt") as f:
                o = f.read()
            f.close()
            if o == str(ctx.message.author.id):
                os.remove(f"RT/server/gc/{ctx.channel.name}.txt")
                os.remove(f"RT/server/gc2/{ctx.channel.name}.txt")
                kek = "グローバルチャットを削除しました。"
            else:
                kek = "グローバルチャット作成者のみこのコマンドを使用できます。"
        else:
            kek = "このコマンドはグローバルチャットの中でのみ使用可能です。"
    await ctx.send(kek)

@bot.command()
async def sinfo(ctx):
    member_count = ctx.message.guild.member_count
    user_count = sum(1 for member in ctx.message.guild.members if not member.bot)
    bot_count = sum(1 for member in ctx.message.guild.members if member.bot)
    guild_id = ctx.message.guild.id
    embed = discord.Embed(title=f"{ctx.message.guild.name}", description=ctx.message.guild.description, color=0x0066ff)
    embed.add_field(name="メンバー数", value=member_count)
    embed.add_field(name="ユーザー数", value=user_count)
    embed.add_field(name="BOT数", value=bot_count)
    embed.add_field(name="チャンネル数", value=len(ctx.message.guild.channels))
    embed.add_field(name="サーバーID", value=guild_id)
    embed.set_author(name=f"{ctx.message.guild.owner.name}", icon_url=ctx.message.guild.owner.avatar_url)
    embed.set_image(url=ctx.message.guild.banner_url)
    embed.set_thumbnail(url=ctx.message.guild.icon_url_as(format="png"))
    embed.set_footer(text=f"作成日:{ctx.message.guild.created_at.strftime('%Y-%m-%d')}")
    await ctx.send(embed=embed)

@bot.command()
async def vset(ctx):
    if True:
        eve = "None"
        pic = "None"
        tran = "None"
        if (os.path.exists(f"RT/server/eve/{ctx.guild.id}.txt")):
            with open(f"RT/server/eve/{ctx.guild.id}.txt") as f:
                eve = f.read()
            f.close()
        pas = "RT/server/pic/" + str(ctx.guild.id) + ".txt"
        if (os.path.exists(pas)):
            pic = "True"
        else:
            pic = "False"
        if (os.path.exists(f"RT/server/tran/{ctx.guild.id}.txt")):
            with open(f"RT/server/tran/{ctx.guild.id}.txt") as f:
                tran = f.read()
            f.close()
        try:
            cha = discord.utils.get(ctx.guild.text_channels, name="長文置き場-rt")
        except AttributeError:
            pass
        if cha is None:
            cha = "False"
        else:
            cha = "True"
        if (os.path.exists(f"RT/server/welcome/id/{ctx.guild.id}.txt")):
            wel = "True"
        else:
            wel = "False"
        if eve != "True":
            eve = "False"
        if pic != "False":
            pic = "True"
        if tran != "True":
            tran = "False"
        embed = discord.Embed(
            title="RT機能ON/OFF表ー",
            description="RTの機能がONかOFF確認\nTrueはONです",
            color=0x0066ff)
        embed.add_field(
            name="全員メンション禁止",
            value=f"**{eve}**\n1番目のリアクションでON/OFFを切り替えれます")
        embed.add_field(
            name="翻訳",
            value=f"**{tran}**\n2番目のリアクションでON/OFFを切り替えれます")
        embed.add_field(
            name="長文コンパクト",
            value=f"**{cha}**\n`長文置き場-rt`というチャンネルを作るとONになります。")
        embed.add_field(
            name="ウェルカムメッセージ",
            value=f"**{wel}**\n`rt!here [送信するメッセージ]`\nで実行した場所にWelcomeメッセを設定\n`rt!heredel`で削除ができます")
        embed.add_field(
            name="画像認証",
            value=f"**{pic}**\n`rt!cpic [役職名/False]`で変更できます\n役職名でいれた役職が認証した人につけられます\nFalseにするとオフになります")
        mes = await ctx.send(embed=embed)
        await mes.add_reaction("<:atto:721338408693399665")
        await mes.add_reaction("<:eng2jaof:721340045553827840")

@bot.command()
async def delmes(ctx, arg):
  global team_id
  if True:
        if ctx.author.guild_permissions.administrator or ctx.author.id in team_id:
            at = int(arg)
            if at < 51 and at > 1:
                msgs = [msg async for msg in ctx.channel.history(limit=(at+1))]
                await ctx.channel.delete_messages(msgs)
                delmsg = await ctx.send(f'複数のメッセージの削除が完了しました。(このメッセージは数秒後消えます)')
                await asyncio.sleep(4)
                await delmsg.delete()
            else:
                delmsg = await ctx.send("値には2から50までのみ入れられます。")
        else:
            delmsg = await ctx.send("このコマンドは管理者のみ実行可能です。")
            await delmsg.delete()


@bot.command()
async def timem(ctx, arg):
    today = datetime.today()
    ago = today - timedelta(days=int(arg))
    async for message in ctx.message.channel.history(limit=1,before=ago):
        link = f"https://discordapp.com/channels/{str(ctx.message.guild.id)}/{str(ctx.message.channel.id)}/{str(message.id)}"
        embed = discord.Embed(description=f"{message.content}\n[メッセージに行く]({link})", color=0x0066ff)
        embed.set_author(name=message.author.display_name,
            icon_url=message.author.avatar_url_as(format="png"))
        embed.set_footer(text=f"{arg}日前のメッセージ | タイムマシン機能")
        await ctx.send(embed=embed)

@bot.command()
async def urlsm(ctx, arg):
    if True:
        url = arg
        turl = GET_Url("d129a315873450fa92f50d4a67dbe3c77821414e", url)
        await ctx.send(f"URLを短縮しました。\nURL:{turl}")

@bot.command()
async def test(ctx):
    if True:
        await ctx.send('開発者のためのテストメッセージ')

@bot.command()
async def info(ctx):
    if True:
        embed = discord.Embed(title=bname, description="どうも。RTというとあるBOT。\n翻訳機能、スタンプ機能、画像認証機能などあるよ。", color=0x0066ff)
        embed.add_field(name="サーバー数", value=len(bot.guilds))
        embed.add_field(name="サポートサーバー", value="[ここをクリック！](https://discord.gg/FJQNpe2)")
        embed.add_field(name="招待リンク", value="[ここをクリック!](https://discord.com/api/oauth2/authorize?client_id=716496407212589087&permissions=808839248&scope=bot)")
        await ctx.send(embed=embed)

@bot.command(alias="cr")
async def credit(ctx):
    embed = discord.Embed(title="クレジット", color=0x0066ff)
    embed.add_field(name="開発者", value="<:yaakiyu:731263096454119464> <@693025129806037003> [サーバー](https://discord.gg/zXPXtUw)\n<:takkun:731263181586169857> <@667319675176091659> [サーバー](https://discord.gg/VX7ceJw)\n<:tasren:731263470636498954> <@634763612535390209> [サイト](http://tasuren.syanari.com/)")
    embed.add_field(name="デザイン", value="<:yutam:732948166881575022> <@628879037275832330>\n<:omochi_nagamochi:733618053631311924> <@705083740694642819>")
    await ctx.send(embed=embed)

@bot.command()
async def staadd(ctx, arg):
    if True:
        wo = arg
        if r'\\' in wo or "/" in wo or "*" in wo or "?" in wo or '"' in wo or "<" in wo or ">" in wo or "|" in wo == True:
            await ctx.send(r'名前に \/:*?"<>| は使えません。')
            return
        await ctx.send("設定中...")
        picu = ctx.message.attachments[0].url
        file = f"RT/stamp/{ctx.guild.id}/{wo}.txt"
        try:
            os.mkdir(f"RT/stamp/{ctx.guild.id}")
        except FileExistsError:
            pass
        with open(file, mode='w') as f:
            f.write(str(picu))
        await ctx.send("スタンプを追加したよ")
        f.close()

@bot.command()
async def stadel(ctx, arg):
    if True:
        woo = arg
        file = f"RT/stamp/{ctx.guild.id}/{woo}.txt"
        if (os.path.exists(file)):
            await ctx.send("削除中...")
            os.remove(file)
            await ctx.send("スタンプを削除したよ")
        else:
            await ctx.send("そのスタンプが見つからなかった...")

@bot.command()
async def quit(ctx):
    if ctx.author.id in team_id:
        await ctx.send("BOTを再起動します")
        await bot.logout()

@bot.group()
async def ng(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("ngのあとにadd,dele,listを入れてください。\nわからない場合は`rt!help ng`と実行してください。")

@ng.command()
async def add(ctx, arg):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            sID = ctx.guild.id
            if str(sID) in str(testf):
                ngtxt = f"RT/nglist/{sID}.txt"
            else:#もしまだngリストファイルがなかったら
                await ctx.send("NGリストファイルを作っています...")
                ngtxt = f"RT/nglist/{sID}.txt"
                f = open(ngtxt, "w")
                f.close()
                testf.append(sID)
            with open(ngtxt) as f:
                nglist = f.read().splitlines()
            nglist = [a for a in nglist if a != '']
            word = arg
            print('add:' + str(word))
            print('NGワードを追加します')
            with open(ngtxt, mode='a') as f:
                f.write('\n' + str(word))
            with open(ngtxt) as f:
                nglist = f.read().splitlines()
            print('追加しました')
            await ctx.send('NGワードを追加したよ。')
            await ctx.message.delete()
            f.close()
        else:#管理者じゃなかったら
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@ng.command()
async def list(ctx,arg):
    if True:
        ngtxt = f"RT/nglist/{ctx.guild.id}.txt"
        if (os.path.exists(ngtxt)):
            with open(ngtxt) as f:
                nglist = f.read().splitlines()
            f.close()
            lis = [a for a in nglist if a != '']
            title = "NGワード一覧"
            ngg = arg
            pa = int(ngg)
            no = len(lis)
            embed = discord.Embed(title=title,description=f"{pa}ページ目 NGワードの数:{no}",color=0x4682b4)
            c = 0
            cc = 0
            if pa > 1:
                ccc = pa*10
                c = ccc - 10
            while True:
                try:
                    naiy = lis[c]
                except IndexError:
                    await ctx.send(f"{pa}ページ目はまだありません")
                    return
                c = c + 1
                embed.add_field(name=str(c),value=f"||{naiy}||")
                if c == pa * 10 or c == len(lis):
                    break
            await ctx.send(embed=embed)
        else:
            await ctx.send("まだNGワードが登録されていません。")

@ng.command()
async def dele(ctx, arg):
  dword = arg
  if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            ngtxt = f"RT/nglist/{ctx.guild.id}.txt"
            if (os.path.exists(ngtxt)):
                with open(ngtxt) as f:
                    nglist = f.read().splitlines()
                print(nglist)
                f.close()
            else:
                await ctx.send("NGリストファイルがまだ作られていません。\n`rt!ng add [NGワード]`コマンドでNGワードを追加してください。")
                await ctx.message.delete()
                return
            nglist = [a for a in nglist if a != '']
            true = dword in nglist
            if True == true:
                s = dword
                with open(ngtxt, 'r+') as f:  # 上書き
                    d = f.readlines()
                    f.seek(0)
                    for l in d:
                        if s not in l:
                            f.write(l)
                            f.truncate()
                with open(ngtxt) as f:
                    nglist = f.read().splitlines()
            await ctx.send('NGワードをリストから削除しました。')
            f.close()
        else:
            await ctx.send("このコマンドは管理者のみ実行可能です。")

@bot.group()
async def menu(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("menuのあとにm,s,vを入れてください。\nわからない場合は`rt!help menu`と実行してください。")
    
@menu.command()
async def m(ctx, arg):
    async with ctx.typing():
        if arg in ["New", "False"]:
            if arg == "False":
                with open(f"RT/server/rea2/{ctx.author.id}.txt", mode="w") as f:
                    f.write(arg)
                f.close()
                kek = f"メニュー設定を`{arg}`にしました。"
            if arg == "New":
                ra = randomname(4)
                with open(f"RT/server/rea2/{ctx.author.id}.txt", mode="w") as f:
                    f.write(ra)
                f.close()
                os.mkdir(f"RT/server/rea/{ra}")
                for s in range(8):
                    s = s + 1
                    fa = pathlib.Path(f"RT/server/rea/{ra}/{s}.txt")
                    fa.touch()
                kek = f"メニュー設定ファイルを設定名`{ra}`で作成しました。\n:one: :two: ...のﾘｱｸｼｮﾝで設定が終わったら`rt!menu v {ra}`と実行してください。"
        else:
            kek = "引数にはNewまたはFalseを入れてください。"
    await ctx.send(kek)
    
@menu.command()
async def s(ctx, arg):
    async with ctx.typing():
        if (os.path.exists(f"RT/server/rea/{arg}/")):
            with open(f"RT/server/rea2/{ctx.author.id}.txt", mode="w") as f:
                f.write(arg)
            f.close()
            kek = f"メニュー設定対象を`{arg}`にしました。"
        else:
            kek = f"その設定名のファイルはありませんでした。"
    await ctx.send(kek)

@menu.command()
async def v(ctx, arg):
    ke = 0
    async with ctx.typing():
        if (os.path.exists(f"RT/server/rea2/{ctx.author.id}.txt")):
            with open(f"RT/server/rea2/{ctx.author.id}.txt") as f:
                k = f.read()
            f.close()
            if k == "False":
                kek = f"メニュー設定が`False`になっています。\n`rt!menu m New`と実行してください。"
            else:
                if (os.path.exists(f"RT/server/rea/{arg}/1.txt")):
                    with open(f"RT/server/rea/{arg}/1.txt") as f:
                        kek = f.read()
                        ke = 1
                    f.close()
                    if kek == "" or kek is None:
                        ke = 0
                        kek = f"まだメッセージが設定されていません。\n:one: :two: などのリアクションを自分のメッセージにつけて設定してください。"
                else:
                    kek = "メニュー設定対象名が間違っています。"
        else:
            kek = f"メニュー設定ファイルがありません。\n`rt!menu m New`と実行してください。"
    if ke == 0:
        await ctx.send(kek)
    else:
        mes = await ctx.send(kek)
        async with ctx.typing():
            await mes.add_reaction("<:1_:726043030708158543")
            await mes.add_reaction("<:2_:726043030364356718")
            await mes.add_reaction("<:3_:726043030473146408")
            await mes.add_reaction("<:4_:726043030590586970")
            await mes.add_reaction("<:5_:726043030343123036")
            await mes.add_reaction("<:6_:726043030498574376")
            await mes.add_reaction("<:7_:726043030221750293")
            await mes.add_reaction("<:8_:726043030515220580")
        messs = await ctx.send("ﾒﾆｭｰﾒｯｾｰｼﾞ作成完了\n(数秒後このﾒｯｾｰｼﾞは消えます)")
        await asyncio.sleep(3)
        await messs.delete()

@bot.group()
async def stamp(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("stampのあとにadd,dele,listを入れてください。\nわからない場合は`rt!help stamp`と実行してください。")

@stamp.command()
async def add(ctx, arg):
    if True:
        wo = arg
        if r'\\' in wo or "/" in wo or "*" in wo or "?" in wo or '"' in wo or "<" in wo or ">" in wo or "|" in wo == True:
            await ctx.send(r'名前に \/:*?"<>| は使えません。')
            return
        await ctx.send("設定中...")
        picu = ctx.message.attachments[0].url
        file = f"RT/stamp/{ctx.guild.id}/{wo}.txt"
        try:
            os.mkdir(f"RT/stamp/{ctx.guild.id}")
        except FileExistsError:
            pass
        with open(file, mode='w') as f:
            f.write(str(picu))
        await ctx.send("スタンプを追加したよ")
        f.close()

@stamp.command()
async def dele(ctx, arg):
    if True:
        woo = arg
        file = f"RT/stamp/{ctx.guild.id}/{woo}.txt"
        if (os.path.exists(file)):
            await ctx.send("削除中...")
            os.remove(file)
            await ctx.send("スタンプを削除したよ")
        else:
            await ctx.send("そのスタンプが見つからなかった...")

@stamp.command()
async def list(ctx, arg):
    if True:
        if (os.path.exists("RT/stamp/" + str(ctx.guild.id))):
            lis = file_list("RT/stamp/" + str(ctx.guild.id))
        else:
            await ctx.send("まだスタンプがありません。")
            return
        pa = int(arg)
        no = len(lis)
        embed = discord.Embed(title="スタンプ一覧", description=f"{pa}ページ目\nスタンプの数:{len(lis)}", color=0x0066ff)
        c = 0
        cc = 0
        if pa > 1:
            ccc = pa*10
            c = ccc - 10
        while True:
            try:
                naiy = lis[c]
            except:
                if pa == 1:
                    await ctx.send("まだスタンプがありません。")
                    return
                await ctx.send(f"{pa}ページ目はまだありません")
                return
            c = c + 1
            with open(f"RT/stamp/{ctx.message.guild.id}/{naiy}.txt") as f:
                urll = f.read()
            f.close()
            embed.add_field(name=str(c), value=f"[{naiy}]({urll})")
            if c == pa * 10:
                await ctx.send(embed=embed)
                return
            if c == len(lis):
                break
        await ctx.send(embed=embed)

@bot.group()
async def gc(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("gcのあとにmake,cng,deleを入れてください。\nわからない場合は`rt!help gc`と実行してください。")

@gc.command()
async def make(ctx):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            with ctx.channel.typing():
                if (os.path.exists(f"RT/server/gc/{ctx.channel.name}.txt")):
                    await ctx.channel.send("このチャンネル名のグローバルチャットは既にあります。\n他の名前を使ってください。")
                    return
                aru = re.compile(r'[\\/:*?"<>|]+').search(ctx.channel.name)
                if aru:
                    await ctx.send(r'チャンネル名に \\/:*?"<> の文字は使えません。')
                    return
                print("グローバルチャットを作成します")
                with open(f"RT/server/gc/{ctx.channel.name}.txt", mode="w") as f:
                    f.write(str(ctx.channel.id))
                f.close()
                with open(f"RT/server/gc2/{ctx.channel.name}.txt", mode="w") as f:
                    f.write(str(ctx.message.author.id))
                f.close()
            await ctx.send(f"このチャンネルをグローバルチャットにしました。\nチャンネル名は変更しないでください。\n他のサーバーでこのグローバルチャットに接続するには`rt!gc cng {ctx.channel.name}`と実行してください。")

@gc.command()
async def cng(ctx, arg):
    if True:
        ss = False
        for s in ctx.message.author.roles:
            if s.name == "RT操作権限":
                ss = True
        if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
            name = arg
            if (os.path.exists(f"RT/server/gc/{name}.txt")):
                with open(f"RT/server/gc/{name}.txt", mode="a") as f:
                    ok = f.write(f"\n{ctx.channel.id}")
                f.close()
                await ctx.message.channel.edit(name=name)
            else:
                await ctx.send("そのグローバルチャットはありません。")
                return
            with open(f"RT/server/gc/{name}.txt") as f:
                l_strip = [s.strip() for s in f.readlines()]
            await ctx.send("このチャンネルをグローバルチャットとリンクしました。\nチャンネル名は変更しないでください。")
            for w in l_strip:
                if w == "":
                    continue
                channel = bot.get_channel(int(w))#client
                embed = discord.Embed(
                    title="お知らせ",
                    description=f"グローバルチャットに\n`{ctx.guild.name}`というサーバーが接続しました。",
                    color=0xffd900)
                await channel.send(embed=embed)
            f.close()

@gc.command()
async def dele(ctx):
    async with ctx.typing():
        if (os.path.exists(f"RT/server/gc2/{ctx.channel.name}.txt")):
            with open(f"RT/server/gc2/{ctx.channel.name}.txt") as f:
                o = f.read()
            f.close()
            if o == str(ctx.message.author.id):
                os.remove(f"RT/server/gc/{ctx.channel.name}.txt")
                os.remove(f"RT/server/gc2/{ctx.channel.name}.txt")
                kek = "グローバルチャットを削除しました。"
            else:
                kek = "グローバルチャット作成者のみこのコマンドは使用可能です。"
        else:
            kek = "このコマンドはグローバルチャットの中のみ使用可能です。"
    await ctx.send(kek)

@bot.command()
async def stalist(ctx, arg):
    if True:
        if (os.path.exists("RT/stamp/" + str(ctx.guild.id))):
            lis = file_list("RT/stamp/" + str(ctx.guild.id))
        else:
            await ctx.send("まだスタンプがありません。")
            return
        pa = int(arg)
        no = len(lis)
        embed = discord.Embed(title="スタンプ一覧", description=f"{pa}ページ目\nスタンプの数:{len(lis)}", color=0x0066ff)
        c = 0
        cc = 0
        if pa > 1:
            ccc = pa*10
            c = ccc - 10
        while True:
            try:
                naiy = lis[c]
            except:
                if pa == 1:
                    await ctx.send("まだスタンプがありません。")
                    return
                await ctx.send(f"{pa}ページ目はまだありません")
                return
            c = c + 1
            with open(f"RT/stamp/{ctx.message.guild.id}/{naiy}.txt") as f:
                urll = f.read()
            f.close()
            embed.add_field(name=str(c), value=f"[{naiy}]({urll})")
            if c == pa * 10:
                await ctx.send(embed=embed)
                return
            if c == len(lis):
                break
        await ctx.send(embed=embed)

@bot.group()
async def funp(ctx):
    if ctx.invoked_subcommand is None:
        if ctx.channel.is_nsfw():
            async with ctx.typing():
                lis = file_list("RT/funp/nsfw/")
                print(lis)
                file = random.choice(lis)
                with open(f"RT/funp/nsfw/{file}.txt") as f:
                    n = f.read()
                f.close()
                URL = line(n, 1)
                user = bot.get_user(int(line(n, 2)))
                embed = discord.Embed(title="みんなの画像-nsfw", description="通報する場合は<:report:732564857513312326> をクリック", color=0x0066ff)
                embed.set_author(name=user.display_name,
                    icon_url=user.avatar_url_as(format="png"))
                embed.set_image(url=URL)
            mes = await ctx.send(content=file, embed=embed)
            await mes.add_reaction("<:report:732564857513312326>")
        else:
            async with ctx.typing():
                lis = file_list("RT/funp/fun/")
                print(lis)
                file = random.choice(lis)
                with open(f"RT/funp/fun/{file}.txt") as f:
                    n = f.read()
                f.close()
                URL = line(n, 1)
                user = bot.get_user(int(line(n,2)))
                embed = discord.Embed(title="みんなの画像", description="通報する場合は<:report:732564857513312326> をクリック", color=0x0066ff)
                embed.set_author(name=user.display_name,
                    icon_url=user.avatar_url_as(format="png"))
                embed.set_image(url=URL)
            mes = await ctx.send(content=file, embed=embed)
            await mes.add_reaction("<:report:732564857513312326>")

@funp.command()
async def see(ctx, arg):
    async with ctx.typing():
        embed = None
        if ctx.channel.is_nsfw(): 
            if (os.path.exists(f"RT/funp/nsfw/{arg}.txt")):
                with open(f"RT/funp/nsfw/{arg}.txt") as f:
                    n = f.read()
                f.close()
                URL = line(n, 1)
                user = bot.get_user(int(line(n,2)))
                embed = discord.Embed(title="みんなの画像-nsfw", description="通報する場合は<:report:732564857513312326> をクリック", color=0x0066ff)
                embed.set_author(name=user.display_name,
                    icon_url=user.avatar_url_as(format="png"))
                embed.set_image(url=URL)
                kek = arg
            else:
                kek = "その名前の画像は見つかりませんでした。"
        else:
            if (os.path.exists(f"RT/funp/fun/{arg}.txt")):
                with open(f"RT/funp/fun/{arg}.txt") as f:
                    n = f.read()
                f.close()
                URL = line(n, 1)
                user = bot.get_user(int(line(n,2)))
                embed = discord.Embed(title="みんなの画像", description="通報する場合は<:report:732564857513312326> をクリック", color=0x0066ff)
                embed.set_author(name=user.display_name,
                    icon_url=user.avatar_url_as(format="png"))
                embed.set_image(url=URL)
                kek = arg
            else:
                kek = "その名前の画像は見つかりませんでした。"
    if embed is None:
        mes = await ctx.send(content=kek)
    else:
        mes = await ctx.send(content=kek, embed=embed)
    await mes.add_reaction("<:report:732564857513312326>")

@funp.command()
async def add(ctx, arg):
    aru = re.compile(r'[\\/:*?"<>|]+').search(arg)
    if aru:
        await ctx.send(r'画像名に \\/:*?"<> の文字は使えません。')
        return
    async with ctx.typing():
        if ctx.channel.is_nsfw(): 
            if (os.path.exists(f"RT/funp/nsfw/{arg}.txt")):
                kek = "すみません。その名前は既に使われています。"
            else:
                with open(f"RT/funp/nsfw/{arg}.txt", mode="w") as f:
                    f.write(f"{ctx.message.attachments[0].url}\n{ctx.message.author.id}")
                f.close()
                kek = "画像を登録しました。"
        else:
            if (os.path.exists(f"RT/funp/fun/{arg}.txt")):
                kek = "すみません。その名前は既に使われています。"
            else:
                with open(f"RT/funp/fun/{arg}.txt", mode="w") as f:
                    f.write(f"{ctx.message.attachments[0].url}\n{ctx.message.author.id}")
                f.close()
                kek = "画像を登録しました。"
    await ctx.send(kek)

@funp.command()
async def list(ctx, arg):
    if ctx.channel.is_nsfw():
        lis = file_list("RT/funp/nsfw/")
        pa = int(arg)
        no = len(lis)
        embed = discord.Embed(title="funp画像一覧 NSFW", description=f"{pa}ページ目\nfunpの数:{len(lis)}", color=0x0066ff)
        c = 0
        cc = 0
        if pa > 1:
            ccc = pa*10
            c = ccc - 10
        while True:
            try:
                naiy = lis[c]
            except:
                if pa == 1:
                    await ctx.send("まだfunpがありません。")
                    return
                await ctx.send(f"{pa}ページ目はまだありません")
                return
            c = c + 1
            with open(f"RT/funp/nsfw/{naiy}.txt") as f:
                urll = f.read()
            f.close()
            embed.add_field(name=str(c), value=f"[{naiy}]({line(urll, 1)})")
            if c == pa * 10:
                await ctx.send(embed=embed)
                return
            if c == len(lis):
                break
        await ctx.send(embed=embed)
    else:
        lis = file_list("RT/funp/fun/")
        pa = int(arg)
        no = len(lis)
        embed = discord.Embed(title="funp画像一覧", description=f"{pa}ページ目\nfunpの数:{len(lis)}", color=0x0066ff)
        c = 0
        cc = 0
        if pa > 1:
            ccc = pa*10
            c = ccc - 10
        while True:
            try:
                naiy = lis[c]
            except:
                if pa == 1:
                    await ctx.send("まだfunpがありません。")
                    return
                await ctx.send(f"{pa}ページ目はまだありません")
                return
            c = c + 1
            with open(f"RT/funp/fun/{naiy}.txt") as f:
                urll = f.read()
            f.close()
            embed.add_field(name=str(c), value=f"[{naiy}]({line(urll, 1)})")
            if c == pa * 10:
                await ctx.send(embed=embed)
                return
            if c == len(lis):
                break
        await ctx.send(embed=embed)

@bot.command()
async def report(ctx, arg, *, arg2):
    async with ctx.typing():
        channel = bot.get_channel(732567078531498075)
        embed = discord.Embed(title="通報-funp", description=f"```\n画像名:\n{arg}\n理由:\n{arg2}\n```", color=0x0066ff)
        embed.set_author(name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url_as(format="png"))
        await channel.send(embed=embed)
    await ctx.send("通報しました。ご協力ありがとうございます。")

@bot.group()
async def ocom(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("ocomにはサブコマンドがあります。add,dele,listをocomのあとにつけてください。")

@ocom.command()
async def add(ctx, arg, *, arg2):
    ss = False
    for si in ctx.message.author.roles:
        if si.name == "RT操作権限":
            ss = True
    if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
        aru = re.compile(r'[\\/:*?"<>|]+').search(arg)
        if aru:
            await ctx.send(r'コマンドに \\/:*?"<> の文字は使えません。')
            return
        async with ctx.typing():
            path = f"RT/server/command/{ctx.message.guild.id}/"
            if (os.path.exists(path)):
                with open(f"{path}{arg}.txt", mode="w") as f:
                    f.write(arg2)
                f.close()
                kek = "コマンドを追加しました。"
            else:
                os.mkdir(path)
                with open(f"{path}{arg}.txt", mode="w") as f:
                    f.write(arg2)
                f.close()
                kek = "コマンドを追加しました。"
        await ctx.send(kek)

@ocom.command()
async def dele(ctx, arg):
    ss = False
    for si in ctx.message.author.roles:
        if si.name == "RT操作権限":
            ss = True
    if ctx.author.guild_permissions.administrator or ctx.author.id == team_id or ss == True:
        async with ctx.typing():
            path = f"RT/server/command/{ctx.message.guild.id}/"
            if (os.path.exists(path)):
                if (os.path.exists(f"{path}{arg}.txt")):
                    os.remove(f"{path}{arg}.txt")
                    kek = "コマンドを削除しました。"
                else:
                    kek = "コマンドが見つかりませんでした。"
            else:
                kek = "まだコマンドが追加されてません。"
        await ctx.send(kek)

@ocom.command()
async def list(ctx, arg):
    if True:
        path = f"RT/server/command/{ctx.message.guild.id}/"
        if (os.path.exists(path)):
            lis = file_list(path)
        else:
            await ctx.send("まだコマンドがありません。")
            return
        pa = int(arg)
        no = len(lis)
        embed = discord.Embed(title="コマンド一覧", description=f"{pa}ページ目\nコマンドの数:{len(lis)}", color=0x0066ff)
        c = 0
        cc = 0
        if pa > 1:
            ccc = pa*10
            c = ccc - 10
        while True:
            try:
                naiy = lis[c]
            except:
                if pa == 1:
                    await ctx.send("まだコマンドがありません。")
                    return
                await ctx.send(f"{pa}ページ目はまだありません")
                return
            c = c + 1
            embed.add_field(name=str(c), value=str(naiy))
            if c == pa * 10:
                await ctx.send(embed=embed)
                return
            if c == len(lis):
                break
        await ctx.send(embed=embed)

@bot.command()
async def level(ctx):
    async with ctx.typing():
        if str(ctx.message.author.id) in levels:
            cur_lvl = levels[str(ctx.message.author.id)]["level"]
            exp = levels[str(ctx.message.author.id)]["exp"]
            kek = f"<:LVUP:734358675736625202>レベル:{cur_lvl}\n:chart:経験値:{exp}"
        else:
            kek = "<:LVUP:734358675736625202>レベル:0LV\n:chart:経験値:0"
    await ctx.send(kek)

@bot.group()
async def exmoji(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("exmojiにはサブコマンドがあり、add,dele,listをexmojiの後に追加しなければなりません。\nわからない場合は`rt!help exmoji`をチェック！")

@exmoji.command()
async def add(ctx, arg, *, arg2=None):
    async with ctx.typing():
        if emojis[str(ctx.guild.id)] is None:
            emojis[str(ctx.message.guild.id)] = {}
        ireru = arg2
        if arg2 is None:
            if ctx.message.attachments is not None:
                ireru = ctx.message.attachments[0].url
            else:
                ireru = ""
        emojis[str(ctx.message.guild.id)][arg] = ireru
        with open('RT/emojis.json', 'w') as f:
            json.dump(emojis, f, indent=4)
    await ctx.send("ExMOJIを登録！")

@exmoji.command()
async def dele(ctx, arg):
    if emojis[str(ctx.message.guild.id)] is None:
        kek = "まだ絵文字が登録されていません。"
    else:
        fafafa = emojis[str(ctx.message.guild.id)][arg]
    if fafafa is not None:
        emojis[str(ctx.message.guild.id)].pop(arg)
        with open('RT/emojis.json', 'w') as f:
            json.dump(emojis, f, indent=4)
        kek = "削除しました。"
    else:
        kek = "その絵文字が見つかりませんでした。"
    await ctx.send(kek)

@exmoji.command()
async def list(ctx, arg):
    if emojis[str(ctx.guild.id)] is not None:
        lis = emojis[str(ctx.guild.id)]
        pa = int(arg)
        no = len(lis)
        embed = discord.Embed(title="ExMOJI一覧", description=f"{pa}ページ目\nExMOJIの数:{len(lis)}\nすみません！開発中です", color=0x0066ff)
        print(lis)
        await ctx.send(embed=embed)
    else:
        await ctx.send("まだExMOJIがありません。")

@bot.event#コマンドじゃないよ
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    if message.content == f"{pr}help":
        async with message.channel.typing():
            with open("RT/help/1.txt", encoding="utf-8_sig") as f:
                nai = f.read()
            embed = discord.Embed(title="RTコマンドリスト",
                description=f"**Helpの使い方**\n詳細を知りたい場合は`rt!help [コマンド名]`と実行してください。\nわからないことがあれば[サポートサーバー](https://discord.gg/FJQNpe2)に来てください。",
                color=0x0066ff)
            name = line(nai, 1)
            nai = nai.replace(name, "")
            embed.add_field(name=name, value=nai)
        mes = await message.channel.send(content="1/4", embed=embed)
        for s in ["<:hidari:731730013329817600>", "<:migi:731730012943941683>"]:
            await mes.add_reaction(s)
        f.close()

    fa = re.compile(f"{pr}help (.+)").search(message.content)
    if fa:
        async with message.channel.typing():
            arg = fa.group(1)
            if (os.path.exists(f"RT/help/{arg}.txt")):
                with open(f"RT/help/{arg}.txt", encoding="utf-8_sig") as f:
                    kek = f.read()
                f.close()
                embed = discord.Embed(title=arg, description=kek, color=0x0066ff)
            else:
                embed = discord.Embed(title="RT ヘルプ", description="そのコマンドはありません。", color=0x0066ff)
        await message.channel.send(embed=embed)

    path = f"RT/server/command/{message.guild.id}/"
    if (os.path.exists(f"{path}{message.content}.txt")):
        async with message.channel.typing():
            with open(f"{path}{message.content}.txt") as f:
                naaai = f.read()
            f.close()
        await message.channel.send(naaai)

    if message.guild is False:
        return

    if message.content.startswith("rt!"):
        return

    if message.content.startswith("r2!"):
        return

    global levels
    global emojis
    nochlist = ["spam","スパム","spaming","レベル上げ用","レベル上げ"]

    try:
        fa = message.channel.name
    except:
        return

    mess = message.content
    if True:
        if message.channel.name == "認証-rt":
            if len(message.content) == 8:
                if (os.path.exists(f"RT/server/pic/{message.guild.id}")):
                    with open(f"RT/server/pic/{message.guild.id}/{message.author.id}.txt") as f:
                        na = f.read()
                    f.close()
                    if na == message.content:
                        with open(f"RT/server/pic/{message.guild.id}.txt") as f:
                            role = f.read()
                        role = discord.utils.find(lambda r: r.name == role, message.guild.roles)
                        try:
                            await message.author.add_roles(role)
                        except:
                            try:
                                await message.channel.send(f"エラー:認証は成功しましたが、役職をつけれませんでした...\nつける役職`{role.name}`の位置をRTの役職より下に配置してください。")
                            except:
                                await message.channel.send("エラー:認証は成功しましたが、役職をつけれませんでした...\nつける役職の名前が正しくありません。\n`rt!cpic 役職の名前`で設定しなおしてください。")
                            return
                        await message.channel.send("認証に成功したので役職をつけました。")
                        os.remove(f"RT/server/pic/{message.guild.id}/{message.author.id}.txt")
                        return
                    else:
                        await message.channel.send("コードが違います。")
                else:
                    await message.channel.send("コードが違います。")

    if mess.count("!") == 2:
        x = mess.find("!")
        y = mess.find("!", x+2)
        sta = mess[x + 1 : y]
        if sta == None:
            return
        else:
            pas = f"RT/stamp/{message.guild.id}/{sta}.txt"
            if os.path.exists(pas) == False:
                pass
            else:
                with open(pas) as f:
                    url = f.read()
                await message.channel.send(url)

    if (os.path.exists(f"RT/server/gc/{message.channel.name}.txt")):#グローバルチャット
        with open(f"RT/server/gc/{message.channel.name}.txt") as f:
            l_strip = [s.strip() for s in f.readlines()]
        hub = l_strip
        print(l_strip)
        l_strip.remove(str(message.channel.id))
        if message.attachments == []:
            for w in l_strip:
                if w == "":
                    continue
                channel = bot.get_channel(int(w))
                try:
                    n = 0
                    na = f"Global-{message.channel.name}"
                    if (os.path.exists(f"RT/server/gc/web/{channel.id}.txt")):
                        with open(f"RT/server/gc/web/{channel.id}.txt") as f:
                            web = f.read()
                        f.close()
                    else:
                        webhook_data = await channel.create_webhook(name=na)
                        with open(f"RT/server/gc/web/{channel.id}.txt", mode="w") as f:
                            f.write(webhook_data.url)
                        f.close()
                        n = 1
                    if n == 1:
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(webhook_data.url,adapter=AsyncWebhookAdapter(session))
                            await webhook.send(content=message.content,username=f"{message.author.display_name}/{message.author.id}",avatar_url=message.author.avatar_url_as(format="png"))
                    else:
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(web,adapter=AsyncWebhookAdapter(session))
                            await webhook.send(content=message.content,username=f"{message.author.display_name}/{message.author.id}",avatar_url=message.author.avatar_url_as(format="png"))
                except AttributeError:
                    pass
        else:
            for w in l_strip:
                if w == "":
                    continue
                channel = bot.get_channel(int(w))
                picu = message.attachments[0].url
                try:
                    n = 0
                    na = f"Global-{message.channel.name}"
                    if (os.path.exists(f"RT/server/gc/web/{channel.id}.txt")):
                        with open(f"RT/server/gc/web/{channel.id}.txt") as f:
                            web = f.read()
                        f.close()
                    else:
                        webhook_data = await channel.create_webhook(name=na)
                        with open(f"RT/server/gc/web/{channel.id}.txt", mode="w") as f:
                            f.write(webhook_data.url)
                        f.close()
                        n = 1
                    if n == 1:
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(webhook_data.url,adapter=AsyncWebhookAdapter(session))
                            await webhook.send(content=f"{message.content}\n{picu}",username=f"{message.author.display_name}/{message.author.id}",avatar_url=message.author.avatar_url_as(format="png"))
                    else:
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(web,adapter=AsyncWebhookAdapter(session))
                            await webhook.send(content=f"{message.content}\n{picu}",embed=embed,username=f"{message.author.display_name}/{message.author.id}",avatar_url=message.author.avatar_url_as(format="png"))
                except AttributeError:
                    pass
        await message.add_reaction("<:check:733607564163678230")
        f.close()

    if message.channel.name == "投票-rt":
        await message.add_reaction("<:good:717339022699003904")
        await message.add_reaction("<:bad:717339050276814888")

    # --メンション禁止機能--
    add = 0
    if (os.path.exists(f"RT/server/eve/{message.guild.id}.txt")):
        with open(f"RT/server/eve/{message.guild.id}.txt") as f:
            tr = f.read()
        f.close()
    else:
        tr = "False"
    if tr == "True":
        str1 = message.content
        nglistt = ["@everyone", "@here"]
        listno = len(nglistt)
        for index, w in enumerate(nglistt):
            nghen = nglistt[index]
            tr = str1.find(nghen)
            if not tr <= -1 and nghen != '':
                ngword = message.content
                msg = []
                msg.append(ngword)
                try:  # 権限がなかったりした場合エラーが発生するためtryを配置
                    await message.delete()
                except:
                    embe = discord.Embed(title="全員メンションを発見しました。\nですが削除権限がないまたはエラーが発生して削除できませんでした。\nすいません！", description=f"発言者:{message.author.mention}", color=0xff4242)
                    embe.set_footer(text="全員メンション禁止機能NGワード機能")
                    with open("error_log.txt") as f:
                        n = f.read()
                    n = f"\n-=-=-=-=-=-=-=-=-=-=-=-=\n[ERROR]\n{sys.exc_info()}"
                    with open("error_log.txt", mode="w") as f:
                        f.write(n)
                    f.close()
                    add = 1
                embed = discord.Embed(title="全員メンションがあったので削除しました。", description=f"発言者:{message.author.mention}", color=0xff4242)
                embed.set_footer(text="全員メンション禁止機能")
                await message.channel.send(embed=embed)
                if add == 0:
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(embed=embe)

    # --NGワード機能--
    ad = 0
    sID = message.guild.id
    ngtxt = f"RT/nglist/{sID}.txt"
    if (os.path.exists(ngtxt)):
        with open(ngtxt) as f:
            nglist = f.read().splitlines()
        f.close()
        str1 = message.content
        listno = len(nglist)
        for index, w in enumerate(nglist):
            nghen = nglist[index]
            tr = str1.find(nghen)
            if not tr <= -1 and nghen != '':
                ngword = message.content
                msg = []
                msg.append(ngword)
                try:  # 権限がなかったりした場合エラーが発生するためtryを配置 fa
                    await message.delete()
                except:
                    print("")
                    embe = discord.Embed(title="NGワードを発見しました。\nですが削除権限がないまたはエラーが発生して削除できませんでした。\nすいません！", description=f"発言者:{message.author.mention}\n発言内容:||{message.content}||", color=0xff4242)
                    embe.set_footer(text="NGワード機能")
                    with open("RT/error_log.txt") as f:
                        n = f.read()
                    n = f"\n-=-=-=-=-=-=-=-=-=-=-=-=\n[ERROR]\n{sys.exc_info()}"
                    with open("error_log.txt", mode="w") as f:
                        f.write(n)
                    f.close()
                    ad = 1
                embed = discord.Embed(title="NGワードを発見したから削除したよ。", description=f"発言者:{message.author.mention}\n発言内容:||{message.content}||", color=0xff4242)
                embed.set_footer(text="NGワード機能")
                if ad == 0:
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(embed=embe)

    trr = re.compile(">>(.+)\n(.+)").search(message.content)
    if trr:
        async with message.channel.typing():
            title = trr.group(1)
            des = message.content.replace(f">>{title}\n", "")
            if mess.count(";;") == 2:
                x = mess.find(";;")
                y = mess.find(";;", x+3)
                sta = mess[x + 2 : y]
                if sta is None:
                    embed = discord.Embed(title=title, description=des,
                        color=0x0066ff)
                else:
                    des = des.replace(f";;{sta};;", "")
            embed = discord.Embed(title=title, description=des,
                        color=0x0066ff)
            try:
                if sta is None:
                    pass
                else:
                    embed.set_footer(text=sta)
            except:
                pass
            embed.set_author(name=message.author.display_name,
                icon_url=message.author.avatar_url_as(format="png"))
            if message.attachments == []:
                pass
            else:
                picu = message.attachments[0].url
                embed.set_image(url=picu)
        await message.channel.send(embed=embed)
        await message.delete()

    if not message.channel.name in nochlist:
        if not str(message.author.id) in levels:
            levels[str(message.author.id)] = {}
            levels[str(message.author.id)]["level"] = 0
            levels[str(message.author.id)]["exp"] = 0
        levels[str(message.author.id)]["exp"] += 1
        cur_lvl = levels[str(message.author.id)]["level"]
        exp = levels[str(message.author.id)]["exp"]
        if exp >= round((4 * (cur_lvl ** 3)) / 5):
            levels[str(message.author.id)]["level"] += 1
            await message.add_reaction("<:LVUP:734358675736625202>")
        with open('RT/level.json', 'w') as f:
            json.dump(levels, f, indent=4)

    if not str(message.guild.id) in emojis:
        emojis[str(message.guild.id)] = {}
    else:
        for fafa in extract_emojis(message.content):
            if  fafa in emojis[str(message.guild.id)].keys():
                mozi = emojis[str(message.guild.id)][fafa]
                if mozi is not None:
                    await message.channel.send(mozi)

    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    url_list = re.findall(pattern, message.content)
    if url_list != []:
        await message.add_reaction("<:URL2SM:717984572498903080")
        await asyncio.sleep(3.5)
        try:
            await message.remove_reaction("<:URL2SM:717984572498903080", bot.user)
        except discord.errors.NotFound:
            pass

    ss = False
    for s in message.author.roles:
        if s.name == "RT操作権限":
            ss = True
    if message.author.guild_permissions.administrator or message.author.id == team_id or ss == True:
        if mess.count("$**役職パネルrt**$") > 0:
            for i in range(mess.count("\n")+1):
                ee = line(mess, i)
                try:
                    await message.add_reaction(ee[:1])
                except:
                    pass

    if mess.count("\n") >= 10:
        try:
            cha = discord.utils.get(message.guild.text_channels, name="長文置き場-rt")
        except AttributeError:
            pass
        if cha is not None:
            await message.add_reaction("<:2Small:719445191039385631")
            await asyncio.sleep(3.5)
            try:
                await message.remove_reaction("<:2Small:719445191039385631", bot.user)
            except discord.errors.NotFound:
                print("例外")

    tr = re.compile("[a-zA-Z]").search(message.content)
    if tr:
        fil = f"RT/server/tran/{message.guild.id}.txt"
        if (os.path.exists(fil)):
            with open(fil) as f:
                t = f.read()
            f.close()
            if t == "True":
                try:
                    await message.add_reaction("<:EJP:732940339207340064")#client<:EJP:732940339207340064 732940339207340064
                    await asyncio.sleep(3.5)
                    await message.remove_reaction("<:EJP:732940339207340064", bot.user)
                except discord.errors.NotFound:
                    print("例外")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    s = reaction.message.content
    channel = bot.get_channel(reaction.message.channel.id)

    if reaction.emoji == "❤️":
        pat = f"RT/profile/good/{str(reaction.message.author.id)}.txt"
        if (os.path.exists(pat)):
            pass
        else:
            with open(pat, mode="w") as f:
                f.write("True")
        with open(pat) as f:
            tr = f.read()
        f.close()
        link = f"https://discordapp.com/channels/{str(reaction.message.guild.id)}/{str(reaction.message.channel.id)}/{str(reaction.message.id)}"
        if tr == "True":
            dm = bot.get_user(reaction.message.author.id)
            embed = discord.Embed(title="いいね通知",
                description=f"あなたのメッセージにいいねが付きました。\n[メッセージに行く]({link})",
                color=0x0066ff)
            embed.set_author(name=reaction.message.author.display_name,
                icon_url=reaction.message.author.avatar_url_as(format="png"))
            try:
                await dm.send(embed=embed)
                await dm.send("この通知を消したい場合は`rt!gooddm [True/False]`と実行してください。\nTrueにすると通知がONになります。")
            except:
                print("pass")
        try:
            cha = discord.utils.get(reaction.message.guild.text_channels, name="いいねリスト-rt")
        except AttributeError:
            cha = "None"
        if cha != "None":
            embed = discord.Embed(title="いいねされたメッセージ",
                description=f"{reaction.message.content}\n[メッセージに行く]({link})",
                color=0x0066ff)
            embed.set_author(name=reaction.message.author.display_name,
                icon_url=reaction.message.author.avatar_url_as(format="png"))
            await cha.send(embed=embed)
    
    if type(reaction.emoji) is str:
        return

    if reaction.emoji.id == 734358675736625202:
        if user.id == reaction.message.author.id:
            cur_lvl = levels[str(reaction.message.author.id)]["level"]
            exp = levels[str(reaction.message.author.id)]["exp"]
            await user.send(f"<:LVUP:734358675736625202>レベル:{cur_lvl}\n:chart:経験値:{exp}")

    if reaction.emoji.id == 731730013329817600:
        await reaction.message.remove_reaction("<:hidari:731730013329817600>", user)
        num = int(s[0])
        if num != 1:
            with open(f"RT/help/{num-1}.txt", encoding="utf-8_sig") as f:
                nai = f.read()
            embed = discord.Embed(title="RTコマンドリスト",
                description=f"**Helpの使い方**\n詳細を知りたい場合は`rt!help [コマンド名]`と実行してください。\nわからないことがあれば[サポートサーバー](https://discord.gg/FJQNpe2)に来てください。",
                color=0x0066ff)
            name = line(nai, 1)
            nai = nai.replace(name, "")
            embed.add_field(name=name, value=nai)
            await reaction.message.edit(content=f"{num-1}/4", embed=embed)

    if reaction.emoji.id == 731730012943941683:
        await reaction.message.remove_reaction("<:migi:731730012943941683>", user)
        num = int(s[0])
        if num != 4:
            with open(f"RT/help/{num+1}.txt", encoding="utf-8_sig") as f:
                nai = f.read()
            embed = discord.Embed(title="RTコマンドリスト",
                description=f"**Helpの使い方**\n詳細を知りたい場合は`rt!help [コマンド名]`と実行してください。\nわからないことがあれば[サポートサーバー](https://discord.gg/FJQNpe2)に来てください。",
                color=0x0066ff)
            name = line(nai, 1)
            nai = nai.replace(name, "")
            embed.add_field(name=name, value=nai)
            await reaction.message.edit(content=f"{num+1}/4", embed=embed)

    try:
        if reaction.count >= 2 and reaction.emoji.id == 732940339207340064:
            if False:#本番はreaction.count >= 3に入れ替える
                pass
            else:
                tran = translator.translate(s, dest="ja")
                embed = discord.Embed(title="翻訳:",
                    description=tran.text,
                    color=0x0066ff)
                embed.set_footer(text="Powered by GoogleTranslate")
                await channel.send(embed=embed)
                await reaction.message.remove_reaction("<:EJP:732940339207340064", user)
    except AttributeError:
        pass
                
    try:
        if reaction.count >= 2 and reaction.emoji.id == 717984572498903080:
            if False:
                pass
            else:
                pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
                url_list = re.findall(pattern, s)
                url_list[0]
                mes = s.replace(url_list[0], '')
                parsed_url = urlparse(url_list[0])
                embed = discord.Embed(title=f"{mes}",
                    description=f"URLコンパクト\n[URL先に行く]({url_list[0]})",
                    color=0x0066ff)
                embed.set_author(name=reaction.message.author.display_name,
                    icon_url=reaction.message.author.avatar_url_as(format="png"))
                embed.set_footer(text=f"{parsed_url.netloc}")
                await channel.send(embed=embed)
                await reaction.message.delete()
    except AttributeError:
        pass

    try:
        if reaction.count >= 2 and reaction.emoji.id == 719445191039385631:
            if False:
                pass
            else:
                try:
                    cha = discord.utils.get(reaction.message.guild.text_channels, name="長文置き場-rt")
                except AttributeError:
                    pass
                if cha is not None:
                    messa = await cha.send(f"発言者:{reaction.message.author.display_name}\n内容:\n{s}")
                    embed = discord.Embed(description=f"長文コンパクト化\n[長文を見る]({messa.jump_url})",
                    color=0x0066ff)
                    embed.set_author(name=reaction.message.author.display_name,
                        icon_url=reaction.message.author.avatar_url_as(format="png"))
                    embed.set_footer(text="長文コンパクト機能")
                    await reaction.message.delete()
                    await channel.send(embed=embed)
    except AttributeError:
        pass
                    
    try:
        if reaction.count >= 2 and reaction.emoji.id == 721338408693399665:
            if user.guild_permissions.administrator or user.id in team_id:
                if True:
                    paa = f"RT/server/eve/{reaction.message.guild.id}.txt"
                    if (os.path.exists(paa)):
                        with open(paa) as d:
                            a = d.read()
                        d.close()
                    else:
                        a = "False"
                    if "True" == a:
                        with open(paa, mode="w") as f:
                            f.write("False")
                    else:
                        with open(paa, mode="w") as f:
                            f.write("True")
                    f.close()
                    await reaction.message.edit(embed=vse(reaction.message))
                    await reaction.message.remove_reaction("<:atto:721338408693399665", user)
    except AttributeError:
        pass

    try:
        if reaction.count >= 2 and reaction.emoji.id == 721340045553827840:
            if user.guild_permissions.administrator or user.id in team_id:
                if True:
                    paa = f"RT/server/tran/{reaction.message.guild.id}.txt"
                    if (os.path.exists(paa)):
                        with open(paa) as d:
                            a = d.read()
                        d.close()
                    else:
                        a = "False"
                    if "True" == a:
                        with open(paa, mode="w") as f:
                            f.write("False")
                    else:
                        with open(paa, mode="w") as f:
                            f.write("True")
                    f.close()
                    await reaction.message.edit(embed=vse(reaction.message))
                    await reaction.message.remove_reaction("<:eng2jaof:721340045553827840", user)
    except AttributeError:
        pass

@bot.event
async def on_raw_reaction_remove(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    member = discord.utils.find(lambda m: m.id == payload.user_id, message.guild.members)
    s = message.content
    raw_id = s[0:4]

    try:
        if payload.member == bot.user:
            return
    except:
        pass

    ss = False
    for si in message.author.roles:
        if si.name == "RT操作権限":
            ss = True
    if message.author.guild_permissions.administrator or message.author.id == team_id or ss == True:
        if s.count("$**役職パネルrt**$") > 0:
            for i in range(s.count("\n")+1):
                ee = line(s, i)
                if ee.count(payload.emoji.name) > 0:
                    role_name = ee.replace(payload.emoji.name, "") 
                    role_name = role_name.replace(" ", "")
                    role = discord.utils.find(lambda r: r.name == role_name, message.guild.roles)
                    if role is None:
                        await user.send("__**役職剥奪失敗:**__\n役職をつけれませんでした...\n剥奪する役職の名前が正しくありません。\nサーバーの管理者に役職名があってるか確認してもらってください。")
                    else:
                        if True:
                            await member.remove_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    member = discord.utils.find(lambda m: m.id == payload.user_id, message.guild.members)
    s = message.content
    raw_id = s[0:4]

    try:
        if member == bot.user:
            return
    except:
        pass

    ss = False
    for si in message.author.roles:
        if si.name == "RT操作権限":
            ss = True
    if message.author.guild_permissions.administrator or message.author.id == team_id or ss == True:
        if s.count("$**役職パネルrt**$") > 0:
            for i in range(s.count("\n")+1):
                ee = line(s, i)
                if ee.count(payload.emoji.name) > 0:
                    role_name = ee.replace(payload.emoji.name, "") 
                    role_name = role_name.replace(" ", "")
                    role = discord.utils.find(lambda r: r.name == role_name, message.guild.roles)
                    if role is None:
                        await user.send("__**役職付与失敗:**__\n役職をつけれませんでした...\nつける役職の名前が正しくありません。\nサーバーの管理者に役職名があってるか確認してもらってください。")
                    else:
                        try:
                            await payload.member.add_roles(role)
                        except:
                            await user.send(f"__**役職付与失敗:**__\n役職をつけれませんでした...\nサーバーの管理者につける役職`{role.name}`の位置をRTの役職より下に配置してもらってください。")

    if payload.emoji.id == 732564857513312326:
        embed = discord.Embed(title="通報ボタンが押されました。", description=f"本当に通報する場合は`rt!report {message.content} [理由]`と実行してください。", color=0x0066ff)
        await user.send(embed=embed)
        await message.remove_reaction("<:report:732564857513312326>", payload.member)

    emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣" ,"8️⃣"]
    if payload.emoji.name in emoji:
        if (os.path.exists(f"RT/server/rea2/{payload.user_id}.txt")):
            with open(f"RT/server/rea2/{payload.user_id}.txt") as f:
                id = f.read()
            f.close()
            if id != "False":
                if payload.emoji.name == "1️⃣":
                    with open(f"RT/server/rea/{id}/1.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("1️⃣", payload.member)
                
                if payload.emoji.name == "2️⃣":
                    with open(f"RT/server/rea/{id}/2.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("2️⃣", payload.member)

                if payload.emoji.name == "3️⃣":
                    with open(f"RT/server/rea/{id}/3.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("3️⃣", payload.member)

                if payload.emoji.name == "4️⃣":
                    with open(f"RT/server/rea/{id}/4.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("4️⃣", payload.member)
                
                if payload.emoji.name == "5️⃣":
                    with open(f"RT/server/rea/{id}/5.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("5️⃣", payload.member)

                if payload.emoji.name == "6️⃣":
                    with open(f"RT/server/rea/{id}/6.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("6️⃣", payload.member)

                if payload.emoji.name == "7️⃣":
                    with open(f"RT/server/rea/{id}/7.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904")
                    await message.remove_reaction("7️⃣", payload.member)

                if payload.emoji.name == "8️⃣": 
                    with open(f"RT/server/rea/{id}/8.txt", mode="w") as f:
                        f.write(f"{id}\n>>> `発言者:{message.author.display_name}`\n{s}")
                    f.close()
                    await message.add_reaction("<:good:717339022699003904") 
                    await message.remove_reaction("8️⃣", payload.member)
                      
    if payload.member == bot.user:
        return
    
    if raw_id is None or raw_id == "":
        return
    
    if payload.emoji.id == 726043030708158543:
        with open(f"RT/server/rea/{raw_id}/1.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:1_:726043030708158543", payload.member)

    if payload.emoji.id == 726043030364356718:
        with open(f"RT/server/rea/{raw_id}/2.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:2_:726043030364356718", payload.member)
        
    if payload.emoji.id == 726043030473146408:
        with open(f"RT/server/rea/{raw_id}/3.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:3_:726043030473146408", payload.member)

    if payload.emoji.id == 726043030590586970:
        with open(f"RT/server/rea/{raw_id}/4.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:4_:726043030590586970", payload.member)

    if payload.emoji.id == 726043030343123036:
        with open(f"RT/server/rea/{raw_id}/5.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:5_:726043030343123036", payload.member)
        
    if payload.emoji.id == 726043030498574376:
        with open(f"RT/server/rea/{raw_id}/6.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:6_:726043030498574376", payload.member)

    if payload.emoji.id == 726043030221750293:
        with open(f"RT/server/rea/{raw_id}/7.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:7_:726043030221750293", payload.member)
        
    if payload.emoji.id == 726043030515220580:
        with open(f"RT/server/rea/{raw_id}/8.txt") as f:
            con = f.read()
        await message.edit(content=con)
        await message.remove_reaction("<:8_:726043030515220580", payload.member)
    try:
        f.close()
    except UnboundLocalError:
        pass

if pr == "rt!":
    bot.run("NzE2NDk2NDA3MjEyNTg5MDg3.XxBSFg.L7lTQliwyBDXg8xUas52EO8TX7A")
else:
    bot.run("NzE5NDM0MzQ4OTMxMTg2NzA5.Xu7ZrA.S08W6-BQ26YXzs40nLnSd63xK6M")#test
