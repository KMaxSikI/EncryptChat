import string


async def message_input(message, step):  # Асинхронная функция для шифрования сообщений.
    global encrypted_char

    shifr_message = ''
    for i in message:  # Перебор символов в исходном сообщении.
        if (i == ' ' and i in string.punctuation) or not i.isalpha():  # Проверка на пробел или знак пунктуации.
            encrypted_char = i  # Присвоение текущего символа в случае пробела или знака пунктуации.
        else:
            if ord('А') <= ord(i) <= ord('я'):  # Проверка на наличие буквы кириллицы.
                if i.islower():  # Если буква строчная.
                    encrypted_char = chr(((ord(i) - ord('а') + step) % 32) + ord('а'))  # Шифрование строчной буквы.
                elif i.isupper():  # Если буква заглавная.
                    encrypted_char = chr(((ord(i) - ord('А') + step) % 32) + ord('А'))  # Шифрование заглавной буквы.
            else:  # Если буква латиницы.
                if i.islower():  # Если буква строчная.
                    encrypted_char = chr(((ord(i) - ord('a') + step) % 26) + ord('a'))  # Шифрование строчной буквы.
                elif i.isupper():  # Если буква заглавная.
                    encrypted_char = chr(((ord(i) - ord('A') + step) % 26) + ord('A'))  # Шифрование заглавной буквы.

        shifr_message += encrypted_char  # Добавление зашифрованного символа к зашифрованному сообщению.

    return shifr_message
