import telebot, os, random, time
TOKEN=os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(TOKEN)
try:
    bot.remove_webhook()
    time.sleep(1)
except: pass
R=["هلا يا قلب اسود 🖤","قلبي اسود وناسيك 🖤😈","لا تكلمني كثير قلبي اسود 🖤","طيب يا اسود القلب 🖤","ضحكة قلب ميت 🖤","احبك؟ قلبي اسود ما يعرف يحب 🖤","صباح السواد 🖤😈","مساء قلب ميت 🖤"]
Q=["قلبي أسود لأني شفت كثير مو لأني ولدت كذا 🖤","لا تثق بقلب اسود حتى لو قال احبك 🖤😈","القلب الأسود ما ينكسر هو اللي يكسر 🖤","كنت قلب ابيض لين علمتوني السواد 🖤","قلبي اسود بس صادق مو ابيض وكذاب 🖤","السواد اللي بقلبي هو اللي مخليني عايش 🖤😈"]
@bot.message_handler(commands=['start','help','quote','id'])
def h(m):
 c=m.text
 if '/quote' in c: bot.reply_to(m, f"🖤 {random.choice(Q)}")
 elif '/start' in c: bot.reply_to(m, "هلا 🖤 انا بوت قلب اسود V3 🖤😈\n/quote - حكمة")
 elif '/id' in c: bot.reply_to(m, f"🖤 ايديك: {m.from_user.id}")
 else: bot.reply_to(m, random.choice(R))
@bot.message_handler(func=lambda m:True)
def a(message): bot.reply_to(message, random.choice(R+Q))
print("Bot is running V3")
bot.infinity_polling(skip_pending=True, allowed_updates=["message"])
