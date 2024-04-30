import string


async def message_output(shifr_message, step):  # Асинхронная функция для расшифровки сообщений.
    global decrypted_char

    deshifr_message = ''
    for i in shifr_message:  # Перебор символов в зашифрованном сообщении.
        if (i == ' ' and i in string.punctuation) or not i.isalpha():  # Проверка на пробел или знак пунктуации.
            decrypted_char = i  # Присвоение текущего символа в случае пробела или знака пунктуации.
        else:
            if ord('А') <= ord(i) <= ord('я'):  # Проверка на наличие буквы кириллицы.
                if i.islower():  # Если буква строчная.
                    decrypted_char = chr(((ord(i) - ord('а') - step) % 32) + ord('а'))  # Расшифровка строчной буквы.
                elif i.isupper():  # Если буква заглавная.
                    decrypted_char = chr(((ord(i) - ord('А') - step) % 32) + ord('А'))  # Расшифровка заглавной буквы.
            else:  # Если буква латиницы.
                if i.islower():  # Если буква строчная.
                    decrypted_char = chr(((ord(i) - ord('a') - step) % 26) + ord('a'))  # Расшифровка строчной буквы.
                elif i.isupper():  # Если буква заглавная.
                    decrypted_char = chr(((ord(i) - ord('A') - step) % 26) + ord('A'))  # Расшифровка заглавной буквы.

        deshifr_message += decrypted_char  # Добавление расшифрованного символа к расшифрованному сообщению.

    return deshifr_message
