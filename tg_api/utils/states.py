from aiogram.fsm.state import State, StatesGroup


class GetArg(StatesGroup):
    quote_arg = State()
    graph_arg = State()

