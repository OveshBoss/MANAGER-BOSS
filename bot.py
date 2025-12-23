import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX (WEB SERVER) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Alive!"

def run_web():
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
OWNER_ID = int(os.environ.get("OWNER_ID", 12345678))

app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- STORAGE & HELPERS ---
db = {"fsub": {}, "rules": {}}

def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- COMMANDS ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user = message.from_user
    if LOG_CHANNEL != 0:
        log_text = f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ')}**\n\n🆔 **{sc('ᴜsᴇʀ ɪᴅ')}:** `{user.id}`\n👤 **{sc('ɴᴀᴍᴇ')}:** {user.first_name}\n🔗 **{sc('ᴜsᴇʀɴᴀᴍᴇ')}:** @{user.username if user.username else 'ɴᴏɴᴇ'}"
        await client.send_message(LOG_CHANNEL, log_text)

    WELCOME_IMG = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
    btns = InlineKeyboardMarkup([[InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ ➕"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")]])
    await message.reply_photo(photo=WELCOME_IMG, caption=sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ᴀʟɪᴠᴇ ᴏɴ ʀᴇɴᴅᴇʀ ғʀᴇᴇ ᴛɪᴇʀ."), reply_markup=btns)

# (Baaki saare F-Sub aur Admin commands jo maine pehle diye the, wo yahan niche paste kar sakte hain)

# --- BOT STARTUP ---
if __name__ == "__main__":
    # Start the web server in a separate thread
    Thread(target=run_web).start()
    print(sc("ʙᴏᴛ ɪs sᴛᴀʀᴛɪɴɢ..."))
    app.run()
