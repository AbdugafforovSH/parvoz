import random
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import  db,dp, bot
from aiogram import types
from aiogram.filters import Command
from datetime import timedelta, datetime
from keyboards.default.buttons import attendance
utc_5_plus = datetime.utcnow() + timedelta(hours=5)




@dp.callback_query(lambda c: c.data == 'attend')
async def start_attendance(call: types.CallbackQuery):
    teacher_id = call.from_user.id
    classes = db.execute("SELECT class_id, class_name FROM Classes WHERE teacher_id = ?",
                         (teacher_id,), fetchall=True)

    if not classes:
        await call.message.answer("📌 Sizga tegishli guruhlar topilmadi.")
        return


    check_attend = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='📋 Tekshirish', callback_data='check_attend')]])

    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f'{class_name}', callback_data=f'att_class_{class_id}')]
                                                   for  class_id,class_name in classes if len(class_name) > 1
                                                   ])


    await call.message.answer("📋 Davomatni tekshirish uchun pastdagi tekshirish menyusini bosing:", reply_markup=check_attend)
    await call.message.answer("📌 Qaysi guruh uchun davomat boshlaysiz?\nBir kunda bir marta davomat qilish tavsiya etiladi!", reply_markup=markup)

@dp.callback_query(lambda c: c.data.startswith("att_class_"))
async def mark_attendance(call: types.CallbackQuery):
    class_id = int(call.data.split("_")[2])

    students = db.execute("SELECT student_id, student_name FROM Student WHERE group_id = ?",
                          (class_id,), fetchall=True)

    if not students:
        await call.message.answer("📌 Bu guruhda talaba yo‘q.")
        return

    for student_id, student_name in students:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Kelgan", callback_data=f"att_yes_{class_id}_{student_id}")],
            [InlineKeyboardButton(text="❌ Kelmadi", callback_data=f"att_no_{class_id}_{student_id}")]
        ])

        await call.message.answer(f"👤 {student_name}", reply_markup=markup)


@dp.callback_query(lambda c: c.data.startswith("att_yes_") or c.data.startswith("att_no_"))
async def save_attendance(call: types.CallbackQuery):
    data = call.data.split("_")
    status = "present" if data[1] == "yes" else "absent"
    class_id, student_id = int(data[2]), int(data[3])
    time_now = utc_5_plus
    id = random.randint(1,100000)
    student_name = db.execute("SELECT student_name FROM Student WHERE student_id = ?",
                              (student_id,), fetchone=True)

    if student_name:
        db.execute("""
            INSERT INTO Attendance (id,class_id, student_id, student_name, status, created_at) 
            VALUES (?,?, ?, ?, ?,?)
        """, (id,class_id, student_id, student_name[0], status, time_now), commit=True)

        await call.message.edit_text(f"👤 {student_name[0]} - {'✅ Kelgan' if status == 'present' else '❌ Kelmadi'}")


@dp.callback_query(F.data == 'check_attend')
async def check_attendance(call: types.CallbackQuery):
    teacher_id = call.from_user.id
    classes = db.execute("SELECT class_id, class_name FROM Classes WHERE teacher_id = ?",
                         (teacher_id,), fetchall=True)

    if not classes:
        await call.message.answer("📌 Sizga tegishli guruhlar topilmadi.")
        return

    text = "📌 Davomat natijalari:\n"
    for class_id, class_name in classes:
        present_count = db.execute("""
            SELECT COUNT(*) FROM Attendance 
            WHERE class_id = ? AND status = 'present' 
            AND created_at >= DATETIME('now', '-1 day')
        """, (class_id,), fetchone=True)[0]

        absent_count = db.execute("""
            SELECT COUNT(*) FROM Attendance 
            WHERE class_id = ? AND status = 'absent' 
            AND created_at >= DATETIME('now', '-1 day')
        """, (class_id,), fetchone=True)[0]

        text += f"\n📝 {class_name}: ✅ {present_count} ta kelgan, ❌ {absent_count} ta kelmagan"

    await call.message.answer(text)
