import os, asyncio, random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread

# --- RENDER PORT FIX ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "ʙᴏᴛ ɪs ʟɪᴠᴇ!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- CONFIG ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = -1003166629808 

app = Client("rose_pro_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- STORAGE (IN-MEMORY DATABASE) ---
db = {
    "fsub": {}, 
    "notes": {}, 
    "warns": {}, 
    "locks": {}, 
    "welcome_status": True
}

# --- HELPERS ---
def sc(text):
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

async def is_admin(chat_id, user_id):
    try:
        m = await app.get_chat_member(chat_id, user_id)
        return m.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except: return False

# --- START & LOGGING ---
@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    try: await message.react(emoji=random.choice(["🔥", "❤️", "✨", "⚡", "🌟"]))
    except: pass
    
    user = message.from_user
    log_text = f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ ʟᴏɢ')}**\n\n🆔: `{user.id}`\n👤: {user.first_name}\n🔗: @{user.username}"
    await client.send_message(LOG_CHANNEL, log_text)
    
    img = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴄʜᴀᴛ ➕"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_main")]
    ])
    await message.reply_photo(photo=img, caption=sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ʏᴏᴜʀ ʀᴏsᴇ-sᴛʏʟᴇ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ."), reply_markup=btns)

# --- HELP MENU (WORKING) ---
@app.on_callback_query(filters.regex("^help_"))
async def help_cb(client, cb):
    if cb.data == "help_main":
        text = sc("📑 ʀᴏsᴇ ᴍᴀɴᴀɢᴇʀ ʜᴇʟᴘ\n\nᴄʟɪᴄᴋ ᴏɴ ʙᴜᴛᴛᴏɴs ᴛᴏ sᴇᴇ ᴄᴍᴅs:")
        btns = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("🛡️ ᴀᴅᴍɪɴ"), callback_data="help_adm"), InlineKeyboardButton(sc("📝 ɴᴏᴛᴇs"), callback_data="help_note")],
            [InlineKeyboardButton(sc("📢 ғ-sᴜʙ"), callback_data="help_fs"), InlineKeyboardButton(sc("🔒 ʟᴏᴄᴋs"), callback_data="help_lock")]
        ])
        await cb.message.edit_caption(caption=text, reply_markup=btns)
    elif cb.data == "help_adm":
        await cb.message.edit_caption(caption=sc("🛡️ ᴀᴅᴍɪɴ ᴄᴍᴅs:\n/ban - ʙᴀɴ ᴜsᴇʀ\n/mute - ᴍᴜᴛᴇ ᴜsᴇʀ\n/warn - ɢɪᴠᴇ ᴡᴀʀɴɪɴɢ\n/resetwarns - ᴄʟᴇᴀʀ ᴡᴀʀɴs"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_main")]]))
    elif cb.data == "help_note":
        await cb.message.edit_caption(caption=sc("📝 ɴᴏᴛᴇs ᴄᴍᴅs:\n/save [name] - sᴀᴠᴇ ɴᴏᴛᴇ (ʀᴇᴘʟʏ)\n#name - ɢᴇᴛ ɴᴏᴛᴇ\n/clear [name] - ᴅᴇʟᴇᴛᴇ ɴᴏᴛᴇ"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_main")]]))
    elif cb.data == "help_lock":
        await cb.message.edit_caption(caption=sc("🔒 ʟᴏᴄᴋs:\n/lock [type] - ʟᴏᴄᴋ sᴏᴍᴇᴛʜɪɴɢ\nᴛʏᴘᴇs: links, stickers, forwards, media"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_main")]]))

# --- GROUP HANDLER (SECURITY & FSUB) ---
@app.on_message(filters.group & ~filters.service, group=-1)
async def pro_security(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if await is_admin(chat_id, user_id): return

    # 1. FSUB CHECK
    if chat_id in db["fsub"]:
        try: await client.get_chat_member(db["fsub"][chat_id], user_id)
        except UserNotParticipant:
            await message.delete()
            return await message.reply(sc("ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄʜᴀᴛ!"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ᴊᴏɪɴ ɴᴏᴡ"), url=f"t.me/{(await client.get_chat(db['fsub'][chat_id])).username}")]]))
        except: pass

    # 2. LOCKS (ANTI-LINK/FORWARD)
    if "links" in db["locks"].get(chat_id, []) and ("t.me" in message.text or "http" in message.text):
        await message.delete()
        return
    if "forwards" in db["locks"].get(chat_id, []) and message.forward_from_chat:
        await message.delete()
        return

    # 3. NOTES (#name)
    if message.text and message.text.startswith("#"):
        note_name = message.text[1:]
        if note_name in db["notes"].get(chat_id, {}):
            await message.reply(db["notes"][chat_id][note_name])

# --- ADMIN CMDS ---
@app.on_message(filters.command("save") & filters.group)
async def save_note(client, message):
    if not await is_admin(message.chat.id, message.from_user.id): return
    if len(message.command) < 2 or not message.reply_to_message: return await message.reply(sc("ᴜsᴀɢᴇ: ʀᴇᴘʟʏ ᴛᴏ ᴍsɢ ᴡɪᴛʜ /save [name]"))
    name = message.command[1]
    if message.chat.id not in db["notes"]: db["notes"][message.chat.id] = {}
    db["notes"][message.chat.id][name] = message.reply_to_message.text
    await message.reply(sc(f"✅ ɴᴏᴛᴇ '{name}' sᴀᴠᴇᴅ!"))

@app.on_message(filters.command("warn") & filters.group)
async def warn_user(client, message):
    if not await is_admin(message.chat.id, message.from_user.id): return
    if not message.reply_to_message: return await message.reply(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ!"))
    user_id = message.reply_to_message.from_user.id
    db["warns"][user_id] = db["warns"].get(user_id, 0) + 1
    if db["warns"][user_id] >= 3:
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply(sc("🚨 𝟹 ᴡᴀʀɴɪɴɢs ᴅᴏɴᴇ! ᴜsᴇʀ ʙᴀɴɴᴇᴅ."))
        db["warns"][user_id] = 0
    else:
        await message.reply(sc(f"⚠️ ᴡᴀʀɴᴇᴅ! ({db['warns'][user_id]}/𝟹)"))

@app.on_message(filters.command("lock") & filters.group)
async def lock_cmd(client, message):
    if not await is_admin(message.chat.id, message.from_user.id): return
    if len(message.command) < 2: return await message.reply(sc("ᴜsᴇ /lock links ᴏʀ /lock forwards"))
    l_type = message.command[1]
    if message.chat.id not in db["locks"]: db["locks"][message.chat.id] = []
    db["locks"][message.chat.id].append(l_type)
    await message.reply(sc(f"🔒 {l_type} ʟᴏᴄᴋᴇᴅ!"))

# --- WELCOME ---
@app.on_message(filters.new_chat_members)
async def welcome_rose(client, message):
    if not db["welcome_status"]: return
    for member in message.new_chat_members:
        await message.reply_photo(
            photo="https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg",
            caption=sc(f"✨ ᴡᴇʟᴄᴏᴍᴇ {member.first_name}!\nᴇɴᴊᴏʏ ʏᴏᴜʀ sᴛᴀʏ ɪɴ {message.chat.title}!")
        )

if __name__ == "__main__":
    Thread(target=run_web).start()
    app.run()
