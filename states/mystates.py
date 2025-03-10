from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    get_name = State()
    end = State()

class AddClass(StatesGroup):
    start = State()
    tname = State()

class AddTask(StatesGroup):
    start = State()
    get_title = State()
    get_description = State()
    final = State()

class Gname(StatesGroup):
    start = State()
    end = State()

class Grade(StatesGroup):
    file_gets = State()
    send_feedback = State()
    send_grade = State()
    final = State()

class Broadcast(StatesGroup):
    text = State()
    photo = State()
    video = State()
    voice = State()

class Checkin(StatesGroup):
    get_grade = State()
    get_feedback = State()

