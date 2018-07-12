# APIラッパと非同期I/Oモジュールの読み込み
import discord
from urllib.request import urlopen
import urllib
import json
import pandas as pd

# クライアント接続オブジェクト
client = discord.Client()
# 各種定数
token = "NDY2NDE0MzE5OTk5OTA5ODg4.Dibt3w.gI6weviGHhkPQrDyI3EExltOU7M"
api_key = "FXingzNkqfzyojk5a4u0RGI0ElthzY"
api_url = "https://www.worldcoinindex.com/apiservice/v2getmarkets?key=%s&fiat=jpy" % api_key

# 起動時の処理
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# コメント投稿時の処理
@client.event
async def on_message(message):
    df = _get_data()
    labels = [label.split("/")[0] for label in df.Label]
    if message.content in labels:
        tmp = await client.send_message(message.channel, 'Now loading...')
        price = df[df["Label"] == "%s/JPY" % message.content]["Price"].values[0]
        price = round(price,3)
        await client.edit_message(tmp, str(price)+"円")

# 価格情報の取得
def _get_data():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    request = urllib.request.Request(url=api_url, headers=headers)
    raw_data  = urlopen(request).read().decode("utf-8")
    json_data = json.loads(raw_data)["Markets"][0]
    df = pd.DataFrame(json_data)
    return df


client.run(token)
