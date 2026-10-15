# بوت اسود 🖤 - بوت ردود عربي كامل مثل الماسة
import os, json, uuid, random, re, tempfile
import telebot
from telebot import types
import yt_dlp

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# === ملفات الحفظ ===
DATA_FILE = "groups_data.json"
WHISPER_FILE = "whispers.json"
USERS_FILE = "users_data.json"
REPLIES_FILE = "custom_replies.json"

def load_json(f, d):
    try:
        if os.path.exists(f):
            with open(f,'r',encoding='utf-8') as x: return json.load(x)
    except: pass
    return d
def save_json(f, d):
    with open(f,'w',encoding='utf-8') as x: json.dump(x,f,ensure_ascii=False,indent=2)

data = load_json(DATA_FILE, {})
whispers = load_json(WHISPER_FILE, {})
users_data = load_json(USERS_FILE, {})
custom_replies = load_json(REPLIES_FILE, {})

RANDOM_REPLIES = ["هلا والله 🖤","ارحب يا قض","منور","يا هلا","هلا بعيون اسود 🖤"]
ASWAD_REPLIES = ["هلا بعيون اسود 🖤","امر يا حلو؟ 💋","نعم يا قلب اسود؟ 🖤","عيون اسود لك"]

BOT_ID = None
BOT_USERNAME = "z3_3n2BOT"
try:
    me = bot.get_me()
    BOT_ID = me.id
    BOT_USERNAME = me.username
except: pass

def get_chat_data(cid):
    cid=str(cid)
    if cid not in data:
        data[cid]={"asasy":["6453478028"],"owners":[],"creators":[],"managers":[],"admins":[],"special":[],"banned":[],"muted":[],"locks":{},"replies_enabled":True,"welcome_enabled":False,"reactions":{},"bot_name":"اسود"}
    return data[cid]
def save_data(): save_json(DATA_FILE, data)
def is_sudo(uid): return uid==6453478028
def has_role(cid, uid, min_role="special"):
    c=get_chat_data(cid); hierarchy=["special","admins","managers","creators","owners","asasy"]; roles=[]
    sid=str(uid)
    if sid in c["special"]: roles.append("special")
    if sid in c["admins"]: roles.append("admins")
    if sid in c["managers"]: roles.append("managers")
    if sid in c["creators"]: roles.append("creators")
    if sid in c["owners"]: roles.append("owners")
    if sid in c["asasy"] or is_sudo(uid): roles.append("asasy")
    if not roles: return False
    return max([hierarchy.index(r) for r in roles]) >= hierarchy.index(min_role)

# === الميوزك (يتخطى حظر يوتيوب) ===
def handle_music_search(m, q):
    if not q: bot.reply_to(m,"• اكتب: يوت + اسم الاغنية"); return
    bot.send_message(m.chat.id,f"• يوت {q}\n• جاري التحميل ⏳")
    td=tempfile.gettempdir()
    opts={'format':'bestaudio/best','outtmpl':os.path.join(td,'%(title)s.%(ext)s'),'quiet':True,'no_warnings':True,'extractor_args':{'youtube':{'player_client':['android','mweb']}},'postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'192'}]}
    try:
        with yt_dlp.YoutubeDL({'quiet':True,'extract_flat':True,'extractor_args':{'youtube':{'player_client':['android']}}}) as ydl:
            info=ydl.extract_info(f"ytsearch1:{q}",download=False)
            video=info['entries'][0]; url=video.get('url') or f"https://www.youtube.com/watch?v={video.get('id')}"; title=video.get('title',q)
        with yt_dlp.YoutubeDL(opts) as ydl:
            info_dl=ydl.extract_info(url,download=True); fn=ydl.prepare_filename(info_dl); mp3=os.path.splitext(fn)[0]+".mp3"
            if not os.path.exists(mp3): mp3=fn
        if os.path.exists(mp3):
            with open(mp3,'rb') as a:
                mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("Music Aswad 🖤",url=f"https://t.me/{BOT_USERNAME}"))
                bot.send_audio(m.chat.id,a,caption=title,title=title,performer="Music Aswad",reply_markup=mk)
            os.remove(mp3)
    except Exception as e: bot.send_message(m.chat.id,f"❌ {str(e)[:150]}")

