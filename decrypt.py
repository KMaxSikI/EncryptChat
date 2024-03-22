import string


async def message_output(shifr_message, step):  # расшифровка сообщений
    global decrypted_char

    deshifr_message = ''
    for i in shifr_message:
        if (i == ' ' and i in string.punctuation) or not i.isalpha():
            decrypted_char = i
        else:
            if ord('А') <= ord(i) <= ord('я'):
                if i.islower():
                    decrypted_char = chr(((ord(i) - ord('а') - step) % 32) + ord('а'))
                elif i.isupper():
                    decrypted_char = chr(((ord(i) - ord('А') - step) % 32) + ord('А'))
            else:
                if i.islower():
                    decrypted_char = chr(((ord(i) - ord('a') - step) % 26) + ord('a'))
                elif i.isupper():
                    decrypted_char = chr(((ord(i) - ord('A') - step) % 26) + ord('A'))

        deshifr_message += decrypted_char

    return deshifr_message