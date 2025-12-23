import os, asyncio, random
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread

# --- render port fix ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "ʙᴏᴛ ɪs ʟɪᴠᴇ!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- config ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = -1003166629808 

app = Client("pro_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- storage ---
db = {"fsub": {}, "antispam": True, "antilink": True, "antiforward": True}

# --- helpers ---
def sc(text):
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- reactions & logging on start ---
@app.on_message(filters.private & ~filters.service)
async def pm_handler(client, message):
    try: await message.react(emoji=random.choice(["🔥", "❤️", "✨", "⚡", "🌟", "🥂", "🧿"]))
    except: pass
    
    if message.text == "/start":
        user = message.from_user
        try:
            log_text = f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ')}**\n\n🆔: `{user.id}`\n👤: {user.first_name}\n🔗: @{user.username}"
            await client.send_message(LOG_CHANNEL, log_text)
        except: pass
        
        img = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
        btns = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ ➕"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
            [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_main")]
        ])
        await message.reply_photo(photo=img, caption=sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ʏᴏᴜʀ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ."), reply_markup=btns)

# --- help menu handlers (working now) ---
@app.on_callback_query(filters.regex("^help_"))
async def help_handlers(client, cb):
    if cb.data == "help_main":
        text = sc("📑 ʙᴏᴛ ʜᴇʟᴘ ᴍᴇɴᴜ\n\nᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ:")
        btns = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("🛡️ ᴀᴅᴍɪɴ"), callback_data="help_admin"), InlineKeyboardButton(sc("📢 ғ-sᴜʙ"), callback_data="help_fsub")],
            [InlineKeyboardButton(sc("⚙️ sᴇᴛᴛɪɴɢs"), callback_data="help_set")]
        ])
        await cb.message.edit_caption(caption=text, reply_markup=btns)
    elif cb.data == "help_admin":
        await cb.message.edit_caption(caption=sc("🛡️ ᴀᴅᴍɪɴ ᴄᴍᴅs:\n/ban, /mute, /kick, /unban\n\nᴀʟsᴏ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇs ʟɪɴᴋs & ғᴏʀᴡᴀʀᴅs."), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_main")]]))
    elif cb.data == "help_fsub":
        await cb.message.edit_caption(caption=sc("📢 ғ-sᴜʙ setup:\n/set_fsub [channel id]\n\nᴜsᴇʀs ᴍᴜsᴛ ᴊᴏɪɴ ᴛᴏ sᴘᴇᴀᴋ."), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_main")]]))

# --- group security (anti-link, anti-forward, fsub) ---
@app.on_message(filters.group & ~filters.service, group=-1)
async def group_protector(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # 1. fsub check
    if chat_id in db["fsub"]:
        try:
            await client.get_chat_member(db["fsub"][chat_id], user_id)
        except UserNotParticipant:
            await message.delete()
            btn = InlineKeyboardMarkup([[InlineKeyboardButton(sc("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ"), url=f"t.me/{(await client.get_chat(db['fsub'][chat_id])).username}")]])
            return await message.reply(sc(f"ʜᴇʏ {message.from_user.mention}, ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄʜᴀᴛ!"), reply_markup=btn)
        except: pass

    # 2. anti-link
    if db["antilink"] and ("t.me/" in message.text or "http" in message.text):
        if (await client.get_chat_member(chat_id, user_id)).status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
            await message.delete()
            return await message.reply(sc("❌ ʟɪɴᴋs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ!"))

    # 3. anti-forward
    if db["antiforward"] and message.forward_from_chat:
        await message.delete()
        return await message.reply(sc("❌ ғᴏʀᴡᴀʀᴅᴇᴅ ᴍsɢs ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ!"))

# --- custom welcome ---
@app.on_message(filters.new_chat_members)
async def welcome_new(client, message):
    for member in message.new_chat_members:
        await message.reply_photo(
            photo="https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg",
            caption=sc(f"ᴡᴇʟᴄᴏᴍᴇ {member.mention} ᴛᴏ {message.chat.title}!")
        )

# --- settings ---
@app.on_message(filters.command("set_fsub") & filters.group)
async def set_fsub_cmd(client, message):
    if len(message.command) < 2: return await message.reply(sc("ᴜsᴀɢᴇ: /set_fsub -100xxx"))
    db["fsub"][message.chat.id] = int(message.command[1])
    await message.reply(sc("✅ ғ-sᴜʙ ᴇɴᴀʙʟᴇᴅ!"))

# --- run ---
if __name__ == "__main__":
    Thread(target=run_web).start()
    app.run()
