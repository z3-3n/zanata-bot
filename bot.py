import os, json, uuid, random, re, tempfile
import telebot
from telebot import types
import yt_dlp

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("TOKEN not found!")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

RANDOM_REPLIES = ["هلا والله 🖤","ارحب يا قَضّ 🕊️","منور والله","يا هلا يا هلا","نورت","هلا بعيون اسود 🖤"]
ASWAD_REPLIES = ["هلا بعيون اسود 🖤","امر يا حلو؟ 💋","نعم يا قلب اسود؟ 🖤","ها؟ تناديني؟ 😏","عيون اسود لك","احبك 🖤","احبك؟ قلبي اسود ما يعرف يحب 🖤","ها يا قَضّ؟","قول يا حلو 😈","تأمر يا بعد اسود","نعم نعم؟ 💋","اسود يسمعك 🖤"]

DATA_FILE = "groups_data.json"
WHISPER_FILE = "whispers.json"
USERS_FILE = "users_data.json"

def load_json(file, default):
    try:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as ff:
                return json.load(ff)
    except: pass
    return default

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as ff:
        json.dump(data, ff, ensure_ascii=False, indent=2)

data = load_json(DATA_FILE, {})
whispers = load_json(WHISPER_FILE, {})
users_data = load_json(USERS_FILE, {})
pending = {}
pending_reaction = {}

BOT_ID = None
BOT_USERNAME = "z3_3n2BOT"
try:
    me = bot.get_me()
    BOT_ID = me.id
    BOT_USERNAME = me.username
except Exception as e:
    print(f"get_me failed: {e}")

def get_chat_data(chat_id):
    chat_id = str(chat_id)
    if chat_id not in data:
        data[chat_id] = {"asasy": ["6453478028"], "owners": [], "creators": [], "managers": [], "admins": [], "special": [], "banned": [], "muted": [], "locks": {}, "replies_enabled": True, "reactions": {}, "bot_name": "اسود"}
    if "reactions" not in data[chat_id]: data[chat_id]["reactions"] = {}
    return data[chat_id]

def save_data(): save_json(DATA_FILE, data)
def save_whispers(): save_json(WHISPER_FILE, whispers)
def save_users(): save_json(USERS_FILE, users_data)
def is_sudo(uid): return uid == 6453478028

def has_role(chat_id, user_id, min_role="special"):
    c = get_chat_data(chat_id)
    hierarchy = ["special", "admins", "managers", "creators", "owners", "asasy"]
    roles = []
    sid = str(user_id)
    if sid in c["special"]: roles.append("special")
    if sid in c["admins"]: roles.append("admins")
    if sid in c["managers"]: roles.append("managers")
    if sid in c["creators"]: roles.append("creators")
    if sid in c["owners"]: roles.append("owners")
    if sid in c["asasy"] or is_sudo(user_id): roles.append("asasy")
    if not roles: return False
    return max([hierarchy.index(r) for r in roles]) >= hierarchy.index(min_role)

def add_user(user):
    uid = str(user.id)
    if uid not in users_data:
        users_data[uid] = {"id": user.id, "name": user.first_name, "username": user.username or ""}
        save_users()

def handle_music_search(message, query, search_type="يوت"):
    if not query:
        bot.reply_to(message, "• اكتب: يوت + اسم الاغنية")
        return
    try:
        bot.send_message(message.chat.id, f"• {search_type} {query}\n• جاري التحميل... ⏳")
    except: pass
    try:
        ydl_opts_search = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
            search_query = f"ytsearch1:{query}"
            info = ydl.extract_info(search_query, download=False)
            if not info or 'entries' not in info or len(info['entries']) == 0:
                bot.send_message(message.chat.id, "❌ ما لقيت شي"); return
            video = info['entries'][0]
            video_url = video.get('url') or video.get('webpage_url') or f"https://www.youtube.com/watch?v={video.get('id')}"
            title = video.get('title', query)
            duration = video.get('duration', 0)
        temp_dir = tempfile.gettempdir()
        ydl_opts_download = {'format': 'bestaudio/best','outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),'quiet': True,'no_warnings': True,'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]}
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            info_dl = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dl)
            mp3_file = os.path.splitext(filename)[0] + ".mp3"
            if not os.path.exists(mp3_file): mp3_file = filename
        if os.path.exists(mp3_file):
            with open(mp3_file, 'rb') as audio:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Music Aswad 🖤", url=f"https://t.me/{BOT_USERNAME}"))
                bot.send_audio(message.chat.id, audio, caption=title, title=title, performer="Music Aswad", duration=duration, reply_markup=markup)
            try: os.remove(mp3_file)
            except: pass
        else:
            bot.send_message(message.chat.id, f"🎵 {title}\n{video_url}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ: {str(e)[:200]}")
        print(f"YT error: {e}")

