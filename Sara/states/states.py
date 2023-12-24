from aiogram.dispatcher.filters.state import State, StatesGroup


class send_forwad(StatesGroup):
    text = State()


class sendAd(StatesGroup):
    text = State()


class verifyDeleteUsers(StatesGroup):
    code = State()


class send_user(StatesGroup):
    id = State()
    habar = State()


class answer(StatesGroup):
    habar = State()