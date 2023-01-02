from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_KEYBOARD = InlineKeyboardMarkup()
START_KEYBOARD.add(InlineKeyboardButton("Создать ссылку", callback_data='create_link'))

CANCEL_KEYBOARD = InlineKeyboardMarkup()
CANCEL_KEYBOARD.add(InlineKeyboardButton("Отмена", callback_data='cancel'))


def get_links_keyboard(links: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for link in links:
        keyboard.add(InlineKeyboardButton(link['redirect'], callback_data=f"LINK_{link['id']}"))
    return keyboard
