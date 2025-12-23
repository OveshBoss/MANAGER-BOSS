import os, asyncio, random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "ʙᴏᴛ ɪs ᴀʟɪᴠᴇ!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = -1003166629808 
OWNER_USERNAME = "Ovesh_Boss" # Apna username yahan dalein
CHANNEL_USERNAME = "OveshBossOfficial" # Apne channel ka username yahan dalein

app = Client("rose_pro_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- STORAGE ---
db = {"fsub": {}, "notes": {}, "warns": {}, "locks": {}}

# --- SMALL CAPS HELPER ---
def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- PM HANDLER (START, REACTIONS, LOGS) ---
@app.on_message(filters.private & filters.incoming)
async def pm_handler(client, message):
    # 1. Random Reaction on every message
    try: await message.react(emoji=random.choice(["🔥", "❤️", "✨", "⚡", "🌟", "🥂", "🧿"]))
    except: pass

    if message.text and message.text.startswith("/start"):
        # Log to Channel
        user = message.from_user
        try:
            log_text = f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ')}**\n\n🆔: `{user.id}`\n👤: {user.first_name}\n🔗: @{user.username if user.username else 'None'}"
            await client.send_message(LOG_CHANNEL, log_text)
        except: pass

        # Welcome Image & Buttons
        img = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
        caption = (
            f"**{sc('ʜᴇʟʟᴏ!')}** 👋\n\n"
            f"ɪ ᴀᴍ **{sc('ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ')}**.\n"
            f"ɪ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀᴛs ᴡɪᴛʜ ғᴏʀᴄᴇ sᴜʙ, ᴀᴅᴍɪɴ ᴛᴏᴏʟs, ᴀɴᴅ ʟᴏɢs.\n\n"
            f"**{sc('ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴍʏ ᴘᴏᴡᴇʀs.')}**"
        )
        
        btns = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
            [InlineKeyboardButton(sc("ᴏᴡɴᴇʀ"), url=f"t.me/{Ovesh_Boss}"), InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url=f"t.me/{OveshBossOfficial}")],
            [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_main")]
        ])
        await message.reply_photo(photo=img, caption=caption, reply_markup=btns)

# --- NEW CHAT MEMBER (INVITE THANKS) ---
@app.on_message(filters.new_chat_members)
async def invite_handler(client, message):
    me = await client.get_me()
    for member in message.new_chat_members:
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

# --- HELP CALLBACK HANDLER ---
@app.on_callback_query(filters.regex("^help_"))
async def help_callback(client, cb):
    if cb.data == "help_main":
        text = sc("📑 ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ᴍᴇɴᴜ\n\nᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴛᴇɢᴏʀʏ:")
        btns = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("🛡️ ᴀᴅᴍɪɴ"), callback_data="help_adm"), InlineKeyboardButton(sc("📝 ɴᴏᴛᴇs"), callback_data="help_note")],
            [InlineKeyboardButton(sc("📢 ғ-sᴜʙ"), callback_data="help_fs"), InlineKeyboardButton(sc("🔒 ʟᴏᴄᴋs"), callback_data="help_lock")],
            [InlineKeyboardButton(sc("🔙 ʙᴀᴄᴋ"), callback_data="help_home")]
        ])
        await cb.message.edit_caption(caption=text, reply_markup=btns)
    elif cb.data == "help_adm":
        await cb.message.edit_caption(caption=sc("🛡️ ᴀᴅᴍɪɴ ᴄᴍᴅs:\n/ban - ʙᴀɴ ᴜsᴇʀ\n/mute - ᴍᴜᴛᴇ ᴜsᴇʀ\n/kick - ᴋɪᴄᴋ ᴜsᴇʀ\n/unban - ᴜɴʙᴀɴ\n/warn - ᴡᴀʀɴ ᴜsᴇʀ"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("🔙 ʙᴀᴄᴋ"), callback_data="help_main")]]))

# --- GROUP COMMANDS REDIRECT ---
@app.on_message(filters.command(["ban", "mute", "kick", "warn", "set_fsub"]) & filters.private)
async def redirect_to_group(client, message):
    await message.reply_text("ʜᴇʏ! ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs. ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ᴛᴏ ᴜsᴇ ɪᴛ.")

# --- ACTUAL GROUP ADMIN COMMANDS ---
@app.on_message(filters.group & filters.command(["ban", "mute", "unban", "unmute"]))
async def admin_logic(client, message):
    # Check if sender is admin
    sender = await client.get_chat_member(message.chat.id, message.from_user.id)
    if sender.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply_text(sc("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴛʜɪs!"))
    
    if not message.reply_to_message:
        return await message.reply_text(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ!"))
    
    target = message.reply_to_message.from_user
    cmd = message.command[0]
    
    try:
        if cmd == "ban":
            await client.ban_chat_member(message.chat.id, target.id)
            await message.reply_text(sc(f"✅ {target.first_name} ʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!"))
        elif cmd == "mute":
            await client.restrict_chat_member(message.chat.id, target.id, ChatPermissions(can_send_messages=False))
            await message.reply_text(sc(f"✅ {target.first_name} ᴍᴜᴛᴇᴅ!"))
        # Logs
        log_txt = sc(f"📑 ᴀᴅᴍɪɴ ᴀᴄᴛɪᴏɴ: {cmd}\nɢʀᴏᴜᴘ: {message.chat.title}\nᴛᴀʀɢᴇᴛ: {target.id}")
        await client.send_message(LOG_CHANNEL, log_txt)
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e}")

if __name__ == "__main__":
    Thread(target=run_web).start()
    app.run()
