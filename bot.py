import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant

# --- CONFIG (ENVIRONMENT VARIABLES) ---
# Render ke "Environment Variables" section mein ye sab zaroor bharein
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
# Default value -100 ko 0 kar diya taaki syntax error na aaye
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0)) 
OWNER_ID = int(os.environ.get("OWNER_ID", 12345678))

app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- DATABASE STORAGE ---
db = {
    "fsub": {},
    "filters": {},
    "rules": {},
    "welcome": {},
    "locks": {}
}

# --- SMALL CAPS HELPER ---
def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- START COMMAND ---
@app.on_message(filters.command("start"))
async def start(client, message):
    text = sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ.\nɪ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀᴛs ᴡɪᴛʜ ғ-sᴜʙ, ʟᴏᴄᴋs, ᴀɴᴅ ᴀᴅᴍɪɴ ᴛᴏᴏʟs.")
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton(sc("ᴏᴡɴᴇʀ"), url="t.me/your_username"), InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url="t.me/your_channel")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ ᴍᴇɴᴜ"), callback_data="help_menu")]
    ])
    await message.reply_text(text, reply_markup=btns)

# --- FSUB CHECK & VERIFICATION ---
@app.on_message(filters.group & ~filters.service, group=-1)
async def fsub_check(client, message):
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
        await message.reply_text(sc(f"ʜᴇʏ {message.from_user.mention}, ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴍᴇssᴀɢᴇ!"), reply_markup=btn)

@app.on_callback_query(filters.regex(r"^vfy_"))
async def verify_cb(client, cb):
    _, user_id, channel_id = cb.data.split("_")
    if cb.from_user.id != int(user_id): return await cb.answer(sc("ɴᴏᴛ ʏᴏᴜʀ ʙᴜᴛᴛᴏɴ!"))
    
    try:
        await client.get_chat_member(int(channel_id), int(user_id))
        await client.restrict_chat_member(cb.message.chat.id, int(user_id), ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True))
        await cb.message.delete()
        await cb.answer(sc("ᴠᴇʀɪғɪᴇᴅ! ʏᴏᴜ ᴄᴀɴ ᴄʜᴀᴛ ɴᴏᴡ."), show_alert=True)
    except UserNotParticipant:
        await cb.answer(sc("ᴊᴏɪɴ ғɪʀsᴛ!"), show_alert=True)

# --- FSUB SETTINGS ---
@app.on_message(filters.command("set_fsub") & filters.group)
async def set_fsub(client, message):
    if len(message.command) < 2: return await message.reply(sc("ᴜsᴀɢᴇ: /set_fsub -100xxxx"))
    db["fsub"][message.chat.id] = int(message.command[1])
    await message.reply(sc(f"✅ ғ-sᴜʙ sᴇᴛ ᴛᴏ {message.command[1]}"))

# --- ADMIN ACTIONS (BAN, MUTE, KICK) ---
@app.on_message(filters.command(["ban", "mute", "kick", "unban", "unmute"]) & filters.group)
async def admin_cmds(client, message):
    # Admin Check
    m = await client.get_chat_member(message.chat.id, message.from_user.id)
    if m.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]: return

    if not message.reply_to_message: return await message.reply(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ!"))
    
    target = message.reply_to_message.from_user
    cmd = message.command[0]

    if cmd == "ban":
        await client.ban_chat_member(message.chat.id, target.id)
        act = "ʙᴀɴɴᴇᴅ"
    elif cmd == "mute":
        await client.restrict_chat_member(message.chat.id, target.id, ChatPermissions(can_send_messages=False))
        act = "ᴍᴜᴛᴇᴅ"
    elif cmd == "kick":
        await client.ban_chat_member(message.chat.id, target.id)
        await client.unban_chat_member(message.chat.id, target.id)
        act = "ᴋɪᴄᴋᴇᴅ"
    elif "un" in cmd:
        await client.unban_chat_member(message.chat.id, target.id)
        await client.restrict_chat_member(message.chat.id, target.id, ChatPermissions(can_send_messages=True))
        act = "ᴜɴᴍᴜᴛᴇᴅ/ᴜɴʙᴀɴɴᴇᴅ"

    await message.reply(sc(f"✅ {target.first_name} {act}!"))
    if LOG_CHANNEL != 0:
        await client.send_message(LOG_CHANNEL, sc(f"📑 ʟᴏɢ: {act}\nɢʀᴏᴜᴘ: {message.chat.title}\nᴀᴅᴍɪɴ: {message.from_user.id}\nᴜsᴇʀ: {target.id}"))

# --- HELP MENU ---
@app.on_callback_query(filters.regex("help_menu"))
async def help_cb(client, cb):
    help_text = sc("🏷 ᴄᴏᴍᴍᴀɴᴅs ʟɪsᴛ:\n\n/ban - ʙᴀɴ ᴜsᴇʀ\n/mute - ᴍᴜᴛᴇ ᴜsᴇʀ\n/set_fsub - sᴇᴛ ғ-sᴜʙ\n/rules - ᴄʜᴇᴄᴋ ʀᴜʟᴇs\n/setrules - sᴇᴛ ʀᴜʟᴇs")
    await cb.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="start_back")]]))

print(sc("ʙᴏᴛ sᴛᴀʀᴛᴇᴅ..."))
app.run()
