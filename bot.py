from os import environ
import os
import time
from unshortenit import UnshortenIt
from urllib.request import urlopen
from urllib.parse import urlparse
import aiohttp
from pyrogram import Client, filters
from pyshorteners import Shortener
from bs4 import BeautifulSoup
#from doodstream import DoodStream
import requests
import re

API_ID = 9244035
API_HASH = '66c62a85cfbf593a991ea680223a0549'
BOT_TOKEN = '5616078400:AAEh4j9PyNc-xlhKDq-Z_krZg6o5l1pCE0o'
CHANNEL = '@cinemacollections'
MDISK_TOKEN ='JxqOU07iKDWgg2pTtHCR'
bot = Client('Doodstream bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=0)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hi, {message.chat.first_name} !!**\n\n"
        "**I am your Personal MDisk Bot 🤗, Send me a MDisk Post to see the Magic 😅**")
    
@bot.on_message(filters.text & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("processing...⏳")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'**{Doodstream_link}**' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("processing....⏳")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        if(len(Doodstream_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{Doodstream_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'**{Doodstream_link}**')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)



async def Doodstream_up(link):
    if ('bit' in link ):
        #link = urlopen(link).geturl()
        unshortener = UnshortenIt()
        link = unshortener.unshorten(link)
    
    title_new = urlparse(link)
    title_new = os.path.basename(title_new.path)
    title_Doodstream = '@' + CHANNEL + title_new
    realaurl = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
    param = {'token':f'{MDISK_TOKEN}','link':link}
    res = requests.post(realaurl, json = param)         
    data = res.json()
    data = dict(data)
    print(data)
    #bot.delete_messages(con)
    v_url = data['sharelink']
    return (v_url)


async def multi_Doodstream_up(ml_string):
    list_string = ml_string.splitlines()
    ml_string = ' \n'.join(list_string)
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = await remove_username(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_Doodstream_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    return await addFooter(new_string)


async def new_Doodstream_url(urls):
    new_urls = []
    for i in urls:
        time.sleep(0.2)
        new_urls.append(await Doodstream_up(i))
    return new_urls


async def remove_username(new_List):
    for i in new_List:
        if('@' in i or 't.me' in i or 'https://bit.ly/abcd' in i or 'https://bit.ly/123abcd' in i or 'telegra.ph' in i or 'https://youtu.be/abcd' in i or 'http://mdisk.fun/QuBXzL' in i or 'https://t.me/' in i):
            new_List.remove(i)
    return new_List

async def addFooter(str):
    footer = """

""" + CHANNEL + """ """
    return str + footer

bot.run()
