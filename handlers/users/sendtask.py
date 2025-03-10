import random
from loader import db, dp, bot
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import ADMINS
from states.mystates import Grade
from aiogram.fsm.context import FSMContext
from filters.admin_bot import IsBotAdmin
import os
import time

# SEND TASK
@dp.callback_query(F.data == 'send_task')
async def send_start(call: types.CallbackQuery, state:FSMContext):
    try:
        await call.message.answer(
            "📂 Marhamat, vazifani yuboring.\n"
            "❗ Faqat ZIP formatidagi fayl jo‘natishingiz kerak!"
        )
        await state.set_state(Grade.file_gets)
    except Exception as e:
        print(e)
        await call.message.answer('🔔 Hozircha hech qanday vazifa mavjud emas! Vazifa joylashganda sizga xabar berishadi😊')


@dp.message(F.text | F.document | F.photo | F.video | F.audio, Grade.file_gets)
async def receive(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    student_id = db.select_info(student_id=user_id)
    class_id = student_id[1]
    student_name = student_id[5]
    get_id = db.select_all_classes(class_id=class_id)
    teacher_id = get_id[3]

    get_task = db.select_task(class_id=class_id)
    task_id = get_task[0]

    file_id = None

    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.text:
        file_id = message.text

    file = await bot.get_file(file_id=file_id)
    os.makedirs('tasks', exist_ok=True)
    custom_file_name = f'tasks/{time.time()}'
    await bot.download(file=file, destination=custom_file_name)
    await state.update_data({'file': custom_file_name})

    send_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Baho va feedback yuborish", callback_data=f"check_task_{user_id}")]
        ]
    )

    caption = f"🔔 Yangi vazifa keldi!\nTalabaning ismi: {student_name}"

    for admin in ADMINS:
        if message.document:
            await message.bot.send_document(admin, message.document.file_id, caption=caption, reply_markup=send_button)
        elif message.text:
            await message.bot.send_message(admin, caption + message.text, reply_markup=send_button)
        elif message.photo:
            await message.bot.send_message(admin, message.photo[-1].file_id, reply_markup=send_button)

    await message.answer(f"✅ Vazifangiz o‘qituvchiga yuborildi! Tez orada natijangizni olasiz 😊.")
    db.add_submission(
        id = random.randint(1000,100000),
        student_id=user_id,
        student_name=student_id[5],
        task_id=task_id,
        class_id=class_id,
        teacher_id=teacher_id,
        file_url=file_id
    )
    await state.clear()


