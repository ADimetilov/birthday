from aiogram.fsm.state import State,StatesGroup

class Birthday_State(StatesGroup):
    Day = State()
    Month = State()
    Name = State()
    mes_id = State()
class Birthdays_State(StatesGroup):
    id = State()
    solution = State()
class Notifi_game(StatesGroup):
    name = State()
    