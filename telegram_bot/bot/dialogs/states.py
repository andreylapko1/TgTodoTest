from aiogram.fsm.state import StatesGroup, State


class TaskCreation(StatesGroup):
    title = State()
    description = State()
    category = State()
    due_date = State()
    confirm = State()

