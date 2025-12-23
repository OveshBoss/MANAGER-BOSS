import os
import re
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant

# --- config ---
API_ID = int(os.environ.get("API_ID", "your_id"))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003166629808"))
OWNER_ID = int(os.environ.get("OWNER_ID", "1416433622"))

app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- database (temporary for render) ---
FSUB_DATA = {}
FILTERS = {}
RULES = {}
LOCKS = {}

# --- small caps helper ---
def sc(text):
    mapping = {"a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ғ", "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ", "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ", "s": "s", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x", "y": "ʏ", "z": "ᴢ"}
    return "".join([mapping.get(c.lower(), c) for c in text])

# --- start command ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    caption = sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ.\nɪ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀᴛs ᴡɪᴛʜ ᴀᴅᴠᴀɴᴄᴇᴅ ᴛᴏᴏʟs.")
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton(sc("ᴏᴡɴᴇʀ"), url="t.me/your_username"), InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url="t.me/your_channel")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_main")]
    ])
    await message.reply_photo(photo="https://telegra.ph/file/your_image.jpg", caption=caption, reply_markup=buttons)

# --- f-sub handler ---
@app.on_message(filters.group & ~filters.service, group=-1)
async def fsub_handler(client, message):
    chat_id = message.chat.id
    if chat_id in FSUB_DATA:
        channel_id = FSUB_DATA[chat_id]
        try:
            await client.get_chat_member(channel_id, message.from_user.id)
        except UserNotParticipant:
            await message.delete()
            return await message.reply_text(sc(f"ʜᴇʏ {message.from_user.mention}, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ sᴇɴᴅ ᴍᴇssᴀɢᴇs!"), 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ"), url=f"t.me/{(await client.get_chat(channel_id)).username}")]]))

# --- admin commands: ban, mute, kick ---
@app.on_message(filters.command(["ban", "dban", "sban", "mute", "dmute", "smute", "kick", "skick"]) & filters.group)
async def admin_cmds(client, message):
    # admin verification
    self = await client.get_chat_member(message.chat.id, message.from_user.id)
    if self.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return

    cmd = message.command[0]
    if not message.reply_to_message:
        return await message.reply_text(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ!"))

    user = message.reply_to_message.from_user
    log_msg = ""

    if "ban" in cmd:
        await client.ban_chat_member(message.chat.id, user.id)
        log_msg = f"🚫 ʙᴀɴɴᴇᴅ: {user.mention}"
    elif "mute" in cmd:
        await client.restrict_chat_member(message.chat.id, user.id, ChatPermissions(can_send_messages=False))
        log_msg = f"🔇 ᴍᴜᴛᴇᴅ: {user.mention}"
    elif "kick" in cmd:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        log_msg = f"👞 ᴋɪᴄᴋᴇᴅ: {user.mention}"

    if cmd.startswith("d"): await message.reply_to_message.delete()
    if cmd.startswith("s"): await message.delete()
    else: await message.reply_text(sc(f"✅ ᴅᴏɴᴇ! {log_msg}"))

    # log to channel
    await client.send_message(LOG_CHANNEL, sc(f"📝 ʟᴏɢ ᴇᴠᴇɴᴛ\n\nɢʀᴏᴜᴘ: {message.chat.title}\nᴀᴄᴛɪᴏɴ: {cmd}\nᴀᴅᴍɪɴ: {message.from_user.id}\nᴛᴀʀɢᴇᴛ: {user.id}"))

# --- filter system ---
@app.on_message(filters.command("filter") & filters.group)
async def set_filter(client, message):
    if len(message.command) < 3: return
    trigger = message.command[1]
    reply = message.text.split(None, 2)[2]
    FILTERS[message.chat.id] = {trigger: reply}
    await message.reply_text(sc(f"✅ ғɪʟᴛᴇʀ '{trigger}' sᴀᴠᴇᴅ!"))

@app.on_message(filters.text & filters.group, group=1)
async def filter_reply(client, message):
    if message.chat.id in FILTERS:
        for trigger, reply in FILTERS[message.chat.id].items():
            if trigger.lower() in message.text.lower():
                await message.reply_text(reply)

# --- force subscribe setting ---
@app.on_message(filters.command("set_fsub") & filters.group)
async def set_fsub_cmd(client, message):
    if len(message.command) < 2: return
    cid = int(message.command[1])
    FSUB_DATA[message.chat.id] = cid
    await message.reply_text(sc(f"✅ ғ-sᴜʙ sᴇᴛ ᴛᴏ {cid}"))

# --- help menu ---
@app.on_callback_query(filters.regex("help_main"))
async def help_cb(client, cb):
    await cb.message.edit_text(sc("🏷 ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs:\n\n/ban - ʙᴀɴ ᴜsᴇʀ\n/mute - ᴍᴜᴛᴇ ᴜsᴇʀ\n/filter - sᴇᴛ ᴀ ғɪʟᴛᴇʀ\n/set_fsub - sᴇᴛ ғ-sᴜʙ\n/rules - ᴄʜᴇᴄᴋ ʀᴜʟᴇs"), 
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="start_back")]]))

print(sc("ʙᴏᴛ ɪs ᴀʟɪᴠᴇ ᴀɴᴅ ʀᴜɴɴɪɴɢ!"))
app.run()
