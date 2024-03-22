import SQL_DB
import asyncio
import logging
import sys
import buttons as bt
import state as st
import text as txt
import encrypt as en
import decrypt as de
import time
import re
import random

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F
from datetime import timedelta
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = '5518716450:AAH-2v-qOrseYSvOnMlYD4714GWongaXSkM'
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
PAYMENTS_TOKEN = "381764678:TEST:69793"

price = types.LabeledPrice(label="Подписка на 30 дней", amount=1000 * 100)  # в копейках (руб)

# @KikerEhoBot, https://t.me/KikerEhoBot - ссылка на тестовый бот

SQL_DB = SQL_DB.Data_Base()
RESTR = r"[\w\D'._+-]+#[\d]+"


def days_to_seconds(days):
    return days * 24 * 60 * 60  # Перевод дней в секунды


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if SQL_DB.get_id_status(message.from_user.id):
        await message.answer(f'С возвращением {hbold(message.from_user.full_name)} !', reply_markup=bt.keyboard)
    else:
        await message.reply(f'Добро пожаловать, {hbold(message.from_user.full_name)} !\n'
                            f'\n'
                            f'{txt.greeting_message}', reply_markup=bt.keyboard)
        await SQL_DB.add_users(message.from_user.id, message.from_user.full_name, 0)


async def shifr_message(message: Message, state: FSMContext):
    if message.text is not None and re.match(RESTR, message.text):
        text_input = await en.message_input(message.text.split('#')[0], int(message.text.split('#')[1]))
        await message.answer(text_input)
        await SQL_DB.add_data_shifr(message.from_user.id, message.text.split('#')[0], int(message.text.split('#')[1]),
                                    text_input)
        await asyncio.sleep(random.randint(600, 600))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await state.clear()
    else:
        await message.answer('Введите корректный формат сообщения ("Сообщение"#4, без кавычек)')
        await asyncio.sleep(random.randint(20, 20))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


async def deshifr_message(message: Message, state: FSMContext):
    if message.text is not None and re.match(RESTR, message.text):
        text_output = await de.message_output(message.text.split('#')[0], int(message.text.split('#')[1]))
        await message.answer(text_output)
        await SQL_DB.add_data_deshifr(message.from_user.id, message.text.split('#')[0], int(message.text.split('#')[1]),
                                      text_output)
        await asyncio.sleep(random.randint(600, 600))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await state.clear()
    else:
        await message.answer('Введите корректный формат сообщения ("Сообщение"#4, без кавычек)')
        await asyncio.sleep(random.randint(20, 20))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


@dp.message(F.text.lower() == '🔐 зашифровать сообщение')
async def encrypt(message: types.Message, state: FSMContext):
    await state.set_state(st.States.shifr)
    await message.answer(f'{txt.shifr_text}')
    await asyncio.sleep(random.randint(20, 20))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


@dp.message(F.text.lower() == '🔓 расшифровать сообщение')
async def decrypt(message: types.Message, state: FSMContext):
    await state.set_state(st.States.deshifr)
    await message.answer(f'{txt.deshifr_text}')
    await asyncio.sleep(random.randint(20, 20))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


@dp.message(F.text.lower() == '💬 общий чат')
async def feedback(message: types.Message, state: FSMContext):
    if SQL_DB.get_sub_status(message.from_user.id):
        await state.set_state(st.States.feedback)
        tg_encript_group = "https://t.me/encript_chat"
        await message.answer(f"Спасибо что вы с нами, что бы присоединиться к сообществу\n"
                             f" перейдите по ссылке: {tg_encript_group}")
        await asyncio.sleep(random.randint(20, 20))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await state.clear()
    else:
        await message.answer('Чат с другими участниками доступен только по подписке.')
        await asyncio.sleep(random.randint(20, 20))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


@dp.message(F.text.lower() == '💻 кодовая семантика')
async def info_channal(message: types.Message, state: FSMContext):
    if SQL_DB.get_sub_status(message.from_user.id):
        await state.set_state(st.States.info_channal)
        tg_info_group = "https://t.me/Program_semanti"
        await message.answer(f"Вступайте в самое крутое сообщество по программированию по ссылке {tg_info_group}")
        await asyncio.sleep(random.randint(20, 20))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        await state.clear()
    else:
        await message.answer('Этот канал предназначен для новичков в программировании.\n'
                             'Он помогает освоить основы и советует, как улучшить навыки,\n'
                             'общаясь с сообществом программистов.\n'
                             'Доступ к каналу только по подписке.')
        await asyncio.sleep(random.randint(20, 20))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


@dp.message(F.text.lower() == '🪪 профиль')
async def profile(message: types.Message):
    user_nik = "Имя профиля: " + await SQL_DB.get_nik(message.from_user.id)
    user_sub = time_sub_day(SQL_DB.get_time_sub(message.from_user.id))
    if not user_sub:
        user_sub = "Нет подписки"

    user_sub = "\nПодписка оформлена на: " + user_sub
    await bot.send_message(message.from_user.id, user_nik + user_sub)
    await asyncio.sleep(random.randint(20, 20))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


@dp.message(F.text.lower() == '📄 описание')
async def description(message: types.Message, state: FSMContext):
    await state.set_state(st.States.description)
    await message.answer(f'{txt.description}')
    await asyncio.sleep(random.randint(180, 180))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    await state.clear()


@dp.message(F.text.lower() == '💰 подписка')
async def buy_subscription(message: types.Message, state: FSMContext):
    await state.set_state(st.States.buy_subscription)
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на 30 дней",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[price],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    await asyncio.sleep(random.randint(300, 300))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
    await state.clear()


@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    if message.successful_payment.invoice_payload == "test-invoice-payload":
        time_sub = int(time.time()) + days_to_seconds(30)
        await SQL_DB.set_sub_time(message.from_user.id, time_sub)
        await bot.send_message(message.chat.id, 'Подписка успешно оплачена')
        await asyncio.sleep(random.randint(300, 300))
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


dp.message.register(shifr_message, st.States.shifr)
dp.message.register(deshifr_message, st.States.deshifr)
dp.message.register(feedback, st.States.feedback)
dp.message.register(description, st.States.description)
dp.message.register(info_channal, st.States.info_channal)
dp.message.register(buy_subscription, st.States.buy_subscription)


@dp.message()
async def handle_messages(message: types.Message):
    await message.answer('Я вас не понимаю.\n'
                         'Пожалуйста используйте кнопки для взаимодействия со мной.')
    await asyncio.sleep(random.randint(10, 10))
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
