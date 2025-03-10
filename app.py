from loader import dp,bot,db
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio
from utils.notify_admins import start,shutdown
from utils.set_botcommands import commands
import handlers
import middlewares
import logging
import sys

async def main():

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands,scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        # Create Users Table
        try:
            db.create_table_users()
            db.create_table_class()
            db.create_table_attendance()
            db.create_table_tasks()
            db.create_table_submission()
            db.create_table_checking()
            db.create_table_notification()
            db.create_table_message()
            db.create_table_files()
            db.create_table_rating()
            db.create_table_sinfo()
        except:
            pass
        #############################
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

async def clear_attendance():
    while True:
        await asyncio.sleep(86400)
        db.execute("DELETE FROM Attendance", commit=True)