@bot.message_handler(func=lambda m: m.text and (m.text.strip().startswith("يوت ") or m.text.strip().startswith("بحث ")))
def music_in_group(message):
    text = message.text.strip()
    if text.startswith("يوت "): q = text.replace("يوت ","",1).strip(); typ = "يوت"
    else: q = text.replace("بحث ","",1).strip(); typ = "بحث"
    if not q: return
    handle_music_search(message, q, typ)

@bot.message_handler(func=lambda m: m.chat.type == 'private', content_types=['text'])
def private_panel(message):
    uid = message.from_user.id
    add_user(message.from_user)
    if not is_sudo(uid):
        if uid in pending:
            wid = pending.get(uid)
            w = whispers.get(wid)
            if not w: return
            w['text'] = message.text
            whispers[wid] = w
            save_whispers()
            try: bot.delete_message(message.chat.id, message.message_id)
            except: pass
            bot.send_message(message.chat.id, f"تم ارسال همستك لـ {w['to_name']} 🕊️")
            try:
                mk = types.InlineKeyboardMarkup()
                mk.add(types.InlineKeyboardButton("رؤية الهمسة", callback_data=f"view_{wid}"))
                mk.add(types.InlineKeyboardButton(f"اهمس لـ {w['to_name']}", callback_data=f"re_{w['to_id']}_{w['group_id']}"))
                bot.send_message(w['group_id'], f"• الهمسه لـ -> {w['to_name']} 🕊️\n• من -> {w['from_name']}", reply_markup=mk)
            except: pass
            del pending[uid]
        else:
            txt = message.text.strip()
            if txt.startswith("يوت ") or txt.startswith("بحث "):
                q = txt.split(" ", 1)[1] if " " in txt else ""
                handle_music_search(message, q, txt.split(" ")[0])
        return
    text = message.text.strip()
    if text.startswith("اذاعة خاص") or text.startswith("اذاعه خاص"):
        msg = text.replace("اذاعة خاص","").replace("اذاعه خاص","").strip()
        if not msg: bot.send_message(message.chat.id, "• اكتب: اذاعة خاص + النص"); return
        count = 0
        for uid_str in list(users_data.keys()):
            try: bot.send_message(int(uid_str), f"📢 من اسود 🖤:\n\n{msg}"); count += 1
            except: pass
        bot.send_message(message.chat.id, f"✅ تمت اذاعة خاص لـ {count} عضو"); return
    if text.startswith("اذاعة عام") or text.startswith("اذاعه عام") or text.startswith("اذاعة") or text.startswith("اذاعه"):
        msg = text.replace("اذاعة عام","").replace("اذاعه عام","").replace("اذاعة","").replace("اذاعه","").strip()
        if not msg: bot.send_message(message.chat.id, "• اذاعة خاص + نص\n• اذاعة عام + نص"); return
        count_users = 0; count_groups = 0
        for uid_str in list(users_data.keys()):
            try: bot.send_message(int(uid_str), f"📢 اذاعة من اسود 🖤:\n\n{msg}"); count_users += 1
            except: pass
        for cid in list(data.keys()):
            try: bot.send_message(cid, f"📢 اذاعة من اسود 🖤:\n\n{msg}"); count_groups += 1
            except: pass
        bot.send_message(message.chat.id, f"✅ اذاعة عام:\n• {count_users} خاص\n• {count_groups} قروب"); return
    if text in ["القروبات","/groups"]:
        txt = f"📊 قروبات {BOT_USERNAME}:\n"
        for cid in data.keys():
            try: title = bot.get_chat(cid).title
            except: title = "غير معروف"
            txt += f"• {title} ({cid})\n"
        txt += f"\n👥 خاص: {len(users_data)} عضو"
        bot.send_message(message.chat.id, txt[:4000]); return
    if text in ["الاوامر","/help","/start"]:
        bot.send_message(message.chat.id, f"هلا اسود 🖤 @{BOT_USERNAME}"); return

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("ضع تفاعل"))
def set_react1(message):
    if message.chat.type == 'private': return
    if not has_role(message.chat.id, message.from_user.id, "managers"): bot.reply_to(message, "❌ للمدراء فقط"); return
    full = message.text.replace("ضع تفاعل","",1).strip()
    if not full: bot.reply_to(message, "• ضع تفاعل + الاسم\nمثال: ضع تفاعل محمد 🌹"); return
    parts = full.split()
    if len(parts) >= 2 and len(parts[-1]) <= 10:
        emoji = parts[-1]
        name = " ".join(parts[:-1])
        c = get_chat_data(str(message.chat.id))
        if name not in c["reactions"]: c["reactions"][name] = []
        if isinstance(c["reactions"][name], str): c["reactions"][name] = [c["reactions"][name]]
        if emoji in c["reactions"][name]: bot.reply_to(message, f"• {emoji} موجود من قبل"); return
        if len(c["reactions"][name]) >= 5: bot.reply_to(message, f"❌ الحد 5 لـ {name}: {' '.join(c['reactions'][name])}"); return
        c["reactions"][name].append(emoji); save_data()
        bot.reply_to(message, f"✅ {name} {emoji}\n• المجموع: {' '.join(c['reactions'][name])} ({len(c['reactions'][name])}/5)")
    else:
        name = full
        pending_reaction[message.chat.id] = {"name": name, "user": message.from_user.id}
        bot.reply_to(message, f"• ارسل ايموجي لـ {name} 🌹\n• تقدر ترسل اكثر: 🌹 ❤️ 🔥")

