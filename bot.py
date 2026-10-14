import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً @z3_3n ! البوت شغال تمام ✅\nارسل أي ملف أو رسالة.")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"استلمت: {message.text}")

print("Bot is running...")
bot.infinity_polling()