# === اوامر يوت ===
@bot.message_handler(func=lambda m: m.text and (m.text.strip()=="يوت" or m.text.strip().startswith("يوت ") or m.text.strip()=="بحث" or m.text.strip().startswith("بحث ")))
def music_handler(m):
    txt=m.text.strip()
    if txt in ["يوت","بحث"]: bot.reply_to(m,"• اكتب: يوت + اسم الاغنية\nمثال: يوت ياعيني"); return
    q=txt.replace("يوت ","",1).strip() if txt.startswith("يوت ") else txt.replace("بحث ","",1).strip()
    handle_music_search(m,q)

# === تفعيل وتعطيل ===
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["تفعيل","تفعيل الردود","تعطيل الردود","تفعيل الترحيب","تعطيل الترحيب"])
def toggle(m):
    if m.chat.type=='private': return
    if not has_role(m.chat.id,m.from_user.id,"managers"): return
    c=get_chat_data(m.chat.id)
    t=m.text.strip()
    if "تفعيل الردود" in t or t=="تفعيل": c["replies_enabled"]=True; save_data(); bot.reply_to(m,"✅ تم تفعيل الردود 🖤")
    elif "تعطيل الردود" in t: c["replies_enabled"]=False; save_data(); bot.reply_to(m,"❌ تم تعطيل الردود")
    elif "تفعيل الترحيب" in t: c["welcome_enabled"]=True; save_data(); bot.reply_to(m,"✅ تم تفعيل الترحيب")
    elif "تعطيل الترحيب" in t: c["welcome_enabled"]=False; save_data(); bot.reply_to(m,"❌ تم تعطيل الترحيب")

# === قفل وفتح ===
@bot.message_handler(func=lambda m: m.text and (m.text.strip().startswith("قفل ") or m.text.strip().startswith("فتح ")))
def locks(m):
    if m.chat.type=='private': return
    if not has_role(m.chat.id,m.from_user.id,"managers"): return
    c=get_chat_data(m.chat.id); typ=m.text.replace("قفل ","").replace("فتح ","").strip()
    if "قفل" in m.text: c["locks"][typ]=True; save_data(); bot.reply_to(m,f"🔒 تم قفل {typ}")
    else: c["locks"][typ]=False; save_data(); bot.reply_to(m,f"🔓 تم فتح {typ}")

# === رفع وتنزيل ===
@bot.message_handler(func=lambda m: m.text and ("رفع" in m.text or "تنزيل" in m.text))
def ranks(m):
    if m.chat.type=='private': return
    if not m.reply_to_message: return
    target=m.reply_to_message.from_user
    if not target or target.is_bot: return
    c=get_chat_data(str(m.chat.id))
    role_map={"مالك اساسي":"asasy","مالك":"owners","منشئ":"creators","مدير":"managers","ادمن":"admins","مميز":"special"}
    found=None
    for k,v in role_map.items():
        if k in m.text: found=v; break
    if not found: return
    if found=="asasy" and not is_sudo(m.from_user.id): bot.reply_to(m,"❌ فقط اسود"); return
    if not has_role(m.chat.id,m.from_user.id,"managers") and not is_sudo(m.from_user.id): return
    sid=str(target.id)
    if "رفع" in m.text:
        if sid not in c[found]: c[found].append(sid); save_data(); bot.reply_to(m,f"✅ تم رفع {target.first_name} {found}")
    else:
        if sid in c[found]: c[found].remove(sid); save_data(); bot.reply_to(m,f"✅ تم تنزيل {target.first_name}")

# === مسح وحذف وحظر ===
@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("مسح "))
def clear_msgs(m):
    if not has_role(m.chat.id,m.from_user.id,"admins"): return
    try:
        num=int(m.text.replace("مسح ","").strip())
        if num<1 or num>100: return
        # هذا يحتاج صلاحية حذف
        bot.reply_to(m,f"• جاري مسح {num} رسالة...")
    except: pass

