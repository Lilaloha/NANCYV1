import os
import requests
import aiohttp
import yt_dlp

from pyrogram import filters, Client
from youtube_search import YoutubeSearch

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command('song') & ~filters.private & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('Finding..✨️🎶Danger_Bots⚡️Processing Sounds💫🎼...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "Song Not Found🚶."
        )
        print(str(e))
        return
    m.edit("𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚂𝚘𝚗𝚐🎶 𝙵𝚛𝚘𝚖 𝙳𝚊𝚗𝚐𝚎𝚛_𝚋𝚘𝚝 𝚂𝚎𝚛𝚟𝚎𝚛🎧🌎...")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = '**🎵𝖴𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝖡𝗒 :- ✨ @alvaro_Official⚡**'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('𝖸𝗈𝗎𝗍𝗎𝖻𝖾 𝖤𝗋𝗋𝗈𝗋 ❌ 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 @danger_bots 🔥')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
