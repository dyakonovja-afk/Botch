from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from config import FREE_RETURNS, FREE_FILTERS
from db import ensure_user, get_user, inc_return, inc_filter, save_dialog
from keyboards import chat_kb, end_kb, filters_kb
from matcher import add_to_queue, try_match, end_chat, active_chats

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    ensure_user(message.from_user.id)
    add_to_queue(message.from_user.id)
    a, b = try_match()
    if a and b:
        await message.bot.send_message(a, "💬 Собеседник найден", reply_markup=chat_kb())
        await message.bot.send_message(b, "💬 Собеседник найден", reply_markup=chat_kb())
    else:
        await message.answer("🔎 Ищем собеседника...")

@router.message()
async def relay(message: Message):
    partner = active_chats.get(message.from_user.id)
    if partner:
        await message.bot.send_message(partner, message.text)

@router.callback_query(F.data == "end")
async def end_dialog(cb: CallbackQuery):
    partner = end_chat(cb.from_user.id)
    save_dialog(cb.from_user.id, partner)
    user = get_user(cb.from_user.id)
    can_return = user[1] < FREE_RETURNS
    await cb.message.answer("Диалог завершён", reply_markup=end_kb(can_return))
    if partner:
        await cb.bot.send_message(partner, "Диалог завершён", reply_markup=end_kb(True))

@router.callback_query(F.data == "return")
async def return_dialog(cb: CallbackQuery):
    user = get_user(cb.from_user.id)
    if user[1] >= FREE_RETURNS:
        await cb.message.answer("🔒 Бесплатные возвраты закончились")
        return
    inc_return(cb.from_user.id)
    await cb.message.answer("🔁 Возврат диалога пока в разработке")

@router.callback_query(F.data == "f_apply")
async def apply_filters(cb: CallbackQuery):
    user = get_user(cb.from_user.id)
    if user[2] >= FREE_FILTERS:
        await cb.message.answer("🔒 Бесплатные фильтры закончились")
        return
    inc_filter(cb.from_user.id)
    await cb.message.answer("🎯 Фильтры применены")