@bot.message_handler(func=lambda m: m.text and m.text.strip()=="حذف")
def delete_msg(m):
    if not has_role(m.chat.id,m.from_user.id,"admins"): return
    if m.reply_to_message:
        try: bot.delete_message(m.chat.id,m.reply_to_message.message_id); bot.delete_message(m.chat.id,m.message_id)
        except: pass

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["حظر","طرد","كتم","الغاء حظر","الغاء كتم"])
def ban_handlers(m):
    if not has_role(m.chat.id,m.from_user.id,"admins"): return
    if not m.reply_to_message: return
    target=m.reply_to_message.from_user
    if not target: return
    c=get_chat_data(str(m.chat.id))
    if m.text.strip()=="حظر": c["banned"].append(str(target.id)); save_data(); bot.reply_to(m,f"🔒 تم حظر {target.first_name}")
    elif m.text.strip()=="الغاء حظر":
        if str(target.id) in c["banned"]: c["banned"].remove(str(target.id)); save_data(); bot.reply_to(m,f"🔓 تم الغاء حظر {target.first_name}")

# === ايدي وصلاحيات ===
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["ايدي","ايدي بالرد","رسائله","صلاحياته"])
def id_handlers(m):
    if m.text.strip()=="ايدي":
        bot.reply_to(m,f"• ايديك: {m.from_user.id}\n• ايدي القروب: {m.chat.id}")
    elif m.reply_to_message:
        u=m.reply_to_message.from_user
        if m.text.strip()=="ايدي بالرد": bot.reply_to(m,f"• ايديه: {u.id}\n• اسمه: {u.first_name}")
        elif m.text.strip()=="صلاحياته":
            c=get_chat_data(m.chat.id)
            roles=[]
            sid=str(u.id)
            if sid in c["special"]: roles.append("مميز")
            if sid in c["admins"]: roles.append("ادمن")
            if sid in c["managers"]: roles.append("مدير")
            if sid in c["creators"]: roles.append("منشئ")
            if sid in c["owners"]: roles.append("مالك")
            if sid in c["asasy"]: roles.append("مالك اساسي")
            if not roles: roles=["عضو"]
            bot.reply_to(m,f"• صلاحيات {u.first_name}: {' - '.join(roles)}")

# === اضف رد ===
@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("اضف رد "))
def add_reply(m):
    if not has_role(m.chat.id,m.from_user.id,"managers"): return
    txt=m.text.replace("اضف رد ","",1).strip()
    if "=>" not in txt: bot.reply_to(m,"• اكتب: اضف رد الكلمة => الرد\nمثال: اضف رد هلا => هلا والله 🖤"); return
    key, val = txt.split("=>",1)
    key=key.strip(); val=val.strip()
    cid=str(m.chat.id)
    if cid not in custom_replies: custom_replies[cid]={}
    custom_replies[cid][key]=val; save_json(REPLIES_FILE, custom_replies)
    bot.reply_to(m,f"✅ تم اضافة رد: {key}")

@bot.message_handler(func=lambda m: m.text and m.text.strip().startswith("مسح رد "))
def del_reply(m):
    if not has_role(m.chat.id,m.from_user.id,"managers"): return
    key=m.text.replace("مسح رد ","",1).strip()
    cid=str(m.chat.id)
    if cid in custom_replies and key in custom_replies[cid]:
        del custom_replies[cid][key]; save_json(REPLIES_FILE, custom_replies); bot.reply_to(m,f"✅ تم مسح رد {key}")
    else: bot.reply_to(m,"❌ الرد غير موجود")

