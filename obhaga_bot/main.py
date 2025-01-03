import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import requests

from api import get_product_details, get_categories, get_products

# Включаем логирование для отслеживания ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение категорий

# Получение товаров для выбранной категории


# Обработка команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Выберите категорию:', reply_markup=category_keyboard())

# Создание клавиатуры с категориями
def category_keyboard():
    categories = get_categories()
    keyboard = [[InlineKeyboardButton(category['name'], callback_data=f'category_{category["id"]}') for category in categories]]
    return InlineKeyboardMarkup(keyboard)

# Обработка выбора категории
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Получение ID выбранной категории
    category_id = int(query.data.split('_')[1])

    # Получение товаров для выбранной категории
    products = get_products(category_id)

    if products:
        keyboard = [[InlineKeyboardButton(product['name'], callback_data=f'product_{product["id"]}') for product in products]]
        keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_categories')])

        await query.edit_message_text(text="Выберите товар:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_text(text="Нет товаров в этой категории.")

# Обработка выбора товара
async def product_details(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Получение ID выбранного товара
    product_id = int(query.data.split('_')[1])

    # Получение подробной информации о товаре
    product = get_product_details(product_id)

    if product:
        text = f"Товар: {product['name']}\nОписание: {product['description']}\nНаличие: {'В наличии' if product['in_stock'] else 'Нет в наличии'}"
        await query.edit_message_text(text=text)

        # Кнопка назад для возврата в категории
        keyboard = [[InlineKeyboardButton("Назад", callback_data='back_to_categories')]]
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard))


# Обработка кнопки "Назад" для возврата в категории
async def back_to_categories(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Выберите категорию:", reply_markup=category_keyboard())

# Основная функция для запуска бота
def main():
    # Получаем токен из вашего бота
    application = Application.builder().token("7828137116:AAEZTwnMFHQ5IAKIUIQfNfb3yKnFdzM55-U").build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчики кнопок
    application.add_handler(CallbackQueryHandler(button, pattern='^category_'))
    application.add_handler(CallbackQueryHandler(product_details, pattern='^product_'))
    application.add_handler(CallbackQueryHandler(back_to_categories, pattern='^back_to_categories'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
