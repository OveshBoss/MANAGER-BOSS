import os, asyncio, random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread

# --- ʀᴇɴᴅᴇʀ ᴘᴏʀᴛ ғɪx ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "ʙᴏᴛ ɪs ʟɪᴠᴇ!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- ᴄᴏɴғɪɢ ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = -1003166629808 

app = Client("rose_pro_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- sᴛᴏʀᴀɢᴇ ---
db = {"fsub": {}, "notes": {}, "warns": {}, "locks": {}}

# --- ʜᴇʟᴘᴇʀs ---
def sc(text):
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- ɴᴇᴡ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ ʜᴀɴᴅʟᴇʀ (ɪɴᴠɪᴛᴇ ᴛʜᴀɴᴋs) ---
@app.on_message(filters.new_chat_members)
async def welcome_handler(client, message):
    me = await client.get_me()
    for member in message.new_chat_members:
        # 1. ᴀɢᴀʀ ʙᴏᴛ ᴋᴏ ᴀᴅᴅ ᴋɪʏᴀ ɢᴀʏᴀ
        if member.id == me.id:
            invite_img = "https://graph.org/file/f340b55f492b0ad0276a9-24b7dabf4b19a8d723.jpg"
            caption = (
                f"✨ **{sc('ᴛʜᴀɴᴋs ғᴏʀ ɪɴᴠɪᴛɪɴɢ ᴍᴇ!')}**\n\n"
                f"ɪ ᴀᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ **{message.chat.title}** sᴍᴏᴏᴛʜʟʏ.\n"
                f"ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ **{sc('ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ')}** sᴏ ɪ ᴄᴀɴ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ!\n\n"
                f"⚡ **{sc('ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʀᴏsᴇ ᴍᴀɴᴀɢᴇʀ')}**"
            )
            btns = InlineKeyboardMarkup([[
                InlineKeyboardButton(sc("📑 ᴍʏ ᴄᴏᴍᴍᴀɴᴅs"), url=f"https://t.me/{me.username}?start=help")
            ]])
            await message.reply_photo(photo=invite_img, caption=caption, reply_markup=btns)
        
        # 2. ᴀɢᴀʀ ᴋᴏɪ ɴᴀʏᴀ ᴜsᴇʀ ᴀᴀʏᴇ (ɢʀᴇᴇᴛɪɴɢs)
        else:
            await message.reply_text(sc(f"ʜᴇʏ {member.mention}, ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {message.chat.title}!"))

# --- sᴛᴀʀᴛ ᴄᴏᴍᴍᴀɴᴅ ---
@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    try: await message.react(emoji=random.choice(["🔥", "❤️", "✨", "⚡", "🌟"]))
    except: pass
    
    # ʟᴏɢɢɪɴɢ ᴜsᴇʀ ɪɴғᴏ
    try:
        log_text = f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ ʟᴏɢ')}**\n\n🆔: `{message.from_user.id}`\n👤: {message.from_user.first_name}"
        await client.send_message(LOG_CHANNEL, log_text)
    except: pass

    # ɪғ sᴛᴀʀᴛᴇᴅ ғʀᴏᴍ "ᴍʏ ᴄᴏᴍᴍᴀɴᴅs" ʙᴜᴛᴛᴏɴ
    if "help" in message.text:
        return await help_main_msg(client, message)

    img = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴄʜᴀᴛ ➕"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_main")]
    ])
    await message.reply_photo(photo=img, caption=sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ʏᴏᴜʀ ʀᴏsᴇ-sᴛʏʟᴇ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ."), reply_markup=btns)

# --- ʜᴇʟᴘ ᴍᴇɴᴜ ғᴜɴᴄᴛɪᴏɴ ---
async def help_main_msg(client, message):
    help_text = sc("📑 ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ᴍᴇɴᴜ\n\nʜᴇʀᴇ ᴀʀᴇ ᴍʏ ᴘᴏᴡᴇʀs:")
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("🛡️ ᴀᴅᴍɪɴ"), callback_data="help_adm"), InlineKeyboardButton(sc("📝 ɴᴏᴛᴇs"), callback_data="help_note")],
        [InlineKeyboardButton(sc("📢 ғ-sᴜʙ"), callback_data="help_fs"), InlineKeyboardButton(sc("🔒 ʟᴏᴄᴋs"), callback_data="help_lock")]
    ])
    if message.photo: # ɪғ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ɪᴍᴀɢᴇ
        await message.reply_text(help_text, reply_markup=btns)
    else:
        await message.reply_text(help_text, reply_markup=btns)

# --- ᴄᴀʟʟʙᴀᴄᴋ ʜᴀɴᴅʟᴇʀs (ғᴏʀ ʙᴜᴛᴛᴏɴs) ---
@app.on_callback_query(filters.regex("^help_"))
async def help_cb(client, cb):
    if cb.data == "help_main":
        await cb.edit_message_text(sc("📑 ʜᴇʟᴘ ᴍᴇɴᴜ"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("🛡️ ᴀᴅᴍɪɴ"), callback_data="help_adm"), InlineKeyboardButton(sc("📝 ɴᴏᴛᴇs"), callback_data="help_note")],
            [InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_back")]
        ]))
    elif cb.data == "help_adm":
        await cb.edit_message_text(sc("🛡️ ᴀᴅᴍɪɴ:\n/ban, /mute, /warn, /kick"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_main")]]))
    # ᴀᴅᴅ ᴍᴏʀᴇ ᴄʙ ᴀs ɴᴇᴇᴅᴇᴅ

if __name__ == "__main__":
    Thread(target=run_web).start()
    app.run()
