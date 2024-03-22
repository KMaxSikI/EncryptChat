import string


async def message_input(message, step):  # шифрование сообщений
    global encrypted_char

    shifr_message = ''
    for i in message:
        if (i == ' ' and i in string.punctuation) or not i.isalpha():
            encrypted_char = i
        else:
            if ord('А') <= ord(i) <= ord('я'):
                if i.islower():
                    encrypted_char = chr(((ord(i) - ord('а') + step) % 32) + ord('а'))
                elif i.isupper():
                    encrypted_char = chr(((ord(i) - ord('А') + step) % 32) + ord('А'))
            else:
                if i.islower():
                    encrypted_char = chr(((ord(i) - ord('a') + step) % 26) + ord('a'))
                elif i.isupper():
                    encrypted_char = chr(((ord(i) - ord('A') + step) % 26) + ord('A'))

        shifr_message += encrypted_char

    return shifr_message
