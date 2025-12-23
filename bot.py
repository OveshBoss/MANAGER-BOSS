import os
import asyncio
import random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "ʙᴏᴛ ɪs ᴀʟɪᴠᴇ!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
OWNER_ID = int(os.environ.get("OWNER_ID", 12345678))

app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- DATABASE ---
db = {"fsub": {}, "rules": {}}

# --- SMALL CAPS HELPER ---
def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- START COMMAND WITH RANDOM REACTION ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    # 7 Positive Emojis ka List
    emojis = ["🔥", "❤️", "✨", "⚡", "🌟", "🥂", "🧿"]
    
    # 1. Random Emoji React karna
    try:
        await message.react(emoji=random.choice(emojis))
    except:
        pass

    user = message.from_user
    WELCOME_IMG = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
    
    # Log to Channel (Small Caps - As per your preference)
    if LOG_CHANNEL != 0:
        log_text = (
            f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ')}**\n\n"
            f"🆔 **{sc('ᴜsᴇʀ ɪᴅ')}:** `{user.id}`\n"
            f"👤 **{sc('ɴᴀᴍᴇ')}:** {user.first_name}\n"
            f"🔗 **{sc('ᴜsᴇʀɴᴀᴍᴇ')}:** @{user.username if user.username else 'ɴᴏɴᴇ'}\n"
            f"📅 **{sc('ᴅᴀᴛᴇ')}:** 𝟸𝟶𝟸𝟻"
        )
        await client.send_message(LOG_CHANNEL, log_text)

    caption = (
        f"**{sc('ʜᴇʟʟᴏ!')}** 👋\n\n"
        f"ɪ ᴀᴍ **{sc('ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ')}**.\n"
        f"ɪ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀᴛs ᴡɪᴛʜ ғᴏʀᴄᴇ sᴜʙ, ᴀᴅᴍɪɴ ᴛᴏᴏʟs, ᴀɴᴅ ʟᴏɢs.\n\n"
        f"**{sc('ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ.')}**"
    )
    
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ ➕"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton(sc("ᴏᴡɴᴇʀ"), url="t.me/Ovesh_Boss"), InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url="t.me/OveshBossOfficial")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_menu")]
    ])
    
    await message.reply_photo(photo=WELCOME_IMG, caption=caption, reply_markup=btns)

# (Baaki F-Sub aur Admin commands pehle wale hi rahenge)

# --- STARTUP ---
if __name__ == "__main__":
    Thread(target=run_web).start()
    print(sc("ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴏɴ ʀᴇɴᴅᴇʀ!"))
    app.run()
