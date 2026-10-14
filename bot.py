import telebot
import os
import json
import random
from telebot import types

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- ملفات الحفظ ---
def load(p, d):
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except: return d
def save(p, data):
    with open(p, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

replies = load("replies.json", {
    "هلا": "هلا وغلا والله 🌝🖤",
    "مرحبا": "مرحبتين يا حلو 🙂🖤",
    "السلام عليكم": "وعليكم السلام ورحمة الله 🌞🖤",
    "هاي": "حيا حيا 😍🖤",
    "شلونك": "بخير دامك بخير 🦦🖤",
    "وينك": "موجود في قلبك 🥲🖤"
})
whispers = {} # id -> data
settings = load("settings.json", {"enabled": True})

# --- قائمة الزبج / الردود المضحكة لما يقولون للبوت مادخلك ---
ROAST_REPLIES = [
    "امك عارفه انك بالتلجرام؟ 🦦🖤",
    "تعال خاص نحكي ونترمسس 🙂🖤",
    "من كلمك؟ اكلم الحلوين بس 🌝🖤",
    "اهدا لا يطق لك عرق 🫩💔",
    "يا هلا باللي اذا سكت القروب يرتاح 🧘🖤",
    "انت كلامك واجد وفعلك ساكت 😕🤦",
    "خليك حبوب لا تقلب نكد 🫩💔",
    "ذكائك اليوم طالع اجازة 🧑‍🦯🫩",
    "انت الحلو اللي يرفع الضغط 🙂‍↕️💔",
    "لا تكثر شرح فهمنا من اول كلمة 🙂‍↕️🙂",
    "يا مرحبا بملك الزنط 🌝🌚",
    "اسكت شوية خلي الاكسجين يوصل 🫩🌞",
    "يا اخي انت نكتة تمشي 🏃🌝",
    "انت ثقيل بس دمك عسل 🦥🖤",
    "صياح على الفاضي يا فنان 🔥🙂‍↕️",
    "خليك بعيد الحلا يبقى احلى 🌝🖤",
    "لو السكوت ذهب انت فحم 🖤🔥",
    "قوم شوف لك شغلة 🏃🫩",
    "روح نام الليل نصه 🌚🧘",
    "انت وجودك محتوى 🙂🌝",
    "تتكلم كثير وتنجز قليل 😕🤌🏻",
    "مكانك معروف لا تضيع 🧑‍🦯🏃"
]

waiting = {}

def is_admin(chat_id, user_id):
    try:
        st = bot.get_chat_member(chat_id, user_id).status
        return st in ['administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "أهلاً! أنا بوت زناطة صنعانية 🤖🔥\nضيفني قروب وارفعني مشرف واستمتع بالردود والهمس والكتم\n\nالأوامر:\nاضف رد - حذف رد - الردود\nهمس - تاك - كتم - حظر")

# --- اضافة رد ---
@bot.message_handler(func=lambda x: x.text and x.text.strip() in ["اضف رد", "إضافة رد", "➕ اضف رد"])
def add1(m):
    if m.chat.type!= 'private' and not is_admin(m.chat.id, m.from_user.id):
        bot.reply_to(m, "❌ للمشرفين فقط")
        return
    waiting[m.chat.id] = {"a": "trig", "uid": m.from_user.id}
    bot.reply_to(m, "أرسل الكلمة اللي تبي أرد عليها:")

# --- حذف رد ---
@bot.message_handler(func=lambda x: x.text and x.text.strip() in ["حذف رد", "🗑️ حذف رد"])
def del1(m):
    waiting[m.chat.id] = {"a": "del", "uid": m.from_user.id}
    bot.reply_to(m, "أرسل الكلمة اللي تبي تحذفها:")

@bot.message_handler(func=lambda x: x.text and x.text.strip() in ["الردود", "قائمة الردود", "📋 قائمة الردود"])
def list_r(m):
    if not replies:
        bot.reply_to(m, "ما في ردود")
        return
    txt = "📋 الردود:\n"
    for k,v in replies.items(): txt+=f"- {k} => {v[:30]}\n"
    bot.reply_to(m, txt)

# --- همس ---
@bot.message_handler(func=lambda x: x.text and x.text.lower().startswith("همس"))
def hams(m):
    try:
        # صيغة: همس @username الرسالة او رد على رسالة وكتابة همس الرسالة
        parts = m.text.split(" ", 2)
        if len(parts) < 2:
            bot.reply_to(m, "طريقة الهمس: همس @الشخص الرسالة\nأو رد على رسالة الشخص واكتب همس + رسالتك")
            return

        target = None
        hams_text = ""
        if m.reply_to_message:
            target = m.reply_to_message.from_user
            hams_text = m.text.replace("همس", "").strip()
        else:
            # يدور منشن
            if "@" in m.text:
                # نحاول ناخذ اليوزر
                hams_text = parts[2] if len(parts)>2 else "همسة 😉"
            else:
                bot.reply_to(m, "منشن الشخص أو رد على رسالته")
                return

        wid = str(random.randint(10000,999999))
        whispers[wid] = {"from": m.from_user.id, "text": hams_text, "to_id": target.id if target else 0, "to_name": target.first_name if target else parts[1]}

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"👁️ همسة لـ {whispers[wid]['to_name']}", callback_data=f"hams_{wid}"))

        bot.send_message(m.chat.id, f"🤫 {m.from_user.first_name} أرسل همسة إلى {whispers[wid]['to_name']}", reply_markup=markup)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda c: c.data.startswith("hams_"))
