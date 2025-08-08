import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler
from Password_gen import pass_gen

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

Param = ["Специальные знаки", "Цифры"]


def toggle_button(user_data): # Переключение параметров
    keyboard = []
    for par in Param:
        enabled = user_data.get(par,False)
        emoji = "✅" if enabled else "❌"
        text = f"{emoji}{par}"
        keyboard.append(InlineKeyboardButton(text,callback_data=f"Включённый:{par}"))
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Начальная кнопка
    button = InlineKeyboardButton("Приступим", callback_data="go_to_main_menu")

    reply_markup = InlineKeyboardMarkup([button])

    await update.message.reply_text("Я бот для создания паролей", reply_markup=reply_markup)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    func_button = InlineKeyboardButton(text = "Создать пароль", callback_data="run_action")
    param_buttons = toggle_button(context.user_data)
    menu = [[func_button]] + [[b] for b in param_buttons]
    reply_markup = InlineKeyboardMarkup(menu)

    await query.edit_message_text(text = "Создать пароль или изменить параметр", reply_markup = reply_markup)
    # Todo: Finish buttons query and understand it

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"Выбранная кнопка: {query.data}")

def main() -> None:
    application = Application.builder().token('8371099251:AAEsSiD1GaC38er7xCQxK2mRVzbDW2-1cgc').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(main_menu, pattern = "go_to_main_menu")
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(start_handler)

    application.run_polling()

if __name__ == '__main__':
    main()