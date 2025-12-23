import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import UserNotParticipant

# --- config (env variables) ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -100...))
OWNER_ID = int(os.environ.get("OWNER_ID", 12345678))

app = Client("manager_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- storage ---
FSUB_DB = {} # {chat_id: channel_id}

# --- small caps helper ---
def sc(text):
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- f-sub check logic ---
@app.on_message(filters.group & ~filters.service, group=-1)
async def fsub_check(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id not in FSUB_DB:
        return

    channel_id = FSUB_DB[chat_id]
    try:
        await client.get_chat_member(channel_id, user_id)
    except UserNotParticipant:
        # user ko mute kar do jab tak join na kare
        await client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        await message.delete()
        
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ"), url=f"t.me/{(await client.get_chat(channel_id)).username}")],
            [InlineKeyboardButton(sc("✅ ᴠᴇʀɪғʏ ᴍᴇ"), callback_data=f"verify_{user_id}_{channel_id}")]
        ])
        await message.reply_text(
            sc(f"ʜᴇʏ {message.from_user.mention}, ʏᴏᴜ ᴀʀᴇ ᴍᴜᴛᴇᴅ! ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴄʟɪᴄᴋ ᴠᴇʀɪғʏ ᴛᴏ sᴘᴇᴀᴋ."),
            reply_markup=btn
        )

# --- verification button handler ---
@app.on_callback_query(filters.regex(r"^verify_"))
async def verify_handler(client, cb):
    _, user_id, channel_id = cb.data.split("_")
    user_id = int(user_id)
    
    if cb.from_user.id != user_id:
        return await cb.answer(sc("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ!"), show_alert=True)
    
    try:
        await client.get_chat_member(int(channel_id), user_id)
        # unmute user
        await client.restrict_chat_member(cb.message.chat.id, user_id, ChatPermissions(
            can_send_messages=True, can_send_media_messages=True, 
            can_send_other_messages=True, can_add_web_page_previews=True
        ))
        await cb.message.delete()
        await cb.answer(sc("ᴠᴇʀɪғɪᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ sᴘᴇᴀᴋ."), show_alert=True)
    except UserNotParticipant:
        await cb.answer(sc("ʏᴏᴜ sᴛɪʟʟ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ!"), show_alert=True)

# --- admin commands (ban/mute/kick) ---
@app.on_message(filters.command(["ban", "dban", "sban", "mute", "dmute", "smute", "kick", "skick", "unban", "unmute"]) & filters.group)
async def admin_cmds(client, message):
    admin = await client.get_chat_member(message.chat.id, message.from_user.id)
    if admin.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return

    if not message.reply_to_message:
        return await message.reply_text(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ."))

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
    else: await message.reply_text(sc(f"✅ {target.first_name} {act}!"))

    # log entry
    await client.send_message(LOG_CHANNEL, sc(f"📑 ʟᴏɢ: {act}\nɢʀᴏᴜᴘ: {message.chat.title}\nᴀᴅᴍɪɴ: {message.from_user.id}\nᴜsᴇʀ: {target.id}"))

# --- fsub setting command ---
@app.on_message(filters.command("set_fsub") & filters.group)
async def set_fsub(client, message):
    if len(message.command) < 2:
        return await message.reply_text(sc("ᴜsᴀɢᴇ: /set_fsub -100xxxxxxx"))
    
    FSUB_DB[message.chat.id] = int(message.command[1])
    await message.reply_text(sc(f"✅ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ sᴇᴛ ᴛᴏ {message.command[1]}"))

@app.on_message(filters.command("remove_fsub") & filters.group)
async def rem_fsub(client, message):
    FSUB_DB.pop(message.chat.id, None)
    await message.reply_text(sc("❌ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ʀᴇᴍᴏᴠᴇᴅ!"))

# --- help menu ---
@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    text = sc("ʜᴇʟᴘ ᴍᴇɴᴜ:\n/ban - ʙᴀɴ ᴜsᴇʀ\n/mute - ᴍᴜᴛᴇ ᴜsᴇʀ\n/set_fsub - sᴇᴛ ғ-sᴜʙ\n/remove_fsub - ᴅɪsᴀʙʟᴇ ғ-sᴜʙ\n/rules - ᴄʜᴇᴄᴋ ʀᴜʟᴇs")
    await message.reply_text(text)

app.run()
