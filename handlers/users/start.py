import random
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from data.config import ADMINS
from states.mystates import Register, Gname
from loader import dp, db
from aiogram import types, F
from keyboards.default.buttons import role_button
from keyboards.inline.buttons import start_button, starts_button
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


@dp.message(CommandStart())
async def start_bot(message:types.Message, state:FSMContext):
    register = db.select_user(telegram_id=message.from_user.id)
    if register:
        if message.from_user.id in ADMINS:
            await message.answer("🖥️ Asosiy menyudasiz! \n👇Quyidagi menyular orqali guruhingizni nazorat qilishingiz mumkin!",reply_markup=starts_button)
        else:
            await message.answer(
                "🖥️ Asosiy menyudasiz! \n👇Quyidagi menyular orqali guruhingizni tekshirishingzi , vazifalaringizni bilib olishingiz mumkin!",
                reply_markup=start_button)
    else:
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}, botimizga xush kelibsiz!\n\nBotdan foydalanish uchun ro'yxatdan o'tish zarur! ")
        await message.answer(f"✍️ Ism Familiyangizni kiriting:")
        await state.set_state(Register.get_name)

@dp.message(F.text, Register.get_name)
async def role(message:types.Message, state:FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(f"🧑‍💻 O'quv markazidagi vazifangiz qanday: ", reply_markup=role_button)
    await state.set_state(Register.end)

@dp.message(F.text, Register.end)
async def final(message:types.Message, state:FSMContext):
    await state.update_data({'role': message.text})
    data = await state.get_data()
    db.add_user(
    id= random.randint(1,1000000),
    fullname=data.get('name'),
    role = data.get('role'),
    telegram_id=message.from_user.id
    )
    if message.from_user.id in ADMINS:
        await message.answer("Ma'lumotlaringiz saqlandi. Endi botdan foydalanishngiz mumkin!",reply_markup=starts_button)
    else:
        await message.answer("Ma'lumotlaringiz saqlandi. Endi botdan foydalanishngiz mumkin!",reply_markup=start_button)
    await state.clear()



@dp.callback_query(F.data == 'join_cls')
async def test(call: types.CallbackQuery, state:FSMContext):
    user_id = call.from_user.id
    check_group = db.select_info(student_id=user_id)

    get_mycls = db.get_group_name()
    get_cls = db.select_all_class()

    groups_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{cls[2]}', callback_data=f'gname_{cls[1]}')] for cls in get_cls
    ])

    myclass = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{mg[2]}", callback_data=f"myg_{mg[0]}")] for mg in get_mycls
    ])

    if check_group is None:
        await call.message.answer('Siz hali hech qaysi guruhga qo\'shilmagansiz. Qaysi guruhda o\'qiysiz?', reply_markup=groups_button)
        await state.set_state(Gname.start)
    else:
        await call.message.answer('🗂️ Sizning Guruhingiz\n👇Kirish uchun ustiga bosing', reply_markup=myclass)


@dp.callback_query(lambda query: query.data.startswith('gname_'), Gname.start)
async def save(call: types.CallbackQuery, state:FSMContext):
    cls_id = int(call.data.split('_')[1])
    await state.update_data({'cls_id': cls_id})

    get_name = db.select_all_classes(class_id=cls_id)
    group_name = get_name[2]
    group_id = get_name[1]
    get_sname = db.get_fullname(telegram_id=call.from_user.id)
    student_name = get_sname[1]
    teacher_name = get_name[4]
    data = await state.get_data()
    db.add_student(
        id=random.randint(1, 100000),
        group_name=group_name,
        student_id=call.from_user.id,
        group_id=group_id,
        student_name=student_name,
        teacher_name=teacher_name)

    await call.message.answer(f'{group_name} ga muvaffaqiyatli qo\'shildingiz. Menyuni yangilab guruhingizni kuzatishingiz mumkin.')