@bot.message_handler(func=lambda m: m.chat.type!= 'private' and m.chat.id in pending_reaction, content_types=['text'])
def set_react2(message):
    if message.chat.id not in pending_reaction: return
    pr = pending_reaction[message.chat.id]
    if pr["user"]!= message.from_user.id: return
    emoji_text = message.text.strip()
    emojis = emoji_text.split() if " " in emoji_text else [emoji_text]
    emojis = [e for e in emojis if len(e) <= 10][:5]
    name = pr["name"]
    c = get_chat_data(str(message.chat.id))
    if name not in c["reactions"]: c["reactions"][name] = []
    if isinstance(c["reactions"][name], str): c["reactions"][name] = [c["reactions"][name]]
    added = []
    for em in emojis:
        if em not in c["reactions"][name] and len(c["reactions"][name]) < 5:
            c["reactions"][name].append(em); added.append(em)
    save_data(); del pending_reaction[message.chat.id]
    if added: bot.reply_to(message, f"✅ {name} {' '.join(added)}\n• المجموع: {' '.join(c['reactions'][name])} ({len(c['reactions'][name])}/5)")
    else: bot.reply_to(message, f"• الحد او موجود\n• الحالي: {' '.join(c['reactions'][name])}")

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("مسح تفاعل"))
def del_react(message):
    if message.chat.type == 'private': return
    if not has_role(message.chat.id, message.from_user.id, "managers"): return
    full = message.text.replace("مسح تفاعل","",1).strip()
    if not full: bot.reply_to(message, "• مسح تفاعل + الاسم"); return
    parts = full.split()
    c = get_chat_data(str(message.chat.id))
    if len(parts) >= 2:
        emoji = parts[-1]; name = " ".join(parts[:-1])
        if name in c["reactions"]:
            if isinstance(c["reactions"][name], str): c["reactions"][name] = [c["reactions"][name]]
            if emoji in c["reactions"][name]:
                c["reactions"][name].remove(emoji)
                if len(c["reactions"][name]) == 0: del c["reactions"][name]
                save_data()
                remaining = ' '.join(c["reactions"].get(name, [])) if name in c["reactions"] else "تم مسح الكل"
                bot.reply_to(message, f"✅ مسح {emoji} من {name}\n• الباقي: {remaining}")
            else: bot.reply_to(message, f"❌ {emoji} مو موجود")
        else: bot.reply_to(message, "❌ غير موجود")
    else:
        name = full
        if name in c["reactions"]: del c["reactions"][name]; save_data(); bot.reply_to(message, f"✅ تم مسح كل تفاعلات {name}")
        else: bot.reply_to(message, "❌ غير موجود")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["التفاعلات","تفاعلات"])
