from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateLink(StatesGroup):
    waiting_redirect_url = State()
    waiting_source_url = State()
