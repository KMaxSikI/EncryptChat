from aiogram import types

# Создание клавиатуры с кнопками.
kb = [[types.KeyboardButton(text='🔐 Зашифровать сообщение'),
       types.KeyboardButton(text='🔓 Расшифровать сообщение')],
      [types.KeyboardButton(text='💰 Подписка'),
       types.KeyboardButton(text='📄 Описание')],
      [types.KeyboardButton(text='💬 Общий чат'),
       types.KeyboardButton(text='💻 Кодовая семантика')],
      [types.KeyboardButton(text='🪪 Профиль')]
      ]

# Создание клавиатуры с установленными параметрами.
keyboard = types.ReplyKeyboardMarkup(keyboard=kb,
                                     resize_keyboard=True,
                                     input_field_placeholder="Напишите сообщение")
