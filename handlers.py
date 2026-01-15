from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from db import (
    ensure_user,
    get_user,
    inc_return,
    inc_filter,
    save_dialog,
)
from matcher import (
    add_to_queue,
    try_match,
    end_chat,
    active_chats,
)
from keyboards import chat_kb, end_kb
from config import FREE_RETURNS, FREE_FILTERS

router = Router()


# =========================
# /start — ВСЕГДА ОТВЕЧАЕТ
# =========================
@router.message(F.text == "/start")
async def start(message: Message):
    user_id = message.from_user.id
    ensure_user(user_id)

    add_to_queue(user_id)
    a, b = try_match()

    # Мгновенный отклик — никогда не молчим
    await message.answer(
        "👋 Вы в анонимном чате.\n"
        "💬 Подбираем собеседника…\n"
        "⏳ Пожалуйста, подождите."
    )

    # Если пара нашлась — соединяем
    if a and b:
        await message.bot.send_message(
            a,
            "💬 Собеседник найден!\nМожете начинать общение.",
            reply_markup=chat_kb()
        )
        await message.bot.send_message(
            b,
            "💬 Собеседник найден!\nМожете начинать общение.",
            reply_markup=chat_kb()
        )


# =========================
# ПЕРЕСЫЛКА СООБЩЕНИЙ
# =========================
@router.message()
async def relay(message: Message):
    user_id = message.from_user.id
    partner_id = active_chats.get(user_id)

    if not partner_id:
        await message.answer(
            "❗ Сейчас у вас нет активного диалога.\n"
            "Нажмите /start, чтобы найти собеседника."
        )
        return

    await message.bot.send_message(partner_id, message.text)


# =========================
# ЗАВЕРШЕНИЕ ДИАЛОГА
# =========================
@router.callback_query(F.data == "end")
async def end_dialog(cb: CallbackQuery):
    user_id = cb.from_user.id
    partner_id = end_chat(user_id)

    # сохраняем диалог
    if partner_id:
        save_dialog(user_id, partner_id)

    user = get_user(user_id)
    can_return = user[1] < FREE_RETURNS

    await cb.message.answer(
        "💬 Диалог завершён.",
        reply_markup=end_kb(can_return)
    )

    if partner_id:
        await cb.bot.send_message(
            partner_id,
            "💬 Собеседник завершил диалог.",
            reply_markup=end_kb(True)
        )


# =========================
# ВОЗВРАТ ДИАЛОГА
# =========================
@router.callback_query(F.data == "return")
async def return_dialog(cb: CallbackQuery):
    user_id = cb.from_user.id
    user = get_user(user_id)

    if user[1] >= FREE_RETURNS:
        await cb.message.answer(
            "🔒 Бесплатные возвраты закончились.\n"
            "Оформите подписку, чтобы вернуть диалог."
        )
        return

    inc_return(user_id)

    await cb.message.answer(
        "🔁 Возврат диалога будет доступен в следующем обновлении.\n"
        "Спасибо за терпение 🙌"
    )


# =========================
# НОВЫЙ ДИАЛОГ
# =========================
@router.callback_query(F.data == "new")
async def new_dialog(cb: CallbackQuery):
    user_id = cb.from_user.id

    add_to_queue(user_id)
    a, b = try_match()

    await cb.message.answer(
        "🔎 Ищем нового собеседника…"
    )

    if a and b:
        await cb.bot.send_message(
            a,
            "💬 Новый собеседник найден!",
            reply_markup=chat_kb()
        )
        await cb.bot.send_message(
            b,
            "💬 Новый собеседник найден!",
            reply_markup=chat_kb()
        )


# =========================
# ЖАЛОБА
# =========================
@router.callback_query(F.data == "report")
async def report(cb: CallbackQuery):
    await cb.message.answer(
        "🚩 Жалоба принята.\n"
        "Спасибо, вы помогаете делать чат безопаснее."
        )
