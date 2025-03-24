import openai
import telebot
import os
from supabase import create_client
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Читаем ключи из .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Создаем клиентов
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.text}]
    )
    
    bot_reply = response["choices"][0]["message"]["content"]

    supabase.table("messages").insert({
        "user_id": str(message.chat.id),
        "message": message.text,
        "response": bot_reply
    }).execute()

    bot.send_message(message.chat.id, bot_reply)

bot.polling()
