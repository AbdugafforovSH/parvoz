from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db
start_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👥 Guruhlar bo\'yicha reyting',callback_data='groups'), InlineKeyboardButton(text='👁️‍🗨️ Guruhga kirish', callback_data='join_cls')],
    [InlineKeyboardButton(text='📋 Bugungi Vazifalar', callback_data='mytask'), InlineKeyboardButton(text='📩 Vazifani yuborish', callback_data='send_task')],
    [InlineKeyboardButton(text='📊 O\'quv Markazi Haqida', callback_data='statistic')]
])

starts_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👥 Guruhlar bo\'yicha reyting',callback_data='groups'),InlineKeyboardButton(text='➕ Guruh yaratish', callback_data='create')],
    [InlineKeyboardButton(text='🎛️ Davomat', callback_data='attend'), InlineKeyboardButton(text='📩 Vazifa Joylash', callback_data='add_task')],
    [InlineKeyboardButton(text='📋 Tekshirish', callback_data='checkin'), InlineKeyboardButton(text='📨 Xabar Yuborish', callback_data='sendmessage')],
    [InlineKeyboardButton(text='📊 O\'quv Markazi Haqida', callback_data='statistic')]
])

cls_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👥 O\'quvchilar ro\'yxati', callback_data='clstable'),InlineKeyboardButton(text='🗂️ Vazifalar ro\'yxati', callback_data='task_table')],
])


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    @staticmethod
    def main():
        menu = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="♻️ Xabar Yuborish", callback_data="send")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="stat")]
        ])
        return menu

    @staticmethod
    def menuus():
        menu = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Statistika", callback_data="stat")]
        ])
        return menu

    @staticmethod
    def admin():
        menu = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📷 PHOTO XABAR YUBORISH", callback_data="photo")],
            [InlineKeyboardButton(text="🎥 VIDEO XABAR YUBORISH", callback_data="video")],
            [InlineKeyboardButton(text="🎙 VOICE XABAR YUBORISH", callback_data="voice")],
            [InlineKeyboardButton(text="📝 TEXT XABAR YUBORISH", callback_data="text")]
        ])
        return menu

kb = Keyboards()

