import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -100123456789))
OWNER_ID = int(os.environ.get("OWNER_ID", 12345678))

app = Client("powerful_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- IN-MEMORY DATABASE ---
db = {
    "fsub": {},
    "filters": {},
    "rules": {},
    "locks": {},
    "welcome": {},
    "welcome_status": {}
}

# --- SMALL CAPS HELPER ---
def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- LOGGING HELPER ---
async def send_log(client, chat_title, action, admin, target):
    log_text = f"✨ **{sc('ɴᴇᴡ ʟᴏɢ ᴇɴᴛʀʏ')}** ✨\n\n" \
               f"🌐 **{sc('ɢʀᴏᴜᴘ')}:** `{chat_title}`\n" \
               f"⚡ **{sc('ᴀᴄᴛɪᴏɴ')}:** `{action}`\n" \
               f"👮 **{sc('ᴀᴅᴍɪɴ')}:** {admin}\n" \
               f"👤 **{sc('ᴛᴀʀɢᴇᴛ')}:** {target}\n" \
               f"📅 **{sc('ᴅᴀᴛᴇ')}:** 𝟸𝟶𝟸𝟻"
    await client.send_message(LOG_CHANNEL, log_text)

# --- START & HELP ---
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    img = "https://telegra.ph/file/your_image.jpg" # apni image url yahan dalein
    text = sc("ʜᴇʟʟᴏ! ɪ ᴀᴍ ᴛʜᴇ ᴍᴏsᴛ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ.\nɪ ᴡɪʟʟ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ᴀɴᴅ sᴇᴄᴜʀᴇ ʏᴏᴜʀ ᴄʜᴀᴛs ᴇғғɪᴄɪᴇɴᴛʟʏ.")
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton(sc("ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ"), url=f"t.me/{(await client.get_me()).username}?startgroup=true")],
        [InlineKeyboardButton(sc("ᴏᴡɴᴇʀ"), url="t.me/your_username"), InlineKeyboardButton(sc("ᴄʜᴀɴɴᴇʟ"), url="t.me/your_channel")],
        [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="open_help")]
    ])
    await message.reply_photo(img, caption=text, reply_markup=btns)

# --- BAN/MUTE/KICK LOGIC ---
@app.on_message(filters.command(["ban", "dban", "sban", "mute", "dmute", "smute", "kick", "skick", "unban", "unmute"]) & filters.group)
async def admin_actions(client, message):
    user_status = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user_status.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return

    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text(sc("ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ."))

    target_user = message.reply_to_message.from_user if message.reply_to_message else await client.get_users(message.command[1])
    cmd = message.command[0]

    try:
        if "ban" in cmd:
            await client.ban_chat_member(message.chat.id, target_user.id)
            act = "ʙᴀɴɴᴇᴅ"
        elif "mute" in cmd:
            await client.restrict_chat_member(message.chat.id, target_user.id, ChatPermissions(can_send_messages=False))
            act = "ᴍᴜᴛᴇᴅ"
        elif "kick" in cmd:
            await client.ban_chat_member(message.chat.id, target_user.id)
            await client.unban_chat_member(message.chat.id, target_user.id)
            act = "ᴋɪᴄᴋᴇᴅ"
        elif "unban" in cmd:
            await client.unban_chat_member(message.chat.id, target_user.id)
            act = "ᴜɴʙᴀɴɴᴇᴅ"
        elif "unmute" in cmd:
            await client.restrict_chat_member(message.chat.id, target_user.id, ChatPermissions(can_send_messages=True))
            act = "ᴜɴᴍᴜᴛᴇᴅ"

        if "d" in cmd: await message.reply_to_message.delete()
        if "s" in cmd: await message.delete()
        else: await message.reply_text(sc(f"✅ {target_user.first_name} has been {act}"))

        await send_log(client, message.chat.title, act, message.from_user.mention, target_user.mention)
    except Exception as e:
        await message.reply_text(f"ᴇʀʀᴏʀ: {e}")

# --- RULES SYSTEM ---
@app.on_message(filters.command("setrules") & filters.group)
async def set_rules(client, message):
    if len(message.command) < 2: return
    db["rules"][message.chat.id] = message.text.split(None, 1)[1]
    await message.reply_text(sc("✅ ᴄʜᴀᴛ ʀᴜʟᴇs ʜᴀᴠᴇ ʙᴇᴇɴ sᴇᴛ!"))

@app.on_message(filters.command("rules") & filters.group)
async def get_rules(client, message):
    rules = db["rules"].get(message.chat.id, sc("ɴᴏ ʀᴜʟᴇs sᴇᴛ ғᴏʀ ᴛʜɪs ᴄʜᴀᴛ."))
    await message.reply_text(rules)

# --- FSUB HANDLER ---
@app.on_message(filters.command("set_fsub") & filters.group)
async def set_fsub(client, message):
    if len(message.command) < 2: return
    db["fsub"][message.chat.id] = int(message.command[1])
    await message.reply_text(sc(f"✅ ғ-sᴜʙ sᴇᴛ ᴛᴏ {message.command[1]}"))

@app.on_message(filters.group & ~filters.service, group=-1)
async def check_fsub(client, message):
    chat_id = message.chat.id
    if chat_id in db["fsub"]:
        try:
            await client.get_chat_member(db["fsub"][chat_id], message.from_user.id)
        except UserNotParticipant:
            await message.delete()
            return await message.reply_text(sc(f"ʜᴇʏ {message.from_user.mention}, ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄʜᴀᴛ!"),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ᴊᴏɪɴ ɴᴏᴡ"), url=f"t.me/{(await client.get_chat(db['fsub'][chat_id])).username}")]]))

# --- HELP CALLBACK ---
@app.on_callback_query(filters.regex("open_help"))
async def help_menu(client, cb):
    text = sc("ʜᴇʟᴘ ᴍᴇɴᴜ - ᴄᴏᴍᴍᴀɴᴅs ʟɪsᴛ\n\n"
              "🔹 /ban, /mute, /kick - ᴀᴅᴍɪɴ ᴛᴏᴏʟs\n"
              "🔹 /set_fsub [ɪᴅ] - sᴇᴛ ғᴏʀᴄᴇ sᴜʙ\n"
              "🔹 /setrules [ᴛᴇxᴛ] - sᴇᴛ ɢʀᴏᴜᴘ ʀᴜʟᴇs\n"
              "🔹 /filter [ᴡᴏʀᴅ] [ʀᴇᴘʟʏ] - sᴇᴛ ᴀᴜᴛᴏ-ʀᴇᴘʟʏ\n"
              "🔹 /locks - sᴇᴇ ᴄʜᴀᴛ ʟᴏᴄᴋs")
    await cb.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="open_help")]]))

print(sc("ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!"))
app.run()
