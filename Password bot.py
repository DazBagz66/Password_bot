import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler, filters, MessageHandler
from Password_gen import pass_gen
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
""" Параметры """
Param = ["Специальные знаки", "Цифры"]
def_length = 8
load_dotenv()
bot_token = os.getenv("TOKEN")

""" Первоначальное сообщение """
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: # Начальная кнопка
    button = InlineKeyboardButton("Приступим", callback_data="main_menu")

    reply_markup = InlineKeyboardMarkup([[button]])
    context.user_data["length"] = def_length
    for par in Param:
        context.user_data[par] = True


    await update.message.reply_text("Я бот для создания паролей", reply_markup=reply_markup)

""" Кнопки главного меню """
def toggle_button(user_data: dict): # Переключение параметров
    keyboard = []
    keyboard.append(
        [InlineKeyboardButton("Задать длину", callback_data="set_length"),
         InlineKeyboardButton("Создать пароль", callback_data="run_action")])
    for par in Param:
        enabled = user_data.get(par,False)
        emoji = "✅" if enabled else "❌"
        text = f"{emoji} {par}"
        keyboard.append(
            [InlineKeyboardButton(text,callback_data=f"toggle:{par}")])
    return InlineKeyboardMarkup(keyboard)

""" Возвращение в главное меню после длины и нажатия кнопки "Приступим" """
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "Главное меню:",
            reply_markup=toggle_button(context.user_data)
        )
    else:
        await update.message.reply_text(
            "Главное меню:",
            reply_markup=toggle_button(context.user_data)
        )
""" Сообщение на нажатие кнопки длины """
async def ask_length(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Введите длину пароля (число от 4 до 64):")

    context.user_data["waiting_length"] = True

""" Обработка количества попыток ввода длины """
async def handle_length(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "len_attempts" not in context.user_data:
        context.user_data["len_attempts"] = 0
    context.user_data["len_attempts"] += 1

    try:
        length = int(update.message.text)
        if 4 <= length <= 64:
            context.user_data["length"] = length
            context.user_data["waiting_length"] = False
            context.user_data["len_attempts"] = 0
            await update.message.reply_text("Главное меню:", reply_markup = toggle_button(context.user_data))

        else: # Если вводится за пределы 4 и 64
            remaining_attempts = 5 - context.user_data["len_attempts"]
            if remaining_attempts > 0:
                await update.message.reply_text(f"❌ Длина должна быть 4-64. Осталось попыток: {remaining_attempts}\n"
                    "Попробуйте еще раз:")
            else:
                await handle_max_attempts(update, context)
    except ValueError: # Если вводится не цифра
        remaining_attempts = 5 - context.user_data["len_attempts"]
        if remaining_attempts > 0:
            await update.message.reply_text(
                f"❌ Нужно ввести число. Осталось попыток: {remaining_attempts}\n"
                "Попробуйте еще раз:"
            )
        else:
            await handle_max_attempts(update, context)

    context.user_data["waiting_length"] = False

""" Параметр максимального количества попыток ввести длинну пароля """
async def handle_max_attempts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["waiting_length"] = False
    context.user_data['length_attempts'] = 0
    await update.message.reply_text("Главное меню:", reply_markup=toggle_button(context.user_data))

""" Обработка параметров для переключения режимов """
async def query_param(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        param = query.data.split(":")[1]
        context.user_data[param] = not context.user_data.get(param, False)
        await query.edit_message_reply_markup(
            reply_markup=toggle_button(context.user_data)
        )
""" Передеача параметров из кнопки-параметеров в функцию для генерации пароля"""
async def run_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    param_length = context.user_data.get("length", False) # Параметр длины
    Specials = context.user_data.get("Специальные знаки", False) # Наличие специальных знаков
    Nums = context.user_data.get("Цифры", False) # Наличие цифр

    await query.edit_message_text(text=f"Ваш пароль: <b>{pass_gen(param_length, Nums, Specials)}</b>", parse_mode="HTML")

""" Основная функция для работы программы """
def main() -> None:
    application = Application.builder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(main_menu, pattern = "main_menu"))
    application.add_handler(CallbackQueryHandler(ask_length, pattern = "set_length"))
    application.add_handler(CallbackQueryHandler(query_param, pattern = "toggle:"))
    application.add_handler(CallbackQueryHandler(run_action, pattern = "run_action"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_length))

    application.run_polling()

if __name__ == '__main__':
    main()