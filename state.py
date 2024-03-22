from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):  # Класс состояний
    shifr = State()  # Состояние шифровки
    deshifr = State()  # Состояние дешифровки
    buy_subscription = State()  # Состояние подписки
    feedback = State()  # Состояние обратная связь
    description = State()  # Состояние описание
    info_channal = State()  # Состояние информационный канал
