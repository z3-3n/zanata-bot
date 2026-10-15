import telebot, os, random

TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

R = [
"هلا يا قلب اسود 🖤",
"قلبي اسود وناسيك 🖤😈",
"لا تكلمني كثير قلبي اسود 🖤",
"طيب يا اسود القلب 🖤",
"ههههه ضحكة قلب ميت 🖤",
"احبك؟ قلبي اسود ما يعرف يحب 🖤",
"صباح السواد 🖤😈",
"مساء قلب ميت 🖤"
]

Q = [
"قلبي أسود لأني شفت كثير مو لأني ولدت كذا 🖤",
"لا تثق بقلب اسود حتى لو قال احبك 🖤😈",
"القلب الأسود ما ينكسر هو اللي يكسر 🖤",
"كنت قلب ابيض لين علمتوني السواد 🖤",
"قلبي اسود بس صادق مو ابيض وكذاب 🖤",
"السواد اللي بقلبي هو اللي مخليني عايش 🖤😈"
]

@bot.message_handler(commands=['start','help'])
def start(m):
    bot.reply_to(m, "هلا 🖤 انا بوت قلب اسود 🖤😈\n/quote - حكمة سوداء\n/id - ايديك")

@bot.message_handler(commands=['quote','q'])
def quote(m):
    bot.reply_to(m, f"🖤 {random.choice(Q)}")

@bot.message_handler(commands=['id'])
def ids(m):
    bot.reply_to(m, f"🖤 ايديك: {m.from_user.id}")

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    bot.reply_to(message, random.choice(R+Q))

bot.infinity_polling()
