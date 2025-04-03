import logging
import openai
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

openai.api_key = os.getenv("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")
TELEGRAM_BOT_TOKEN = os.getenv("7894050355:AAEH_K-7cfV_aT9vmex0xx1TJ3ezqWv608Q")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
user_model = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("GPT-3.5", callback_data="gpt-3.5-turbo")],
        [InlineKeyboardButton("GPT-4", callback_data="gpt-4")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я GPT-бот. Выбери модель:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_model = query.data
    chat_id = query.message.chat.id
    user_model[chat_id] = selected_model
    await query.edit_message_text(f"Вы выбрали модель: {selected_model}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    model = user_model.get(chat_id, "gpt-3.5-turbo")
    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": user_text}]
        )
        reply = response.choices[0].message["content"].strip()
    except Exception as e:
        logger.error(f"Ошибка OpenAI API: {e}")
        reply = "🚫 Ошибка при обращении к OpenAI. Проверьте токен или модель."
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
