from aiogram import  Bot, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.enums import ContentType
from data.config import ADMINS
from states.mystates import Broadcast
from loader import db,dp




@dp.callback_query(F.data == "sendmessage", F.from_user.id.in_(ADMINS))
async def choose_message_type(call: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Oddiy xabar", callback_data="text")],
        [InlineKeyboardButton(text="🖼️ Rasmli xabar", callback_data="photo")],
        [InlineKeyboardButton(text="🎥 Video xabar", callback_data="video")],
        [InlineKeyboardButton(text="🎙 Ovozli xabar", callback_data="voice")]
    ])
    await call.message.answer("👇 Xabar turini tanlang:", reply_markup=keyboard)

# Matnli xabar yuborish
@dp.callback_query(F.data == "text", F.from_user.id.in_(ADMINS))
async def ask_for_text(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🗂️ Barchaga yubormoqchi bo'lgan xabaringizni kiriting:")
    await state.set_state(Broadcast.text)

@dp.message(Broadcast.text, F.content_type == ContentType.TEXT)
async def send_text(message: Message, state: FSMContext, bot: Bot):
    all_users = db.select_all_users()
    for user in all_users:
        try:
            await bot.send_message(chat_id=user[2], text=message.text)
        except Exception as e:
            print(f"Foydalanuvchiga xabar yuborib bo‘lmadi: {user[2]}, Xato: {e}")
    await state.clear()

# Rasm, video va ovozli xabarlarni yuborish
async def send_media(message: Message, state: FSMContext, bot: Bot, media_type: str):
    all_users = db.select_all_users()
    for user in all_users:
        try:
            if media_type == "photo":
                await bot.send_photo(chat_id=user[2], photo=message.photo[-1].file_id, caption=message.caption or "")
            elif media_type == "video":
                await bot.send_video(chat_id=user[2], video=message.video.file_id, caption=message.caption or "")
            elif media_type == "voice":
                await bot.send_voice(chat_id=user[2], voice=message.voice.file_id)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
    await state.clear()

@dp.callback_query(F.data == "photo", F.from_user.id.in_(ADMINS))
async def ask_for_photo(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Rasmni yuboring:")
    await state.set_state(Broadcast.photo)

@dp.message(Broadcast.photo, F.content_type == ContentType.PHOTO)
async def send_photo(message: Message, state: FSMContext, bot: Bot):
    await send_media(message, state, bot, "photo")

@dp.callback_query(F.data == "video", F.from_user.id.in_(ADMINS))
async def ask_for_video(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Videoni yuboring:")
    await state.set_state(Broadcast.video)

@dp.message(Broadcast.video, F.content_type == ContentType.VIDEO)
async def send_video(message: Message, state: FSMContext, bot: Bot):
    await send_media(message, state, bot, "video")

@dp.callback_query(F.data == "voice", F.from_user.id.in_(ADMINS))
async def ask_for_voice(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ovozli xabarni yuboring:")
    await state.set_state(Broadcast.voice)

@dp.message(Broadcast.voice, F.content_type == ContentType.VOICE)
async def send_voice(message: Message, state: FSMContext, bot: Bot):
    await send_media(message, state, bot, "voice")
