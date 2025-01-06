import os

import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from DB import get_products_by_category, get_categories, get_product_by_id, get_category_by_id


# Токен вашего бота
TOKEN = "7828137116:AAEZTwnMFHQ5IAKIUIQfNfb3yKnFdzM55-U"

#TOKEN = "6542894948:AAHN59mcL79G0qS_lqVmgJeWsgAdWfe6wAo"#TEST

application = Application.builder().token(TOKEN).build()

# Путь к папке с изображениями
IMAGE_DIR = "images/"

# Магазин открыт/закрыт
shop_status = {"is_open": True}

# Список заблокированных пользователей
blocked_users = set()

# Защита от спама
order_timestamps = {}

admin_ids = [1170089312,5273933548]  # Список ID администраторов
# Функция для проверки, является ли пользователь администратором

def is_admin(user_id):
    # Здесь можно настроить проверку на основе списка администраторов
    return user_id in admin_ids

async def send_order_to_admins(user, product,context: ContextTypes.DEFAULT_TYPE):
    for admin_id in admin_ids:
        try:
            await application.bot.send_message(
                admin_id,
                f"Пользователь {user['first_name']} ({user['id']}) сделал заказ на продукт:\n"
                f"Название: {product['name']}\n"
                f"Ссылка на профиль: [Ссылка](https://t.me/{user['username']})"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение админу {admin_id}: {e}")


async def order_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    print(update)
    await query.answer()

    # Извлечение ID товара из callback_data
    product_id = query.data.split("_")[1]
    product = get_product_by_id(product_id)

    # Получаем информацию о пользователе
    user ={
        "id" : query.from_user.id,
        "username" : query.from_user.username,
        "first_name": query.from_user.first_name
    }
    product_name = product['name']

    # Отправка уведомлений администраторам
    await send_order_to_admins(user, product, context)

    # Отправка пользователю сообщения о заказе
    await query.message.reply_text(
        f"Ваш заказ на товар '{product_name}' успешно оформлен! "
        f"В ближайшее время с вами свяжется продавец."
    )


# Команда для бана пользователя
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in admin_ids:
        await update.message.reply_text("У вас нет прав для использования этой команды.")
        return

    # Извлекаем ID пользователя для бана
    if len(context.args) < 1:
        await update.message.reply_text("Пожалуйста, укажите ID пользователя для бана.")
        return

    try:
        banned_user_id = int(context.args[0])
        blocked_users.add(banned_user_id)
        await update.message.reply_text(f"Пользователь с ID {banned_user_id} был заблокирован.")
    except ValueError:
        await update.message.reply_text("Ошибка: Укажите правильный ID пользователя.")


# Функция для разбана пользователя
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in admin_ids:
        await update.message.reply_text("У вас нет прав для использования этой команды.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Пожалуйста, укажите ID пользователя для разбана.")
        return

    try:
        unbanned_user_id = int(context.args[0])
        blocked_users.discard(unbanned_user_id)
        await update.message.reply_text(f"Пользователь с ID {unbanned_user_id} был разблокирован.")
    except ValueError:
        await update.message.reply_text("Ошибка: Укажите правильный ID пользователя.")


# Главное меню
def get_main_menu():
    categories = get_categories()

    # Статус магазина
    status = "🟢 Магазин открыт" if shop_status["is_open"] else "🔴 Магазин закрыт"

    # Создание клавиатуры
    keyboard = [
        [InlineKeyboardButton(category['name'], callback_data=f"category_{category['id']}")]
        for category in categories
    ]

    return InlineKeyboardMarkup(keyboard), (
        f"Добро пожаловать в магазин Chips&Beaches.\n"
        f"Здесь вы можете выбрать категорию товаров.\n\n{status}"
    )

# Меню категории
def get_category_menu(category_id):
    items = get_products_by_category(category_id)
    print(items)
    keyboard = [
        [InlineKeyboardButton(
            f"{item['name']} {'✅' if item['in_stock'] else '❌'}",
            callback_data=f"product_{item['id']}"
        )]
        for item in items
    ]
    keyboard.append([InlineKeyboardButton("Назад", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard, message = get_main_menu()
    await update.message.reply_text(message, reply_markup=keyboard)

# Обработчик выбора категории
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category_id = query.data.split("_")[1]
    # Получаем категорию, предполагаем, что get_categor_by_id воyзвращает список с одним элементом
    name = get_category_by_id(category_id)

    await query.edit_message_text(
        text=f"Вы выбрали категорию: {name['name']}\n\nВыберите товар:",
        reply_markup=get_category_menu(category_id)
    )


# Обработчик выбора товара
async def product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлечение ID товара
    product_id = query.data.split("_")[1]
    product = get_product_by_id(product_id)
    image = product['image']
    #image_path = os.path.join(IMAGE_DIR, product['image'])

    # Формирование описания
    product_description = (
            f"{product['name']}\n"
            + product['description'].replace('\\n', '\n')
            + f"\n\n{'✅ В наличии' if product['in_stock'] else '❌ Нет в наличии'}"
    )

    # Отправка изображения с описанием
    try:
        #with open(image_path, "rb") as photo:
            await query.edit_message_media(
                media=InputMediaPhoto(
                    #media=photo,
                    media=image,
                    caption=product_description,  # Указываем caption здесь
                ),
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Заказать", callback_data=f"order_{product_id}"),
                    InlineKeyboardButton("Назад", callback_data="back")
                ]])
            )
    except FileNotFoundError:
        await query.message.reply_text("Файл изображения не найден.")
    except Exception as e:
        await query.message.reply_text(f"Произошла ошибка: {e}")


# Обработчик кнопки "Назад"
async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем главное меню и сообщение
    keyboard, message = get_main_menu()

    # Проверяем, если предыдущее сообщение было с изображением
    if query.message.photo:
        # Удаляем предыдущее сообщение с изображением
        await query.message.delete()
        # Отправляем новое сообщение с главным меню
        await query.message.reply_text(message, reply_markup=keyboard)
    else:
        # Если предыдущее сообщение не с изображением, просто редактируем его
        await query.edit_message_text(text=message, reply_markup=keyboard)

# Команда для изменения доступности товара
'''
async def toggle_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Использование: /toggle_stock <id> <on|off>")
        return

    product_id, status = args
    if product_id not in products:
        await update.message.reply_text("Товар с таким ID не найден.")
        return

    products[product_id]["in_stock"] = (status == "on")
    await update.message.reply_text(f"Доступность товара '{products[product_id]['name']}' обновлена.")
'''

# Команда для открытия/закрытия магазина
async def toggle_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Использование: /toggle_shop <open|close>")
        return

    status = args[0]
    if status == "open":
        shop_status["is_open"] = True
        await update.message.reply_text("Магазин открыт 🟢.")
    elif status == "close":
        shop_status["is_open"] = False
        await update.message.reply_text("Магазин закрыт 🔴.")
    else:
        await update.message.reply_text("Неверный параметр. Используйте 'open' или 'close'.")



async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.full_name
    username = update.message.from_user.username

    if username:
        user_link = f"https://t.me/{username}"  # Ссылка на профиль пользователя
        await update.message.reply_text(f"Ваше имя: {user_name}\nВаш ID: {user_id}\nСсылка на ваш профиль: {user_link}")
    else:
        await update.message.reply_text(f"Ваше имя: {user_name}\nВаш ID: {user_id}\nУ вас нет установленного имени пользователя в Telegram.")


# Команда для отправки сообщения пользователю по ID
async def send_message_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что пользователь — админ
    user_id = update.message.from_user.id
    if user_id not in admin_ids:
        await update.message.reply_text("У вас нет прав для использования этой команды.")
        return

    # Проверяем, что команда содержит аргументы
    if len(context.args) < 2:
        await update.message.reply_text("Использование: /send_message <user_id> <сообщение>")
        return

    try:
        # Извлекаем ID пользователя и сообщение
        target_user_id = int(context.args[0])
        message = " ".join(context.args[1:])

        # Отправляем сообщение
        await application.bot.send_message(chat_id=target_user_id, text=message)
        await update.message.reply_text(f"Сообщение успешно отправлено пользователю с ID {target_user_id}.")
    except ValueError:
        await update.message.reply_text("Ошибка: укажите правильный ID пользователя.")
    except telegram.error.BadRequest as e:
        await update.message.reply_text(f"Ошибка: {e}")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")


# Главная функция
def main():

    # Хендлеры
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(category_handler, pattern="^category_"))
    application.add_handler(CallbackQueryHandler(product_handler, pattern="^product_"))
    application.add_handler(CallbackQueryHandler(back_handler, pattern="^back$"))
    application.add_handler(CommandHandler("userinfo", user_info))
    application.add_handler(CommandHandler("toggle_shop", toggle_shop))
    application.add_handler(CommandHandler("send_message", send_message_to_user))

    application.add_handler(CallbackQueryHandler(order_handler, pattern="^order_"))

    # Хендлеры для бана
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("unban", unban_user))

    application.run_polling()

if __name__ == "__main__":
    main()
