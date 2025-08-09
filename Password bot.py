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
    row = []
    for par in Param:
        enabled = user_data.get(par,False)
        emoji = "✅" if enabled else "❌"
        text = f"{emoji}{par}"
        row.append([InlineKeyboardButton(text,callback_data=f"Включённый:{par}")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Начальная кнопка
    button = InlineKeyboardButton("Приступим", callback_data="main_menu")

    reply_markup = InlineKeyboardMarkup([[button]])

    await update.message.reply_text("Я бот для создания паролей", reply_markup=reply_markup)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Вы в главном меню")

    func_button = InlineKeyboardButton(text = "Создать пароль", callback_data="run_action")
    param_buttons = toggle_button(context.user_data)
    menu = [[func_button], [param_buttons]]
    reply_markup = InlineKeyboardMarkup(menu)

    await query.edit_message_text(text = "Создать пароль или изменить параметр", reply_markup = reply_markup)

async def query_param(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    param = query.data.split(":",1)[1]

    current = context.user_data.get(param, False)
    context.user_data[param] = not current

    func_button = InlineKeyboardButton(text="Создать пароль", callback_data="run_action")
    param_buttons = toggle_button(context.user_data)
    menu = [[func_button]] + [[b] for b in param_buttons]
    reply_markup = InlineKeyboardMarkup(menu)

    await query.edit_message_text(text="Создать пароль или изменить параметр", reply_markup=reply_markup)

async def run_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    param_1 = context.user_data.get("Специальные знаки", False)
    param_2 = context.user_data.get("Цифры", False)

    await query.edit_message_text(text=f"Ваш пароль: {pass_gen(10, param_2, param_1)}")

def main() -> None:
    application = Application.builder().token('8371099251:AAEsSiD1GaC38er7xCQxK2mRVzbDW2-1cgc').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(CallbackQueryHandler(main_menu, pattern = "^main_menu$"))
    application.add_handler(CallbackQueryHandler(query_param, pattern = "^Включённый:"))
    application.add_handler(CallbackQueryHandler(run_action, pattern = "Ваш пароль:"))
    application.add_handler(start_handler)

    application.run_polling()

if __name__ == '__main__':
    main()