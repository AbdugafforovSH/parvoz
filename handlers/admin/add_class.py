import random
from aiogram.filters import  Command
from aiogram.types import CallbackQuery

from data.config import ADMINS
from loader import db, dp
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.mystates import AddClass

@dp.callback_query(F.data == 'create')
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMINS:
        await call.answer("❌ Kechirasiz, bu buyruq siz uchun emas!", show_alert=True)
        return

    await call.message.answer(text='➕ Guruh uchun nom yarating:')
    await state.set_state(AddClass.start)

@dp.message(F.text, AddClass.start)
async def teacher(message:types.Message, state:FSMContext):
    await state.update_data({
        'name': message.text
    })
    await message.answer("O'qituvchi ismini yozing:")
    await state.set_state(AddClass.tname)

@dp.message(F.text, AddClass.tname)
async def final(message: types.Message, state:FSMContext):
    await state.update_data({
        'tname': message.text
    })
    data = await state.get_data()

    db.add_class(
        id=random.randint(1,1000000),
        class_id=random.randint(1,100000),
        class_name=data.get('name'),
        teacher_id=message.from_user.id,
        teacher_name=data.get('tname')
    )

    await message.answer(f"Ma'lumotlaringiz saqlandi. \nTekshirish uchun:\n\nGuruh nomi: {data.get('name')}\nGuruh o'qituvchisi: {data.get('tname')}")
    await state.clear()