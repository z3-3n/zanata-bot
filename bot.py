import telebot
import os
import random

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ========== ردود القلب الأسود ==========
replies_list = [
    "هلا يا قلب اسود 🖤",
    "قلبي اسود وناسيك 🖤😈",
    "لا تكلمني كثير قلبي اسود ما يتحمل 🖤",
    "طيب يا اسود القلب 🖤",
    "ههههه ضحكة قلب ميت 🖤",
    "احبك؟ قلبي اسود ما يعرف يحب 🖤",
    "صباح السواد 🖤😈",
    "مساء قلب ميت 🖤",
    "روح سوّد قلبك وتعال 🖤",
    "يا مرحبا بلي قلبه اسود مثلي 🖤"
]

ROAST = [
    "قلبك مو اسود انت بس ملقوف 🖤😂",
    "روح سوّد قلبك اول 🖤😈",
    "مادخلك يا قلب ابيض مسوي اسود؟ 🖤",
    "اللقافة بقلب اسود؟ استحي 🖤",
    "خليك في سوادك لا تدخل سواد غيرك 🖤"
]

QUOTES = [
    "قلبي أسود لأني شفت كثير.. مو لأني ولدت كذا 🖤",
    "لا تثق بقلب اسود.. حتى لو قال احبك 🖤😈",
    "القلب الأسود ما ينكسر.. هو اللي يكسر 🖤",
    "كنت قلب ابيض.. لين علمتوني السواد 🖤",
    "قلبي اسود بس صادق.. مو ابيض وكذاب 🖤",
    "السواد اللي بقلبي.. هو اللي مخليني عايش 🖤😈",
    "لا تقرب.. قلبي اسود ويحرق 🖤",
    "اضحك وقلبي اسود.. عادي 🖤😂"
]

NASIHA = [
    "نصيحة قلب اسود: لا تثق بأحد 🖤",
    "نصيحة: سوّد قلبك بتعيش مرتاح 🖤😈",
    "نصيحة: اللي يحبك بقلب ابيض.. بيخونك بقلب اسود 🖤",
    "لا تعطي قلبك كامل.. خلي نصه اسود لك 🖤",
    "الطيبة بزمننا ضعف.. سوّد قلبك 🖤"
]

LOVE_BLACK = [
    "احبك بقلب اسود.. يعني ما انساك لو مت 🖤😈",
    "حب القلب الأسود ما ينتهي.. يتحول كره 🖤",
    "احبك وقلبي اسود.. يعني اغار واجنن 🖤",
    "حبي اسود.. يخنق 🖤😍"
]

BOT_ID = None
def get_bot_id():
    global BOT_ID
    if BOT_ID is None:
        BOT_ID = bot.get_me().id
    return BOT_ID

# ========== الأوامر ==========
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "هلا والله 🖤\nأنا **بوت قلب أسود** 🖤😈\n\n**أوامري:**\n/quote - حكمة قلب اسود\n/roast - اهينك 🖤\n/love - حب اسود\n/sad - حزن اسود\n/nasiha - نصيحة قلب اسود\n/id - ايدي حقك\n/help - كل الأوامر\n\nفي الخاص ارد عشوائي 🖤\nفي القروب رد على رسائلي وبرد عليك 🖤")

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.reply_to(m, "🖤 **أوامر بوت قلب أسود:** 🖤\n\n/quote - حكمة سوداء\n/roast - تهزيء قلب اسود\n/love - كلام حب اسود\n/sad - كلام حزن اسود\n/nasiha - نصيحة سوداء\n/id - معلوماتك\n/start - البداية\n\n+ في القروب:\n• رد على رسالة واكتب `مادخلك` اهينه\n• رد على رسالة واكتب `همس` همس اسود\n• رد على رسائلي ارد عليك عشوائي 🖤")

@bot.message_handler(commands=['quote','q'])
def quote_cmd(m):
    bot.reply_to(m, f"🖤 {random.choice(QUOTES)}")

@bot.message_handler(commands=['roast','r'])
def roast_cmd(m):
    bot.reply_to(m, f"🖤 {random.choice(ROAST)}")

@bot.message_handler(commands=['love','l'])
def love_cmd(m):
    bot.reply_to(m, f"🖤 {random.choice(LOVE_BLACK)}")

@bot.message_handler(commands=['sad','s'])
def sad_cmd(m):
    bot.reply_to(m, f"🖤 قلب اسود حزين: {random.choice(QUOTES)} 💔🖤")

@bot.message_handler(commands=['nasiha','n'])
def nasiha_cmd(m):
    bot.reply_to(m, f"🖤 {random.choice(NASIHA)}")

@bot.message_handler(commands=['id'])
def id_cmd(m):
    bot.reply_to(m, f"🖤 معلوماتك يا قلب اسود:\n\nاسمك: {m.from_user.first_name}\nايدي: `{m.from_user.id}`\nاليوزر: @{m.from_user.username if m.from_user.username else 'مافي'}\n\nقلبك: اسود 🖤😈", parse_mode="Markdown")

# ========== رسائل عادية ==========
@bot.message_handler(func=lambda m: True, content_types=['text'])
def all_messages(message):
    text_low = (message.text or "").lower()
    bot_id = get_bot_id()

    if message.chat.type == "private" and not message.text.startswith('/'):
        bot.reply_to(message, random.choice(replies_list + QUOTES))
        return

    if "همس" in text_low and message.reply_to_message:
        from telebot import types
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🖤 افتح همس اسود", callback_data="whisper"))
        bot.send_message(message.chat.id, f"🖤 همس اسود من {message.from_user.first_name} 👇", reply_markup=markup, reply_to_message_id=message.reply_to_message.message_id)
        return

    if "مادخلك" in text_low and message.reply_to_message:
        bot.reply_to(message.reply_to_message, random.choice(ROAST))
        return

    if message.reply_to_message and message.reply_to_message.from_user.id == bot_id:
        bot.reply_to(message, random.choice(replies_list))
        return

bot.infinity_polling()
