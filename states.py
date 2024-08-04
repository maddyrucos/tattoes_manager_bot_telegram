from aiogram.dispatcher.filters.state import State, StatesGroup

class Client(StatesGroup):

    default = State()
    name = State()
    number = State()

class Worker(StatesGroup):

    default = State()

class Admin(StatesGroup):

    default = State()
    info = State()
    description = State()