def list_react(message):
    if message.chat.type == 'private': return
    c = get_chat_data(str(message.chat.id))
    reacts = c.get("reactions", {})
    if not reacts: bot.reply_to(message, "لا يوجد تفاعلات"); return
    txt = "• تفاعلات القروب (حد 5):\n"
    for n,e in reacts.items():
        if isinstance(e, list): txt += f"• {n} => {' '.join(e)} ({len(e)}/5)\n"
        else: txt += f"• {n} => {e}\n"
    bot.reply_to(message, txt)

@bot.message_handler(content_types=['photo','video','sticker','animation','text'], func=lambda m: m.chat.type!= 'private')
def main_handler(message):
    chat_id = str(message.chat.id)
    c = get_chat_data(chat_id)
    if message.from_user: add_user(message.from_user)
    if not has_role(chat_id, message.from_user.id, "admins"):
        locks = c.get("locks", {})
        try:
            if message.content_type == 'photo' and locks.get("الصور"): bot.delete_message(message.chat.id, message.message_id); return
            if message.content_type == 'video' and locks.get("الفيديو"): bot.delete_message(message.chat.id, message.message_id); return
            if message.content_type == 'sticker' and locks.get("الملصقات"): bot.delete_message(message.chat.id, message.message_id); return
            if message.content_type == 'animation' and locks.get("المتحركه"): bot.delete_message(message.chat.id, message.message_id); return
            if message.text and locks.get("الروابط") and ("http" in message.text or "t.me" in message.text): bot.delete_message(message.chat.id, message.message_id); return
            if locks.get("الكل"): bot.delete_message(message.chat.id, message.message_id); return
        except: pass
    if message.text:
        text_lower = message.text.lower()
        for name, emojis in c.get("reactions", {}).items():
            if name.lower() in text_lower:
                if isinstance(emojis, str): emojis = [emojis]
                reaction_list = []
                for em in emojis[:5]:
                    try: reaction_list.append(types.ReactionTypeEmoji(em))
                    except: reaction_list.append({"type":"emoji","emoji":em})
                try: bot.set_message_reaction(message.chat.id, message.message_id, reaction=reaction_list)
                except:
                    try: bot.set_message_reaction(message.chat.id, message.message_id, reaction=[{"type":"emoji","emoji":e} for e in emojis[:5]])
                    except: pass
                break
        bot_name = c.get("bot_name", "اسود").lower()
        if bot_name in text_lower:
            if c.get("replies_enabled", True):
                try: bot.set_message_reaction(message.chat.id, message.message_id, reaction=[types.ReactionTypeEmoji("🖤")])
                except: pass
                bot.reply_to(message, random.choice(ASWAD_REPLIES)); return
    if message.text:
        txt_strip = message.text.strip()
        block_list = ["رفع","تنزيل","قفل","فتح","حظر","طرد","الاوامر","تفعيل","تعطيل","ضع تفاعل","مسح تفاعل","التفاعلات","يوت","بحث","همس","ايدي","م1","م2","م3"]
        if txt_strip == "ه" or any(txt_strip.startswith(k+" ") or txt_strip==k for k in block_list):
            return
    if not c.get("replies_enabled", True): return
    if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == BOT_ID:
        bot.reply_to(message, random.choice(RANDOM_REPLIES)); return
    if random.random() < 0.20: bot.reply_to(message, random.choice(RANDOM_REPLIES))

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الاوامر","اوامر","م1","م2","م3"])
def show_cmds(message):
    if message.chat.type == 'private': return
    mk = types.InlineKeyboardMarkup(row_width=3)
    mk.add(types.InlineKeyboardButton("① ادمنية", callback_data="m1"), types.InlineKeyboardButton("② تفاعلات", callback_data="m2"), types.InlineKeyboardButton("③ قفل", callback_data="m3"))
    mk.add(types.InlineKeyboardButton("اخفاء", callback_data="hide"))
    bot.send_message(message.chat.id, "- اهلاً اسود 🖤\n• م1 ادمنية\n• م2 تفاعلات (حد 5)\n• م3 قفل\n• تفعيل/تعطيل الردود\n• يوت/بحث\n• ضع تفاعل", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text and ("رفع" in m.text or "تنزيل" in m.text))
