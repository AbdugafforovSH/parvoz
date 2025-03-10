from aiogram import types, F
from loader import dp, db

@dp.callback_query(F.data=='statistic')
async def full_stat(call: types.CallbackQuery):

    full_student = db.count_students()
    full_classes = db.count_classes()

    await call.message.answer(text="📊 Parvoz o'quv markazining statistikasi: \n\n"
                                   "📌 Umumiy ma'lumotlar:\n"
                                   f"   ├ 🏫 Jami sinflar: {full_classes} ta\n"
                                   f"   └ 🎓 Jami o'quvchilar: {full_student} nafar")
