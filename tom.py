import os
import glob
import json
import logging
import asyncio
import youtube_dl
from pytube import YouTube
from youtube_search import YoutubeSearch
from pytgcalls import PyTgCalls, idle
from pytgcalls import StreamType
from pytgcalls.types import Update
from pytgcalls.types import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded, StreamVideoEnded
from pytgcalls.types import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo
)
from pyrogram import Client, filters
from pyrogram.raw.base import Update
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from BabyPlugs.queues import QUEUE, add_to_queue, get_queue, clear_queue, pop_an_item
from BabyPlugs.admin_check import *

bot = Client(
    "Tom",
    bot_token = os.environ["BOT_TOKEN" ,"5583584098:AAH8GrxqqdwnkCKALmTYONkEJQU98j_OYiQ"],
    api_id = int(os.environ["API_ID" ,"9683694"]),
    api_hash = os.environ["API_HASH" ,"c426d9f7087744afdafc961a620b6338"]
)

client = Client(os.environ["SESSION_NAME" ,"AQAHLwS-fotPEWLJhYh55Hjm3oZpT7HPF1oKgOzDuP8hL3jCsgpx6pAtwP_LkB3X4JX0QAuDEOAKDOYmq-yio4KPnTX8l0sZYeXpKK9u6T6AqDZ1zldz2rtBWpB8AjlbzcRAShk5GXrRkHx0lAuXsYZK3I_vRXm0KhKTbGzswLWrNTf-_MJi2hYpfRPWcV07AIwbdsa4KHarQrSoc7r2pqrb5wZ3yUpoVlfTedrouLdmJeHixl6kAGTBFApSSR3rMMDd343RkQG4a8oQphNAtOMRukz9uDQ8e0UhnrMSbshPTDzEpUrU271Abq_n9CCfXEUmIm40Qq3EeJdiGXNDRnCwAAAAATGMW3kA"], int(os.environ["API_ID"]), os.environ["API_HASH"])

app = PyTgCalls(client)

OWNER_ID = int(os.environ["OWNER_ID","5286943475"])

BOT_USERNAME = os.environ["BOT_USERNAME","ALONEX_MUSIC_BOT"]

LIVE_CHATS = []

START_TEXT = """
**━━━━━━━━━━━━━━━━━━
💙 𝙷𝙾𝙸 <b>{}</b>,
      𝙸'𝙼 𝙰𝙳𝚅𝙰𝙽𝙲𝙴 𝚅𝙲 𝙱𝙾𝚃 𝙵𝙾𝚁 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 . : /
┏━━━━━━━━━━━━━━━━┓
┣★ 𝙱𝙰𝙱𝚄 
┣★ 𝚂𝙷𝙾𝙽𝙰
┗━━━━━━━━━━━━━━━━┛

😋 𝙰𝙶𝙴𝚁 𝙰𝙿𝙺𝙾 𝙿𝚁𝙾𝙱𝙻𝙴𝙼 𝙷𝙰𝙸 𝚃𝙾 𝙰𝙺𝙴𝙻𝙴 𝙼𝙴 𝙱𝙰𝚃 𝙺𝙰𝚁𝚃𝙴 𝙷𝙰𝙸 𝙱𝙰𝙱𝚈[𝚂𝙷𝙾𝙽𝙰](tg://user?id={}) 𝙱𝙰𝙱𝚈...
━━━━━━━━━━━━━━━━━━**
"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("♡ 𝙱𝙰𝙱𝚄 𝙼𝙴𝚁𝙴 𝙳𝙸𝙻 𝙼𝙴 𝙰𝙾𝙾 ♡", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("♡𝙷𝙴𝙻𝙿 𝙼𝙴 𝙱𝙰𝙱𝚄♡", callback_data="cbcmds"),
            InlineKeyboardButton("♡𝚂𝙷𝙾𝙽𝙰♡", url="https://t.me/Nobita_Doremon_bot")
        ],
        [
            InlineKeyboardButton("♡𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙱𝙰𝙱𝚈♡", url="https://t.me/TheJerrySupport"),
            InlineKeyboardButton("♡𝚄𝙿𝙳𝙰𝚃𝙴 𝙹𝙰𝙰𝙽♡", url="https://t.me/THEJERRY_NETWORK")
        ],
        [
            InlineKeyboardButton("♡𝚂𝚆𝙴𝙴𝚃𝙷𝙴𝙰𝚁𝚃♡", url="https://t.me/song_hye_kyoo")
        ]
    ]
)

BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="♡𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙱𝙰𝙱𝚈♡", url="https://t.me/TheJerrySupport"),
            InlineKeyboardButton(text="♡𝚂𝙷𝙾𝙽𝙰♡", url="https://t.me/Nobita_Doremon_bot")
        ]
    ]
)

async def skip_current_song(chat_id):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await app.leave_group_call(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            title = chat_queue[1][0]
            duration = chat_queue[1][1]
            link = chat_queue[1][2]
            playlink = chat_queue[1][3]
            type = chat_queue[1][4]
            Q = chat_queue[1][5]
            thumb = chat_queue[1][6]
            if type == "Audio":
                await app.change_stream(
                    chat_id,
                    AudioPiped(
                        playlink,
                    ),
                )
            elif type == "Video":
                if Q == "high":
                    hm = HighQualityVideo()
                elif Q == "mid":
                    hm = MediumQualityVideo()
                elif Q == "low":
                    hm = LowQualityVideo()
                else:
                    hm = LowQualityVideo()
                await app.change_stream(
                    chat_id, AudioVideoPiped(playlink, HighQualityAudio(), hm)
                )
            pop_an_item(chat_id)
            await bot.send_photo(chat_id, photo = thumb,
                                 caption = f"» <b>ɴᴀᴍᴇ:</b> [{title}]({link}) | `{type}` \n\n🕕 <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}",
                                 reply_markup = BUTTONS)
            return [title, link, type, duration, thumb]
    else:
        return 0


async def skip_item(chat_id, lol):
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        try:
            x = int(lol)
            title = chat_queue[x][0]
            chat_queue.pop(x)
            return title
        except Exception as e:
            print(e)
            return 0
    else:
        return 0


@app.on_stream_end()
async def on_end_handler(_, update: Update):
    if isinstance(update, StreamAudioEnded):
        chat_id = update.chat_id
        await skip_current_song(chat_id)


@app.on_closed_voice_chat()
async def close_handler(client: PyTgCalls, chat_id: int):
    if chat_id in QUEUE:
        clear_queue(chat_id)


async def yt_video(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()
    

async def yt_audio(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@bot.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("Commands Menu")
    await query.edit_message_text(
        f"""**» 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝙹𝙰𝙰𝙽𝚄 «**
