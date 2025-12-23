import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant

# --- CONFIG (RENDER KE ENV VARIABLES MEIN DALEIN) ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))
OWNER_ID = int(os.environ.get("OWNER_ID", 12345678))

app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- DATABASE STORAGE ---
db = {
    "fsub": {},
    "rules": {}
}

# --- SMALL CAPS HELPER ---
def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- START COMMAND WITH USER LOGGING ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user = message.from_user
    WELCOME_IMG = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
    
    # User Info Log to Log Channel
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
        [InlineKeyboardButton(sc("ᴏᴡɴᴇʀ"), url="t.me/your_username"), InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url="t.me/your_channel")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_menu")]
    ])
    await message.reply_photo(photo=WELCOME_IMG, caption=caption, reply_markup=btns)

# --- FSUB HANDLER WITH VERIFY ---
@app.on_message(filters.group & ~filters.service, group=-1)
async def fsub_handler(client, message):
    chat_id = message.chat.id
    if chat_id not in db["fsub"]: return

    channel_id = db["fsub"][chat_id]
    try:
        await client.get_chat_member(channel_id, message.from_user.id)
    except UserNotParticipant:
        await client.restrict_chat_member(chat_id, message.from_user.id, ChatPermissions(can_send_messages=False))
        await message.delete()
        
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ"), url=f"t.me/{(await client.get_chat(channel_id)).username}")],
            [InlineKeyboardButton(sc("✅ ᴠᴇʀɪғʏ ᴊᴏɪɴᴇᴅ"), callback_data=f"vfy_{message.from_user.id}_{channel_id}")]
        ])
        await message.reply_text(sc(f"ʜᴇʏ {message.from_user.mention}, ᴊᴏɪɴ ᴀɴᴅ ᴠᴇʀɪғʏ ᴛᴏ sᴘᴇᴀᴋ!"), reply_markup=btn)

@app.on_callback_query(filters.regex(r"^vfy_"))
async def verify_callback(client, cb):
    _, user_id, channel_id = cb.data.split("_")
    if cb.from_user.id != int(user_id): return await cb.answer(sc("ɴᴏᴛ ʏᴏᴜʀ ʙᴜᴛᴛᴏɴ!"))
    
    try:
        await client.get_chat_member(int(channel_id), int(user_id))
        await client.restrict_chat_member(cb.message.chat.id, int(user_id), ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
        await cb.message.delete()
        await cb.answer(sc("ᴠᴇʀɪғɪᴇᴅ!"), show_alert=True)
    except UserNotParticipant:
        await cb.answer(sc("ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ!"), show_alert=True)

# --- ADMIN ACTIONS (BAN, MUTE, KICK) ---
@app.on_message(filters.command(["ban", "dban", "sban", "mute", "dmute", "smute", "kick", "skick", "unban", "unmute"]) & filters.group)
async def admin_cmds(client, message):
    admin = await client.get_chat_member(message.chat.id, message.from_user.id)
    if admin.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]: return

    if not message.reply_to_message: return await message.reply(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ!"))
    
    target = message.reply_to_message.from_user
    cmd = message.command[0]

    if "ban" in cmd:
        await client.ban_chat_member(message.chat.id, target.id)
        act = "ʙᴀɴɴᴇᴅ"
    elif "mute" in cmd:
        await client.restrict_chat_member(message.chat.id, target.id, ChatPermissions(can_send_messages=False))
        act = "ᴍᴜᴛᴇᴅ"
    elif "kick" in cmd:
        await client.ban_chat_member(message.chat.id, target.id)
        await client.unban_chat_member(message.chat.id, target.id)
        act = "ᴋɪᴄᴋᴇᴅ"
    elif "un" in cmd:
        await client.unban_chat_member(message.chat.id, target.id)
        await client.restrict_chat_member(message.chat.id, target.id, ChatPermissions(can_send_messages=True))
        act = "ᴜɴ-ʀᴇsᴛʀɪᴄᴛᴇᴅ"

    if "d" in cmd: await message.reply_to_message.delete()
    if "s" in cmd: await message.delete()
    else: await message.reply(sc(f"✅ {target.first_name} {act}!"))

    if LOG_CHANNEL != 0:
        log_text = sc(f"📑 ᴀᴅᴍɪɴ ʟᴏɢ\n\nᴀᴄᴛɪᴏɴ: {act}\nɢʀᴏᴜᴘ: {message.chat.title}\nᴀᴅᴍɪɴ: {message.from_user.id}\nᴛᴀʀɢᴇᴛ: {target.id}")
        await client.send_message(LOG_CHANNEL, log_text)

# --- FSUB SETTINGS ---
@app.on_message(filters.command("set_fsub") & filters.group)
async def set_fsub(client, message):
    if len(message.command) < 2: return await message.reply(sc("ᴜsᴀɢᴇ: /set_fsub -100xxxx"))
    db["fsub"][message.chat.id] = int(message.command[1])
    await message.reply(sc(f"✅ ғ-sᴜʙ sᴇᴛ!"))

# --- HELP MENU CALLBACK ---
@app.on_callback_query(filters.regex("help_menu"))
async def help_cb(client, cb):
    await cb.message.edit_text(sc("🏷 ᴄᴏᴍᴍᴀɴᴅs:\n\n/ban - ʙᴀɴ ᴜsᴇʀ\n/mute - ᴍᴜᴛᴇ ᴜsᴇʀ\n/set_fsub - sᴇᴛ ғ-sᴜʙ\n/rules - ᴄʜᴇᴄᴋ ʀᴜʟᴇs"), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="start_back")]]))

print(sc("ʙᴏᴛ ɪs ᴀʟɪᴠᴇ!"))
app.run()
