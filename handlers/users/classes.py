from aiogram.types import CallbackQuery
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.buttons import cls_menu
from loader import db,dp


@dp.callback_query(F.data == 'groups')
async def all_categories(call: CallbackQuery):
    classes = db.select_all_class()

    if not classes:
        await call.message.answer("Hech qanday guruh topilmadi!")
        return

    group_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{get_class_status(clas[1])} {clas[2]}", callback_data=f"cls_{clas[1]}")]
            for clas in classes if len(clas) > 2
        ]
    )

    await call.message.answer(
        text=("Guruhlar statistikasi:\n"
              "❌ - Bu guruhda hali o'quvchi mavjud emas"
              "🔴 - Hali hech bir talaba vazifa topshirmagan\n"
              "🟡 - Ayrim talabalar vazifa topshirgan\n"
              "🟢 - Guruhda barcha talabalar vazifa topshirishgan\n"
              "Vazifalarni o'z vaqtida topshirishni unutmang😊"),
        reply_markup=group_buttons
    )


def get_class_status(class_id: int):
    sql_total_students = "SELECT COUNT(*) FROM Student WHERE group_id = ?"
    sql_submitted_tasks = "SELECT COUNT(DISTINCT student_id) FROM Submission WHERE class_id = ? AND status = 'submitted'"

    total_students = db.execute(sql_total_students, parameters=(class_id,), fetchone=True)
    submitted_students = db.execute(sql_submitted_tasks, parameters=(class_id,), fetchone=True)

    total_students = total_students[0] if total_students else 0
    submitted_students = submitted_students[0] if submitted_students else 0

    if total_students == 0:
        return "❌"  
    elif submitted_students == 0:
        return "🔴"
    elif submitted_students == total_students:
        return "🟢"
    else:
        return "🟡"



# RATING ACCESS

@dp.callback_query(lambda query: query.data.startswith('cls_'))
async def start(call: types.CallbackQuery):
    cls_id = call.data.split('_',1)[1]
    exta_cls_id = db.select_all_classes(class_id=cls_id)
    cls_name = exta_cls_id[2]
    cls_tname = exta_cls_id[4]
    count_cls = db.get_student_count()
    await call.message.answer(text=f'Guruh nomi: {cls_name} \nGuruh o\'qituvchisi: {cls_tname}\nJami o\'quvchilar: {count_cls}')

# CLS

@dp.callback_query(lambda query: query.data.startswith('myg_'))
async def start(call: types.CallbackQuery):
    cls_id = call.data.split('_')[1]
    exta_cls_id = db.select_id_from_student(id=cls_id)
    cls_name = exta_cls_id[2]
    count_cls = db.get_student_count()
    cls_tname = exta_cls_id[3]
    await call.message.answer(text=f'Guruh nomi: {cls_name} \nGuruh o\'qituvchisi: {cls_tname}\nJami o\'quvchilar:{count_cls} ta',reply_markup=cls_menu)

@dp.callback_query(F.data == 'task_table')
async def show_task(call:types.CallbackQuery):
    student_id = call.from_user.id
    class_id = db.select_info(student_id=student_id)
    get_class = class_id[1]
    print(get_class)
    get_task_list = db.select_all_task()

    if not get_task_list:
        await call.message.answer("❌ Hozircha hech qanday vazifa mavjud emas!")
        return

    get_task = get_task_list[-1]

    await call.message.answer(
        text=f"📌 **Bugungi vazifalar:**\n "
             f"📝 **Vazifa:** {get_task[1]}\n"
             f"ℹ️ **Vazifa haqida:** {get_task[2]}\n"
             f"📅 **Joylangan sana:** {get_task[3]}",
        parse_mode="Markdown"
    )
@dp.callback_query(F.data == 'mytask')
async def show_task(call:types.CallbackQuery):
    student_id = call.from_user.id
    class_id = db.select_info(student_id=student_id)
    get_class = class_id[1]
    print(get_class)
    get_task_list = db.select_all_task()

    if not get_task_list:
        await call.message.answer("❌ Hozircha hech qanday vazifa mavjud emas!")
        return

    get_task = get_task_list[-1]

    await call.message.answer(
        text=f"📌 **Bugungi vazifalar:**\n "
             f"📝 **Vazifa:** {get_task[1]}\n"
             f"ℹ️ **Vazifa haqida:** {get_task[2]}\n"
             f"📅 **Joylangan sana:** {get_task[3]}",
        parse_mode="Markdown"
    )
@dp.callback_query(F.data == 'task_table')
async def show_task(call:types.CallbackQuery):
    student_id = call.from_user.id
    class_id = db.select_info(student_id=student_id)
    get_class = class_id[1]
    print(get_class)
    get_task_list = db.select_all_task()

    if not get_task_list:
        await call.message.answer("❌ Hozircha hech qanday vazifa mavjud emas!")
        return

    get_task = get_task_list[-1]

    await call.message.answer(
        text=f"📌 **Bugungi vazifalar:**\n "
             f"📝 **Vazifa:** {get_task[1]}\n"
             f"ℹ️ **Vazifa haqida:** {get_task[2]}\n"
             f"📅 **Joylangan sana:** {get_task[3]}",
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == 'clstable')
async def show_students(call: types.CallbackQuery):
    students_data = db.get_students_by_group()
    print(students_data)
    if not students_data:
        await call.message.answer("📌 O'quvchilar ro'yxati topilmadi.")
        return

    if not students_data:
        await call.message.answer("📌 O'quvchilar ro'yxati topilmadi.")
        return

    keyboard = []
    current_group = None

    for row in students_data:
        if len(row) < 4:  # Kamroq ustun qaytsa, xato chiqmasligi uchun
            print(f"⚠ Xatolik: noto‘g‘ri format: {row}")
            continue  # Xatolikni o‘tkazib yuboramiz

        student_id, student_name, group_id, group_name = row

        if current_group != group_id:
            keyboard.append([InlineKeyboardButton(text=f"📌 {group_name}", callback_data="ignore")])
            current_group = group_id

        keyboard.append([InlineKeyboardButton(text=student_name, callback_data=f"student_{student_id}")])

    inline_kb = InlineKeyboardMarkup(inline_keyboard=keyboard,)

    await call.message.answer("📌 O'quvchilar ro'yxati:", reply_markup=inline_kb)


    @dp.callback_query(F.data.startswith("student_"))
    async def send_student_info(callback: CallbackQuery):
        student_id = int(callback.data.split("_")[1])

        sql = """
        SELECT student_name, group_name, teacher_name 
        FROM Student WHERE student_id = ?;
        """
        student = db.execute(sql, (student_id,), fetchone=True)

        if student:
            student_name, group_name, teacher_name = student
            message_text = (f"📌 O'quvchi Ism-Familiyasi: {student_name}\n"
                            f"🏫 Guruhi: {group_name}\n"
                            f"👨‍🏫 O‘qituvchi: {teacher_name}")
            await callback.message.answer(message_text, parse_mode="HTML")
        else:
            await callback.answer("Ma'lumot topilmadi.", show_alert=True)
