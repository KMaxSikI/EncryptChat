import sqlite3
import time


class Data_Base:

    def __init__(self):
        self.__db = sqlite3.connect('NeroTek_DataBase.db')
        cursore = self.__db.cursor()
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Users_Messages_Shirf` '
            '(Users_id INTEGER, Message TEXT, Step INTEGER, Result TEXT)')
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Users_Messages_Deshirf` '
            '(Users_id INTEGER, Message TEXT, Step INTEGER, Result TEXT)')
        cursore.execute(
            'CREATE TABLE IF NOT EXISTS `Payment_subscription` (Users_id PRIMARY KEY, User_NicName TEXT, Time_sub INTEGER)')
        self.__db.commit()

    def __del__(self):
        self.__db.close()

    async def add_data_shifr(self, Users_id, Message, Step, Result):
        cursore = self.__db.cursor()
        cursore.execute('''INSERT INTO `Users_Messages_Shirf` VALUES(?,?,?,?)''', (Users_id, Message, Step, Result))
        self.__db.commit()

    async def add_data_deshifr(self, Users_id, Message, Step, Result):
        cursore = self.__db.cursor()
        cursore.execute('''INSERT INTO `Users_Messages_Deshirf` VALUES(?,?,?,?)''', (Users_id, Message, Step, Result))
        self.__db.commit()

    async def add_users(self, Users_id, User_NicName, Time_sub):
        cursore = self.__db.cursor()
        cursore.execute('''SELECT Users_id FROM `Payment_subscription` WHERE `Users_id` = ?''', (Users_id,))
        existing_user = cursore.fetchone()
        if existing_user:
            cursore.execute('''UPDATE `Payment_subscription` SET `User_NicName` = ? WHERE `Users_id` = ?''',
                            (User_NicName, Users_id))
        else:
            cursore.execute('''INSERT INTO `Payment_subscription` VALUES (?, ?, ?)''', (Users_id, User_NicName, Time_sub))
        self.__db.commit()

    async def get_nik(self, Users_id):

        nik = ""
        cursore = self.__db.cursor()
        result = cursore.execute("SELECT `User_NicName` FROM `Payment_subscription` WHERE `Users_id` = ?",
                                 (Users_id,)).fetchall()
        for row in result:
            nik = str(row[0])
        return nik

    async def set_sub_time(self, Users_id, Time_sub):
        cursore = self.__db.cursor()
        cursore.execute('''UPDATE `Payment_subscription` SET `Time_sub` = ? WHERE `Users_id` = ?''',
                        (Time_sub, Users_id,))
        self.__db.commit()

    def get_time_sub(self, Users_id):
        time_sub = 0

        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT `Time_sub` FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchall()
        for row in result:
            time_sub = int(row[0])
        return time_sub

# Проверить метод
    def get_sub_status(self, Users_id):
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

    def get_id_status(self, Users_id):
        cursore = self.__db.cursor()
        result = cursore.execute('''SELECT COUNT(*) FROM `Payment_subscription` WHERE `Users_id` = ?''',
                                 (Users_id,)).fetchone()
        user_count = result[0]
        if user_count > 0:
            return True  # Пользователь найден в столбце Users_id
        else:
            return False  # Пользователь не найден в столбце Users_id