def show_hams(call):
    wid = call.data.split("_")[1]
    data = whispers.get(wid)
    if not data:
        bot.answer_callback_query(call.id, "انتهت الهمسة")
        return
    # يسمح فقط للمرسل له أو المرسل
    if call.from_user.id!= data["to_id"] and call.from_user.id!= data["from"] and data["to_id"]!= 0:
        bot.answer_callback_query(call.id, f"الهمسة مو لك، هي لـ {data['to_name']} فقط 🤫", show_alert=True)
        return
    bot.answer_callback_query(call.id, f"الهمسة: {data['text']}", show_alert=True)

# --- كتم / حظر ---
@bot.message_handler(func=lambda x: x.text and x.text.startswith("كتم"))
def mute(m):
    if not is_admin(m.chat.id, m.from_user.id): return
    if not m.reply_to_message:
        bot.reply_to(m, "رد على الشخص اللي تبي تكتمه واكتب كتم")
        return
    try:
        bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, until_date=0, can_send_messages=False)
        bot.reply_to(m, f"🔇 تم كتم {m.reply_to_message.from_user.first_name}")
    except: bot.reply_to(m, "ما قدرت اكتمه، تأكد اني مشرف وعندي صلاحية")

@bot.message_handler(func=lambda x: x.text and x.text.startswith("الغاء الكتم"))
def unmute(m):
    if not is_admin(m.chat.id, m.from_user.id): return
    if not m.reply_to_message: return
    try:
        bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(m, f"🔊 تم فك كتم {m.reply_to_message.from_user.first_name}")
    except: pass

@bot.message_handler(func=lambda x: x.text and x.text.startswith("حظر"))
def ban(m):
    if not is_admin(m.chat.id, m.from_user.id): return
    if not m.reply_to_message: return
    try:
        bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
        bot.reply_to(m, f"🚫 تم حظر {m.reply_to_message.from_user.first_name}")
    except: bot.reply_to(m, "ما قدرت احظره")

@bot.message_handler(func=lambda x: x.text and x.text.startswith("تاك") or x.text.startswith("منشن"))
def tag_all(m):
    if not is_admin(m.chat.id, m.from_user.id): return
    # تاك وهمي لان تيليجرام ما يسمح بتاك الكل بدون معرفات
    bot.reply_to(m, "👥 يا حلوين تعالوا @all\n" + m.text.replace("تاك","").replace("منشن",""))

# --- المعالج العام ---
@bot.message_handler(func=lambda m: True, content_types=['text'])
def all_text(m):
    chat_id = m.chat.id

    # انتظار اضافة / حذف
    if chat_id in waiting:
        st = waiting[chat_id]
        if st["a"] == "trig":
            waiting[chat_id] = {"a": "reply", "trig": m.text.strip(), "uid": st["uid"]}
            bot.reply_to(m, f"تمام، اذا احد كتب '{m.text.strip()}' وش أرد؟")
            return
        if st["a"] == "reply":
            replies[st["trig"]] = m.text.strip()
            save("replies.json", replies)
            waiting.pop(chat_id)
            bot.reply_to(m, f"✅ تم حفظ الرد: {st['trig']} => {m.text.strip()}")
            return
        if st["a"] == "del":
            if m.text.strip() in replies:
                del replies[m.text.strip()]
                save("replies.json", replies)
                bot.reply_to(m, "✅ تم الحذف")
            else: bot.reply_to(m, "ما لقيتها")
            waiting.pop(chat_id)
            return

    text = m.text.lower()

    # 1. اذا احد رد على البوت وقاله مادخلك / شدخلك
    if m.reply_to_message and m.reply_to_message.from_user.id == bot.get_me().id:
        if any(w in text for w in ["مادخلك", "ما دخلك", "اش دخلك", "شدخلك", "وش دخلك", "ايش دخلك", "من كلمك"]):
            bot.reply_to(m, random.choice(ROAST_REPLIES))
            return

    # 2. ردود تلقائية عادية
    if not settings.get("enabled"): return
    for trig, rep in replies.items():
        if trig.lower() in text:
            bot.reply_to(m, rep)
            break

print("Zanata Bot Running...")
bot.infinity_polling()
