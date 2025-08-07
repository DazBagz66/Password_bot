import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("1-ая кнопка", callback_data="1"),
            InlineKeyboardButton("2-ая кнопка", callback_data="2")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбирай бля", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"Выбранная кнопка: {query.data}")

def main() -> None:
    application = Application.builder().token('8371099251:AAEsSiD1GaC38er7xCQxK2mRVzbDW2-1cgc').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(start_handler)

    application.run_polling()

if __name__ == '__main__':
    main()