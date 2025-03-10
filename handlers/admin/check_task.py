import random
from loader import db, dp, bot
from aiogram import types, F
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.mystates import Checkin

@dp.callback_query(F.data == 'checkin')
async def start(call: types.CallbackQuery):
    teacher_id = call.from_user.id
    classes = db.execute("SELECT class_id, class_name FROM Classes WHERE teacher_id = ?",
                         (teacher_id,), fetchall=True)

    if not classes:
        await call.message.answer("📌 Sizga tegishli guruhlar topilmadi.")
        return

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=class_name, callback_data=f'check_class_{class_id}')]
        for class_id, class_name in classes
    ])

    await call.message.answer("📌 Qaysi guruhdagi o‘quvchilarning vazifasini tekshirasiz?", reply_markup=markup)


@dp.callback_query(lambda c: c.data.startswith("check_class_"))
async def check_tasks(call: types.CallbackQuery, state: FSMContext):
    class_id = int(call.data.split("_")[2])

    students = db.execute("SELECT student_id, student_name FROM Student WHERE group_id = ?", (class_id,), fetchall=True)

    if not students:
        await call.message.answer("📌 Bu guruhda talaba yo‘q.")
        return

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=student_name, callback_data=f'check_task_{student_id}')]
        for student_id, student_name in students
    ])

    await call.message.answer("📌 Qaysi o‘quvchining vazifasini ko‘rishni xohlaysiz?", reply_markup=markup)


@dp.callback_query(lambda c: c.data.startswith("check_task_"))
async def evaluate_task(call: types.CallbackQuery, state: FSMContext):
    student_id = int(call.data.split("_")[2])
    task_data = db.execute("SELECT file_url FROM Submission WHERE student_id = ?", (student_id,), fetchone=True)

    if not task_data:
        await call.message.answer("📌 Ushbu o‘quvchi hali vazifa yubormagan.")
        return

    file_id = task_data[0]  # Foydalanuvchi yuborgan fayl ID

    # Hamma holatlarni tekshirib chiqamiz
    try:
        await call.message.answer_document(file_id,
                                           caption="📂 O‘quvchining vazifasi")  # Avval hujjat sifatida jo‘natamiz
    except:
        try:
            await call.message.answer_photo(file_id,
                                            caption="📂 O‘quvchining vazifasi")  # Agar hujjat bo‘lmasa, rasm sifatida jo‘natamiz
        except:
            await call.message.answer(
                f"📂 O‘quvchining vazifasi: {file_id}")  # Agar na rasm, na hujjat bo‘lsa, oddiy matn sifatida jo‘natamiz

    await call.message.answer("📌 O‘quvchining ishini ko'rib bo'lgandan so'ng baho bering (0-10):")
    await state.update_data(student_id=student_id)
    await state.set_state(Checkin.get_grade)


@dp.message(Checkin.get_grade)
async def get_grade(message: types.Message, state: FSMContext):
    try:
        grade = int(message.text)
        if 0 <= grade <= 10:
            await message.answer("📌 Izoh yozing (ixtiyoriy):")
            await state.update_data(grade=grade)
            await state.set_state(Checkin.get_feedback)
        else:
            await message.answer("❌ Baho 0 dan 10 gacha bo‘lishi kerak!")
    except ValueError:
        await message.answer("❌ Iltimos, faqat son kiriting!")


@dp.message(Checkin.get_feedback)
async def get_feedback(message: types.Message, state: FSMContext):
    data = await state.get_data()
    student_id = data['student_id']
    get_student = db.select_info(student_id=student_id)
    student_name = get_student[5]
    grade = data['grade']
    feedback = message.text

    db.execute(
        "INSERT INTO Taskcheck (id, teacher_id, teacher_name, student_id, student_name, checked, feedback, grade, status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (random.randint(1000, 99999), message.from_user.id, message.from_user.full_name,
         student_id, student_name, "Tekshirildi", feedback, grade, "Yakunlandi"),
        commit=True
    )

    await message.answer("✅ O‘quvchining vazifasi baholandi!")

    await bot.send_message(
        student_id,
        f"✅ Vazifangiz tekshirildi!\n📊 Baho: {grade}/10\n💬 Izoh: {feedback}"
    )

    await state.clear()
