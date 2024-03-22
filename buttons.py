from aiogram import types

# Клавиатура
kb = [[types.KeyboardButton(text='🔐 Зашифровать сообщение'),
       types.KeyboardButton(text='🔓 Расшифровать сообщение')],
      [types.KeyboardButton(text='💰 Подписка'),
       types.KeyboardButton(text='📄 Описание')],
      [types.KeyboardButton(text='💬 Общий чат'),
       types.KeyboardButton(text='💻 Кодовая семантика')],
      [types.KeyboardButton(text='🪪 Профиль')]
      ]
keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                     resize_keyboard=True,
                                     input_field_placeholder="Напишите сообщение")