def handle_ranks(message):
    if message.chat.type == 'private': return
    if not message.reply_to_message: return
    target = message.reply_to_message.from_user
    if not target or target.is_bot: return
    chat_id = str(message.chat.id); c = get_chat_data(chat_id)
    role_map = {"مالك اساسي": "asasy", "مالك": "owners", "منشئ": "creators", "منشى": "creators", "مدير": "managers", "ادمن": "admins", "مميز": "special"}
    found = None
    for k,v in role_map.items():
        if k in message.text: found = v; break
    if not found: return
    if found == "asasy" and not is_sudo(message.from_user.id): bot.reply_to(message, "❌ فقط اسود"); return
    if not has_role(chat_id, message.from_user.id, "managers") and not is_sudo(message.from_user.id): bot.reply_to(message, "❌ ما عندك صلاحية"); return
    sid = str(target.id)
    if "رفع" in message.text:
        if sid not in c[found]: c[found].append(sid); save_data(); bot.reply_to(message, f"✅ تم رفع {target.first_name}")
    else:
        if sid in c[found]: c[found].remove(sid); save_data(); bot.reply_to(message, f"✅ تم تنزيل {target.first_name}")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تفعيل الردود","تعطيل الردود"])
def toggle_replies(message):
    if message.chat.type == 'private': return
    if not has_role(message.chat.id, message.from_user.id, "managers"): return
    c = get_chat_data(str(message.chat.id))
    if "تفعيل" in message.text: c["replies_enabled"] = True; save_data(); bot.reply_to(message, "✅ تم تفعيل الردود 🖤")
    else: c["replies_enabled"] = False; save_data(); bot.reply_to(message, "❌ تم تعطيل الردود")

@bot.message_handler(func=lambda m: m.text and (m.text.strip().startswith("قفل ") or m.text.strip().startswith("فتح ")))
def locks_handler(message):
    if message.chat.type == 'private': return
    if not has_role(message.chat.id, message.from_user.id, "managers"): return
    c = get_chat_data(str(message.chat.id))
    if "locks" not in c: c["locks"] = {}
    typ = message.text.replace("قفل ","").replace("فتح ","").strip()
    if "قفل" in message.text: c["locks"][typ] = True; save_data(); bot.reply_to(message, f"🔒 تم قفل {typ}")
    else: c["locks"][typ] = False; save_data(); bot.reply_to(message, f"🔓 تم فتح {typ}")

