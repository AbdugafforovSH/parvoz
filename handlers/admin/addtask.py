import random
from aiogram.filters import  Command
from aiogram.types import CallbackQuery
from data.config import ADMINS
from loader import db, dp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.mystates import AddTask
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

@dp.callback_query(F.data == 'add_task')
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMINS:
        await call.answer("❌ Kechirasiz, bu buyruq siz uchun emas!", show_alert=True)
        return
    classes = db.select_all_class()

    if not classes:
        await call.message.answer("Hech qanday guruh topilmadi!")
        return

    group_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{clas[2]}", callback_data=f"group_{clas[1]}")]
            for clas in classes if len(clas) > 2
        ]
    )

    await call.message.answer(text=f'Qaysi guruhga vazifa qo\'shmoqchisiz?', reply_markup=group_buttons)
    await state.set_state(AddTask.start)

@dp.callback_query(lambda query: query.data.startswith('group_'))
async def get_class(call: types.CallbackQuery,state:FSMContext):
    class_id = call.data.split('_')[1]
    await state.update_data({'class_id':class_id})
    await call.message.answer(text='➕ Marhamat, vazifa uchun nom kiriting:')
    await state.set_state(AddTask.start)

@dp.message(F.text, AddTask.start)
async def get_name(message:types.Message, state:FSMContext):
    await state.update_data({'task_name': message.text})
    await message.answer('✅ Qabul qilindi, endi vazifa haqida ma\'lumot kiriting:')
    await state.set_state(AddTask.final)

from datetime import timedelta, datetime
utc_5_plus = datetime.utcnow() + timedelta(hours=5)

@dp.message(F.text, AddTask.final)
async def get_description(message:types.Message, state:FSMContext):
    await state.update_data({'description':message.text})
    data = await state.get_data()
    db.add_tasks(
        id = random.randint(1,100000),
        task_title = data['task_name'],
        task_description= data['description'],
        created_at=utc_5_plus,
        class_id=data['class_id']
    )
    await message.answer(text='🗂️ Vazifa muvaffaqiyatli joylandi')