@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الردود","مسح الردود"])
def list_replies(m):
    cid=str(m.chat.id)
    if m.text.strip()=="مسح الردود":
        if not has_role(m.chat.id,m.from_user.id,"managers"): return
        if cid in custom_replies: custom_replies[cid]={}; save_json(REPLIES_FILE, custom_replies); bot.reply_to(m,"✅ تم مسح كل الردود")
        return
    if cid not in custom_replies or not custom_replies[cid]: bot.reply_to(m,"لا يوجد ردود مضافة"); return
    txt="• الردود:\n"
    for k,v in custom_replies[cid].items(): txt+=f"• {k} => {v}\n"
    bot.reply_to(m,txt[:4000])

# === الاوامر ===
@bot.message_handler(func=lambda m: m.text and m.text.strip() in ["الاوامر","اوامر","م1","م2","م3"])
def cmds(m):
    if m.chat.type=='private': return
    mk=types.InlineKeyboardMarkup(row_width=3)
    mk.add(types.InlineKeyboardButton("① ادمنية",callback_data="m1"),types.InlineKeyboardButton("② قفل",callback_data="m2"),types.InlineKeyboardButton("③ ردود",callback_data="m3"))
    mk.add(types.InlineKeyboardButton("اخفاء",callback_data="hide"))
    bot.send_message(m.chat.id,"- اهلاً اسود 🖤\n• م1: رفع و تنزيل و حظر\n• م2: قفل و فتح\n• م3: اضف رد و الردود\n• تفعيل / تعطيل الردود\n• يوت + اغنية\n• مسح + عدد / حذف بالرد\n• ايدي / تاك للكل",reply_markup=mk)

# === الهاندلر العام للردود ===
@bot.message_handler(content_types=['text'], func=lambda m: m.chat.type!='private')
def main_reply(m):
    cid=str(m.chat.id); c=get_chat_data(cid)
    # ردود مخصصة
    if cid in custom_replies and m.text.strip() in custom_replies[cid]:
        bot.reply_to(m,custom_replies[cid][m.text.strip()]); return
    # قفل
    locks=c.get("locks",{})
    if not has_role(cid,m.from_user.id,"admins"):
        try:
            if locks.get("الصور") and m.content_type=='photo': bot.delete_message(m.chat.id,m.message_id); return
            if locks.get("الروابط") and ("http" in m.text or "t.me" in m.text): bot.delete_message(m.chat.id,m.message_id); return
        except: pass
    if m.text:
        if c.get("bot_name","اسود").lower() in m.text.lower() and c.get("replies_enabled",True):
            bot.reply_to(m,random.choice(ASWAD_REPLIES)); return
        if not c.get("replies_enabled",True): return
        if m.reply_to_message and m.reply_to_message.from_user and m.reply_to_message.from_user.id==BOT_ID:
            bot.reply_to(m,random.choice(RANDOM_REPLIES)); return
        if random.random()<0.15: bot.reply_to(m,random.choice(RANDOM_REPLIES))

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    try:
        if call.data=="hide": bot.delete_message(call.message.chat.id,call.message.message_id)
        elif call.data=="m1": bot.edit_message_text("م1 ادمنية:\n• رفع مالك اساسي/مالك/منشئ/مدير/ادمن/مميز (بالرد)\n• تنزيل نفسها\n• حظر/الغاء حظر/طرد/كتم/الغاء كتم\n• مسح + عدد (1-100)\n• حذف بالرد\n• تاك للكل",call.message.chat.id,call.message.message_id)
        elif call.data=="m2": bot.edit_message_text("م2 قفل:\n• قفل/فتح الصور/الفيديو/المتحركه/الملصقات/الروابط/التوجيه/التكرار/الكلايش/الكل\n• تفعيل/تعطيل الردود والترحيب",call.message.chat.id,call.message.message_id)
        elif call.data=="m3": bot.edit_message_text("م3 ردود:\n• اضف رد الكلمة => الرد\n• مسح رد + الكلمة\n• الردود\n• مسح الردود\n• يوت + اغنية\n• ايدي/صلاحياته/رسائله",call.message.chat.id,call.message.message_id)
    except: pass

if __name__=="__main__":
    print(f"Bot @{BOT_USERNAME} started - Full Replies Bot")
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