@bot.message_handler(func=lambda m: m.text and (m.text.strip() == "ه" or (m.text and m.text.strip().startswith("همس"))))
def whisper_init(message):
    if message.chat.type == 'private': return
    if not message.reply_to_message: return
    target = message.reply_to_message.from_user
    if not target: return
    if target.id == message.from_user.id: bot.reply_to(message, "❌ ما تهمس لنفسك"); return
    wid = str(uuid.uuid4())[:8]
    whispers[wid] = {"from_id": message.from_user.id, "from_name": message.from_user.first_name, "to_id": target.id, "to_name": target.first_name, "group_id": message.chat.id, "text": None}
    save_whispers()
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton(f"اكتب همستك لـ {target.first_name}", url=f"https://t.me/{BOT_USERNAME}?start={wid}"))
    bot.reply_to(message, f"• همسه لـ {target.first_name} 🕊️ اضغط واكتب بالخاص", reply_markup=mk)

@bot.message_handler(func=lambda m: m.text and m.text.strip() == "ايدي")
def send_id(message):
    add_user(message.from_user)
    txt = f"• ايديك: {message.from_user.id}\n• ايدي القروب: {message.chat.id}"
    bot.reply_to(message, txt)

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    try:
        if call.data == "hide":
            bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data.startswith("view_"):
            wid = call.data.replace("view_","")
            w = whispers.get(wid)
            if not w: bot.answer_callback_query(call.id, "انتهت"); return
            if call.from_user.id!= w["to_id"] and not is_sudo(call.from_user.id): bot.answer_callback_query(call.id, f"الهمسه لـ {w['to_name']} فقط 🕊️", show_alert=True); return
            bot.answer_callback_query(call.id, f"همسة من {w['from_name']}: {w['text']}", show_alert=True)
        elif call.data.startswith("re_"):
            parts = call.data.replace("re_","").split("_")
            if len(parts)>=2:
                to_id = int(parts[0]); gid = parts[1]
                wid2 = str(uuid.uuid4())[:8]
                whispers[wid2] = {"from_id": call.from_user.id, "from_name": call.from_user.first_name, "to_id": to_id, "to_name": "رد", "group_id": int(gid) if gid.lstrip('-').isdigit() else gid, "text": None}
                save_whispers()
                mk = types.InlineKeyboardMarkup()
                mk.add(types.InlineKeyboardButton(f"اكتب ردك", url=f"https://t.me/{BOT_USERNAME}?start={wid2}"))
                bot.send_message(call.message.chat.id, f"• رد لـ {call.from_user.first_name}", reply_markup=mk)
        elif call.data == "m1": bot.edit_message_text("م1:\n• رفع مالك اساسي/مالك/منشئ/مدير/ادمن/مميز (بالرد)\n• تنزيل نفسها\n• تفعيل/تعطيل الردود\n• قفل/فتح", call.message.chat.id, call.message.message_id)
        elif call.data == "m2": bot.edit_message_text("م2 تفاعلات (حد 5 لكل اسم):\n• ضع تفاعل + الاسم 🌹\n• تقدر: ضع تفاعل محمد 🌹 ❤️ 🔥\n• بعدها ارسل ايموجي\n• مسح تفاعل + الاسم + الايموجي\n• التفاعلات", call.message.chat.id, call.message.message_id)
        elif call.data == "m3": bot.edit_message_text("م3:\n• قفل/فتح الصور/الفيديو/الملصقات/المتحركه/الروابط/الكل\n• ه او همس (بالرد)\n• ايدي\n• يوت + اغنية", call.message.chat.id, call.message.message_id)
    except:
        try: bot.answer_callback_query(call.id, "❌")
        except: pass

@bot.message_handler(commands=['start'])
def start_cmd(message):
    add_user(message.from_user)
    args = message.text.split()
    if len(args) > 1:
        wid = args[1]
        w = whispers.get(wid)
        if w:
            pending[message.from_user.id] = wid
            bot.send_message(message.chat.id, f"• اكتب همستك لـ {w['to_name']} 🕊️\n• سيتم حذفها تلقائيا بعد الارسال")
            return
    bot.send_message(message.chat.id, f"هلا 🖤 @{BOT_USERNAME}\n• ارسل في القروب: ه بالرد لهمس")

if __name__ == "__main__":
    print(f"Bot @{BOT_USERNAME} started")
    bot.infinity_polling(skip_pending=True)
