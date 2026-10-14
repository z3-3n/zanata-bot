import telebot
import os
import random
from telebot import types
TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
replies = {"هلا": "هلا وغلا والله 😍","مرحبا": "مرحبتين يا حلو 😘","السلام عليكم": "وعليكم السلام 😇"}
ROAST = ["امك عارفه انك بالتيليجرام؟ 🫣","خليك في حالك يا حشري 😂","مادخلك؟ روح شوف لك شغلة 🤣"]
whispers = {}
@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "هلا والله بوت زناطة شغال 😍")
@bot.message_handler(func=lambda m: True)
def all_msg(m):
    t = (m.text or "").lower()
    if "همس" in t and m.reply_to_message:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("👁️ افتح الهمس", callback_data="whisper"))
        bot.send_message(m.chat.id, f"همس الى {m.reply_to_message.from_user.first_name} 🤫", reply_markup=markup, reply_to_message_id=m.reply_to_message.message_id)
        return
    if "مادخلك" in t and m.reply_to_message:
        bot.reply_to(m.reply_to_message, random.choice(ROAST))
        return
    for k,v in replies.items():
        if k in t:
            bot.reply_to(m, v)
            return
bot.infinity_polling()
