from aiogram.utils.keyboard import KeyboardButton, KeyboardBuilder, ReplyKeyboardMarkup

role_button =ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True,
keyboard=[
    [KeyboardButton(text='🧑‍🏫 O\'qituvchi')],
    [KeyboardButton(text='👨‍🎓 Talaba')]
]
)

admin_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                   keyboard=
                                   [
                                       [KeyboardButton(text='➕ Guruh Yaratish')]
                                   ])

attendance = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                 keyboard=[[KeyboardButton(text='📋 Davomatni tekshirish')]])