from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def reply_keyboard(size, buttons_list, once=False):
    keyboard = ReplyKeyboardMarkup(row_width=size, resize_keyboard=True, one_time_keyboard=once)
    for button in buttons_list:
        keyboard.insert(KeyboardButton(button))
    return keyboard


def inline_keyboard(size, texts, callbacks):
    keyboard = InlineKeyboardMarkup(row_width=size)
    for callback, text in zip(callbacks, texts):
        keyboard.insert(InlineKeyboardButton(text, callback_data=callback))
    return keyboard


def url_inline(size, texts, data, url):
    keyboard = InlineKeyboardMarkup(row_width=size)
    for text, callback in zip(texts, data):
        if callback == 'url':
            keyboard.insert(InlineKeyboardButton(text, url=url))
        else:
            keyboard.insert(InlineKeyboardButton(text, callback_data=callback))
    return keyboard


