import sqlite3
import time
from datetime import datetime


class Data_Base:

    def __init__(self): # Метод инициализации класса.
        self.__db = sqlite3.connect('NeroTek_DataBase.db')
        cursore = self.__db.cursor()
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Users_Messages_Shirf` '
            '(Users_id INTEGER, Message TEXT, Step INTEGER, Result TEXT)')
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Users_Messages_Deshirf` '
            '(Users_id INTEGER, Message TEXT, Step INTEGER, Result TEXT)')
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Payment_subscription` (Users_id PRIMARY KEY, User_NicName TEXT, '
            'Time_sub INTEGER, Data_Sub TEXT, Free_Count_Messages INTEGER)')
        self.__db.commit()

    def __del__(self): # Метод удаления объекта класса.
        self.__db.close()

    async def add_data_shifr(self, Users_id, Message, Step, Result): # Асинхронная функция для добавления зашифрованных данных в базу.
        cursore = self.__db.cursor()
        cursore.execute('''INSERT INTO `Users_Messages_Shirf` VALUES(?,?,?,?)''', (Users_id, Message, Step, Result))
        self.__db.commit()

    async def add_data_deshifr(self, Users_id, Message, Step, Result): # Асинхронная функция для добавления расшифрованных данных в базу.
        cursore = self.__db.cursor()
        cursore.execute('''INSERT INTO `Users_Messages_Deshirf` VALUES(?,?,?,?)''', (Users_id, Message, Step, Result))
        self.__db.commit()

    async def add_users(self, Users_id, User_NicName, Time_sub, Data_Sub, Free_Count_Messages): # Асинхронная функция для добавления пользователей в базу данных.
        cursore = self.__db.cursor()
        cursore.execute('''SELECT Users_id FROM `Payment_subscription` WHERE `Users_id` = ?''', (Users_id,))
        existing_user = cursore.fetchone()
        if existing_user:
            cursore.execute('''UPDATE `Payment_subscription` SET `User_NicName` = ? WHERE `Users_id` = ?''',
                            (User_NicName, Users_id))
        else:
            cursore.execute('''INSERT INTO `Payment_subscription` VALUES (?, ?, ?, ?, ?)''',
                            (Users_id, User_NicName, Time_sub, Data_Sub, Free_Count_Messages))
        self.__db.commit()

    async def get_nik(self, Users_id): # Асинхронная функция для получения имени пользователя из базы данных.

        nik = ""
        cursore = self.__db.cursor()
        result = cursore.execute("SELECT `User_NicName` FROM `Payment_subscription` WHERE `Users_id` = ?",
                                 (Users_id,)).fetchall()
        for row in result:
            nik = str(row[0])
        return nik

    async def get_free_count_messages(self, Users_id): # Асинхронная функция для получения количества бесплатных сообщений из базы данных.

        fcm = ""
        cursore = self.__db.cursor()

        result = cursore.execute("SELECT `Free_Count_Messages` FROM `Payment_subscription` WHERE `Users_id` = ?",
                                 (Users_id,)).fetchall()

        for row in result:
            fcm = str(row[0])
        return fcm

    async def set_sub_time(self, Users_id, Time_sub): # Асинхронная функция для обновления времени подписки пользователя в базе данных.
        cursore = self.__db.cursor()
        cursore.execute('''UPDATE `Payment_subscription` SET `Time_sub` = ? WHERE `Users_id` = ?''',
                        (Time_sub, Users_id,))
        self.__db.commit()

    def get_time_sub(self, Users_id): # Функция для получения времени подписки пользователя из базы данных.
        time_sub = 0

        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT `Time_sub` FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchall()
        for row in result:
            time_sub = int(row[0])
        return time_sub

    def get_sub_status(self, Users_id): # Функция для получения статуса подписки пользователя из базы данных.
        global time_sub
        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT `Time_sub` FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchall()
        for row in result:
            time_sub = int(row[0])
        if time_sub > int(time.time()):
            return True
        else:
            return False

    def get_id_status(self, Users_id):  # Функция для проверки статуса пользователя по его идентификатору.
        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT COUNT(*) FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchone()
        user_count = result[0]
        if user_count > 0:
            return True
        else:
            return False

    def get_free_message(self, Users_id):  # Функция для проверки доступных бесплатных сообщений пользователя по его идентификатору.
        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT `Free_Count_Messages` FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchone()

        free_count = int(result[0])
        if free_count != 0:
            return True
        else:
            return False

    async def get_data_sub(self, Users_id):  # Асинхронный метод для получения данных о подписке пользователя по его идентификатору.
        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT `Time_sub` FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchone()
        if result and result[0]:
            time_reverse = result[0]
            subscription_date = datetime.fromtimestamp(time_reverse)
            subscription_date_format = subscription_date.strftime('%d.%m.%Y')
            cursore.execute('''UPDATE `Payment_subscription` SET `Data_Sub` = ? WHERE `Users_id` = ?''',
                            (subscription_date_format, Users_id))
            self.__db.commit()
            return True
        else:
            return False

    async def delete_free_message(self, Users_id):  # Асинхронная функция для удаления бесплатного сообщения из базы данных.
        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT `Free_Count_Messages` FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchone()
        free_count = int(result[0])
        if free_count > 0:
            cursore.execute('''UPDATE `Payment_subscription` SET `Free_Count_Messages` = `Free_Count_Messages` -1 
            WHERE `Users_id` = ?''', (Users_id,))
        self.__db.commit()