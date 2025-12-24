import os, asyncio, random, re
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from flask import Flask
from threading import Thread

# --- ʀᴇɴᴅᴇʀ ᴘᴏʀᴛ ғɪx ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "ʙᴏᴛ ɪs ᴀʟɪᴠᴇ!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- ᴄᴏɴғɪɢ ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_token")
LOG_CHANNEL = -1003166629808 
OWNER_ID = 12345678 # ᴀᴘɴɪ ɪᴅ ᴅᴀᴀʟᴇɪɴ

app = Client("manager_boss", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- ᴅᴀᴛᴀʙᴀsᴇ (ɪɴ-ᴍᴇᴍᴏʀʏ ᴇxᴀᴍᴘʟᴇ) ---
db = {
    "fsub": {}, "filters": {}, "greetings": {}, 
    "blocklist": {}, "warns": {}, "conns": {}
}

# --- sᴍᴀʟʟ ᴄᴀᴘs ʜᴇʟᴘᴇʀ ---
def sc(text):
    if not text: return ""
    m = {"a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ","0":"𝟶","1":"𝟷","2":"𝟸","3":"𝟹","4":"𝟺","5":"𝟻","6":"𝟼","7":"𝟽","8":"𝟾","9":"𝟿"}
    return "".join([m.get(c.lower(), c) for c in str(text)])

# --- ᴘᴍ ʜᴀɴᴅʟᴇʀ & ʟᴏɢs ---
@app.on_message(filters.private & filters.incoming)
async def pm_handler(c, m):
    try: await m.react(emoji=random.choice(["🔥", "❤️", "✨", "⚡", "🌟", "🧿"]))
    except: pass
    
    if m.text == "/start":
        user = m.from_user
        log_text = f"**{sc('👤 ɴᴇᴡ ᴜsᴇʀ sᴛᴀʀᴛᴇᴅ')}**\n\n🆔: `{user.id}`\n👤: {user.first_name}\n📅: 𝟸𝟶𝟸𝟻"
        await c.send_message(LOG_CHANNEL, log_text)
        
        img = "https://graph.org/file/3bf4b466c0c5cfc956fe8-f1f7d952b4b3c10747.jpg"
        cap = f"**{sc('ʜᴇʟʟᴏ!')}** 👋\n\n{sc('ɪ ᴀᴍ ᴘᴏᴡᴇʀғᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇʀ ʙᴏᴛ.')}\n{sc('ɪ ᴄᴀɴ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ᴄʜᴀᴛs ᴡɪᴛʜ ғᴏʀᴄᴇ sᴜʙ, ᴀᴅᴍɪɴ ᴛᴏᴏʟs, ᴀɴᴅ ʟᴏɢs.')}\n\n{sc('ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴍʏ ᴘᴏᴡᴇʀs.')}"
        btns = InlineKeyboardMarkup([
            [InlineKeyboardButton(sc("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ ➕"), url=f"t.me/{c.me.username}?startgroup=true")],
            [InlineKeyboardButton(sc("ʜᴇʟᴘ & ᴄᴍᴅs"), callback_data="help_list")]
        ])
        await m.reply_photo(photo=img, caption=cap, reply_markup=btns)

# --- ɪɴᴠɪᴛᴇ ᴛʜᴀɴᴋs ---
@app.on_message(filters.new_chat_members)
async def invite_msg(c, m):
    if m.new_chat_members[0].id == c.me.id:
        img = "https://graph.org/file/f340b55f492b0ad0276a9-24b7dabf4b19a8d723.jpg"
        cap = f"✨ **{sc('ᴛʜᴀɴᴋs ғᴏʀ ɪɴᴠɪᴛɪɴɢ ᴍᴇ!')}**\n\n{sc('ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴ.')}"
        await m.reply_photo(photo=img, caption=cap, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("📑 ᴍʏ ᴄᴏᴍᴍᴀɴᴅs"), url=f"t.me/{c.me.username}?start=help")]]))

