from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def chat_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Завершить диалог", callback_data="end")]
    ])

def end_kb(can_return: bool):
    rows = []
    if can_return:
        rows.append([InlineKeyboardButton(text="🔁 Вернуть диалог", callback_data="return")])
    rows.append([
        InlineKeyboardButton(text="🚩 Пожаловаться", callback_data="report"),
        InlineKeyboardButton(text="➡️ Новый диалог", callback_data="new")
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def filters_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пол: М", callback_data="f_m"),
         InlineKeyboardButton(text="Пол: Ж", callback_data="f_f"),
         InlineKeyboardButton(text="Пол: Любой", callback_data="f_any")],
        [InlineKeyboardButton(text="Применить фильтры", callback_data="f_apply")]
    ])
