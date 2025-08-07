import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler
from Password_gen import pass_gen

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
first_stage, second_stage = 0, 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("1-ая кнопка", callback_data=pass_gen(10))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Я бот для создания паролей", reply_markup=reply_markup)
    return first_stage

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