# --- ʜᴇʟᴘ ᴍᴇɴᴜ (ᴀʟʟ 𝟻 ᴍᴏᴅᴜʟᴇs) ---
@app.on_callback_query(filters.regex("^help_"))
async def help_cb(c, cb):
    if cb.data == "help_list":
        btns = [
            [InlineKeyboardButton(sc("ɪɴʟɪɴᴇ/ғɪʟᴛᴇʀs"), callback_data="help_filt"), InlineKeyboardButton(sc("ɢʀᴇᴇᴛɪɴɢs"), callback_data="help_greet")],
            [InlineKeyboardButton(sc("ʙʟᴏᴄᴋʟɪsᴛs"), callback_data="help_block"), InlineKeyboardButton(sc("ᴡᴀʀɴɪɴɢs"), callback_data="help_warn")],
            [InlineKeyboardButton(sc("ᴄᴏɴɴᴇᴄᴛɪᴏɴ"), callback_data="help_conn")]
        ]
        await cb.message.edit_caption(caption=sc("📑 ʜᴇʟᴘ ᴄᴀᴛᴇɢᴏʀɪᴇs"), reply_markup=InlineKeyboardMarkup(btns))
    
    elif cb.data == "help_filt":
        txt = f"**{sc('ɪɴʟɪɴᴇ ғɪʟᴛᴇʀs')}**\n\n/filter <trigger> <reply>\n/filters\n/stop <trigger>\n/stopall"
        await cb.message.edit_caption(caption=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_list")]]))
    
    elif cb.data == "help_greet":
        txt = f"**{sc('ɢʀᴇᴇᴛɪɴɢs')}**\n\n/welcome <on/off>\n/goodbye <on/off>\n/setwelcome <text>\n/setgoodbye <text>\n/cleanwelcome <on/off>"
        await cb.message.edit_caption(caption=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_list")]]))

    elif cb.data == "help_block":
        txt = f"**{sc('ʙʟᴏᴄᴋʟɪsᴛs')}**\n\n/addblocklist <trigger>\n/rmblocklist <trigger>\n/blocklistmode <action>\n/blocklistdelete <on/off>"
        await cb.message.edit_caption(caption=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_list")]]))

    elif cb.data == "help_warn":
        txt = f"**{sc('ᴡᴀʀɴɪɴɢs')}**\n\n/warn <reason>\n/dwarn (warn & delete)\n/resetwarn\n/warnlimit <num>\n/warntime <time>"
        await cb.message.edit_caption(caption=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_list")]]))

    elif cb.data == "help_conn":
        txt = f"**{sc('ᴄᴏɴɴᴇᴄᴛɪᴏɴs')}**\n\n/connect <id>\n/disconnect\n/reconnect\n/connection"
        await cb.message.edit_caption(caption=txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(sc("ʙᴀᴄᴋ"), callback_data="help_list")]]))

# --- ғɪʟᴛᴇʀ ʟᴏɢɪᴄ ---
@app.on_message(filters.group & ~filters.service)
async def group_handler(c, m):
    chat_id = m.chat.id
    # 𝟷. ʙʟᴏᴄᴋʟɪsᴛ ᴄʜᴇᴄᴋ
    if chat_id in db["blocklist"]:
        for trigger in db["blocklist"][chat_id]:
            if trigger in m.text.lower():
                await m.delete()
                return await m.reply(sc("❌ ᴛʜɪs ᴍᴇssᴀɢᴇ ɪs ʙʟᴏᴄᴋʟɪsᴛᴇᴅ!"))

    # 𝟸. ғɪʟᴛᴇʀ ᴄʜᴇᴄᴋ
    if chat_id in db["filters"] and m.text:
        for trigger, reply in db["filters"][chat_id].items():
            if trigger.lower() == m.text.lower():
                return await m.reply(reply)

# --- ᴄᴏᴍᴍᴀɴᴅs (ᴀᴅᴍɪɴ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘs) ---
@app.on_message(filters.command("filter") & filters.group)
async def add_filter(c, m):
    if len(m.command) < 3: return await m.reply(sc("ᴜsᴀɢᴇ: /filter trigger reply"))
    chat_id = m.chat.id
    if chat_id not in db["filters"]: db["filters"][chat_id] = {}
    db["filters"][chat_id][m.command[1]] = " ".join(m.command[2:])
    await m.reply(sc("✅ ғɪʟᴛᴇʀ sᴀᴠᴇᴅ!"))

@app.on_message(filters.command("warn") & filters.group)
async def warn_logic(c, m):
    if not m.reply_to_message: return await m.reply(sc("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ!"))
    user_id = m.reply_to_message.from_user.id
    db["warns"][user_id] = db["warns"].get(user_id, 0) + 1
    await m.reply(sc(f"⚠️ ᴜsᴇʀ ᴡᴀʀɴᴇᴅ! ({db['warns'][user_id]}/𝟹)"))

# --- ᴘʀɪᴠᴀᴛᴇ ᴄᴏᴍᴍᴀɴᴅ ᴇxᴘʟᴀɪɴᴇʀ ---
@app.on_message(filters.private & filters.command(["filter", "warn", "blocklist", "setwelcome"]))
async def pm_explain(c, m):
    await m.reply(sc("ʜᴇʏ! ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs. ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴀ ᴄʜᴀᴛ ᴛᴏ ᴜsᴇ ɪᴛ."))

if __name__ == "__main__":
    Thread(target=run_web).start()
    app.run()