» /play (Song Name/Link) - 𝙿𝚕𝚊𝚢 𝚖𝚞𝚜𝚒𝚌
» /vplay (video name/link) - 𝙿𝚕𝚊𝚢 𝚅𝚒𝚍𝚎𝚘
» /pause - 𝙿𝚊𝚞𝚜𝚎 𝚃𝚑𝚎 𝚂𝚘𝚗𝚐
» /resume - Resume The Song
» /skip - switch to next Song
» /end - Stop The Streaming
» /join or /userbotjoin - Invite Assistant To Your Group
» /mute - Mute The Assistant On Voice Chat
» /unmute - UnMute The Assistant On Voice Chat
» /playlist - Show You The Playlist
» /restart - Restart The Bot

🤤 By 𝙱𝙰𝙱𝚄 🤤""")


@bot.on_message(filters.command("start") & filters.private)
async def start_private(_, message):
    msg = START_TEXT.format(message.from_user.mention, OWNER_ID, OWNER_ID)
    await message.reply_photo(photo="https://te.legra.ph/file/b0284421d07c5b51b3db1.jpg",
                             caption = msg,
                             reply_markup = START_BUTTONS)
    

@bot.on_message(filters.command(["join", "userbotjoin", "join@{BOT_USERNAME}"]) & filters.group)
async def join_chat(c: Client, m: Message):
    chat_id = m.chat.id
    try:
        invitelink = await c.export_chat_invite_link(chat_id)
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
            await client.join_chat(invitelink)
            return await client.send_message(chat_id, "🙂ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ.")
    except UserAlreadyParticipant:
        return await client.send_message(chat_id, "🙂ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ ʙᴀʙʏ")


@bot.on_message(filters.command("start") & filters.group)
async def start_group(_, message):
    await message.reply_photo(photo="https://telegra.ph/file/22ae93512721d5186932e.jpg",
                              caption = f"ʜᴇʏ 😘 {message.from_user.mention},\n ᴍᴇ ɪᴢ ᴅᴇᴅ ʙᴀʙʏ​ 😴",
                              reply_markup = BUTTONS)


@bot.on_message(filters.command(["play", "vplay"]) & filters.group)
async def video_play(_, message):
    await message.delete()
    user_id = message.from_user.id
    state = message.command[0].lower()
    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply_text(f"<b>Usage:</b> <code>/{state} [query]</code>")
    chat_id = message.chat.id
    m = await message.reply_text("🤤")
    if state == "play":
        damn = AudioPiped
        ded = yt_audio
        doom = "Audio"
    elif state == "vplay":
        damn = AudioVideoPiped
        ded = yt_video
        doom = "Video"
    if "low" in query:
        Q = "low"
    elif "mid" in query:
        Q = "mid"
    elif "high" in query:
        Q = "high"
    else:
        Q = "0"
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumb = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        yt = YouTube(link)
        cap = f"» <b>ɴᴀᴍᴇ:</b> [{yt.title}]({link}) | `{doom}` \n\n🕕 <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}"
        try:
            ydl_opts = {"format": "bestvideo[height<=720]+bestaudio/best[height<=720]"}
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            info_dict = ydl.extract_info(link, download=False)
            p = json.dumps(info_dict)
            a = json.loads(p)
            playlink = a['formats'][1]['manifest_url']
        except:
            ice, playlink = await ded(link)
            if ice == "0":
                return await m.edit("» ɴᴏᴛ ғᴏᴜɴᴅ, ᴛʀʏ sᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ ᴛʜᴇ sᴏɴɢ ɴᴀᴍᴇ ʙᴀʙʏ !")               
    except Exception as e:
        return await m.edit(str(e))
    
    try:
        if chat_id in QUEUE:
            position = add_to_queue(chat_id, yt.title, duration, link, playlink, doom, Q, thumb)
            caps = f"» ɴᴀᴍᴇ [{yt.title}]({link}) <b>ǫᴜᴇᴜᴇᴅ ᴀᴛ {position} ʙᴀʙʏ</b> \n\n🕕 <b>ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration}"
            await message.reply_photo(thumb, caption=caps, reply_markup=BUTTONS)
            await m.delete()
        else:            
            await app.join_group_call(
                chat_id,
                damn(playlink),
                stream_type=StreamType().pulse_stream
            )
            add_to_queue(chat_id, yt.title, duration, link, playlink, doom, Q, thumb)
            await message.reply_photo(thumb, caption=cap, reply_markup=BUTTONS)
            await m.delete()
    except Exception as e:
        return await m.edit(str(e))


@bot.on_message(filters.command("skip") & filters.group)
@is_admin
async def skip(_, message):
    await message.delete()
    chat_id = message.chat.id
    if len(message.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ᴡʜᴀᴛ ᴛᴏ sᴋɪᴘ ʙᴀʙʏ 🥲")
        elif op == 1:
            await message.reply_text("» ᴛʀᴀᴄᴋ sᴋɪᴘᴘᴇᴅ ʙʏ {} ʙᴀʙʏ🤔".format( message.from_user.mention ), )
    else:
        skip = message.text.split(None, 1)[1]
        out = "🗑 <b>Removed the following song(s) from the queue:</b> \n"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        out = out + "\n" + f"<b>#️⃣ {x}</b> - {hm}"
            await message.reply_text(out)


@bot.on_message(filters.command(["playlist"]) & filters.group)
@is_admin
async def playlist(_, message):
    chat_id = message.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await message.delete()
            await message.reply_text(
                f"» <b>ɴᴀᴍᴇ:</b> [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][4]}`",
                disable_web_page_preview=True,
            )
        else:
            out = f"<b>📃 Player queue:</b> \n\n» <b>ɴᴀᴍᴇ:</b> [{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][4]}` \n"
            l = len(chat_queue)
            for x in range(1, l):
                title = chat_queue[x][0]
                link = chat_queue[x][2]
                type = chat_queue[x][4]
                out = out + "\n" + f"<b>#️⃣ {x}</b> - [{title}]({link}) | `{type}` \n"
            await message.reply_text(out, disable_web_page_preview=True)
    else:
        await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
    

@bot.on_message(filters.command(["end", "stop"]) & filters.group)
@is_admin
async def end(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        await app.leave_group_call(chat_id)
        clear_queue(chat_id)
        await message.reply_text("» sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ ʙʏ {} ʙᴀʙʏ🥺".format( message.from_user.mention ), )
    else:
        await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
        

@bot.on_message(filters.command("pause") & filters.group)
@is_admin
async def pause(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.pause_stream(chat_id)
            await message.reply_text("» ᴛʀᴀᴄᴋ ᴘᴀᴜsᴇᴅ ʙʏ {} ʙᴀʙʏ😫".format( message.from_user.mention ), )
        except:
            await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
    else:
        await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
        
        
@bot.on_message(filters.command("resume") & filters.group)
@is_admin
async def resume(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.resume_stream(chat_id)
            await message.reply_text("» ᴛʀᴀᴄᴋ ʀᴇsᴜᴍᴇᴅ ʙʏ {} ʙᴀʙʏ🤗".format( message.from_user.mention ), )
        except:
            await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
    else:
        await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
        
        
@bot.on_message(filters.command("mute") & filters.group)
@is_admin
async def mute(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.mute_stream(chat_id)
            await message.reply_text("🔇 Stream Muted by {} Baby.".format( message.from_user.mention ), )
        except:
            await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
    else:
        await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
        
        
@bot.on_message(filters.command("unmute") & filters.group)
@is_admin
async def unmute(_, message):
    await message.delete()
    chat_id = message.chat.id
    if chat_id in QUEUE:
        try:
            await app.unmute_stream(chat_id)
            await message.reply_text("🔊 Stream unmuted by {} Baby.".format( message.from_user.mention ), )
        except:
            await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
    else:
        await message.reply_text("» ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ʙᴀʙʏ 🥱")
        
        
@bot.on_message(filters.command(["restart", "fuck"]))
async def restart(_, message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        return
    await message.reply_text("🛠 <i>Restarting Music Player...</i>")
    os.system(f"kill -9 {os.getpid()} && python3 tom.py")
            

app.start()
bot.run()
idle()
