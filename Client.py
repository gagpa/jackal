import json
import socket
import os
from colorama import init, Style, Fore
import time

from Base.Player import Player


class Client:
    """Класс клиента"""

    def __init__(self):
        # Задание характеристик и переменных сервера
        self.host = '127.0.0.1'
        self.port = 65432
        # Объект клиента
        self.client = None
        # Полученное сообщение
        self.sent_message = None
        # Ответ на сообщение
        self.color = None
        self.gotten_message = None
        self.possible_answers = None
        # Список всех игроков
        self.players = []
        # Игрок ходит
        self.player_move = None
        # Активация библиотеки с подстветкой
        init(convert=True)

        self.command = {'exit': self.exit_from_game}

    @ staticmethod
    def get_info():
        print()

    # Блок создания клаента
    def create_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_players(self, count):
        """Созадть экземпляры игроков"""
        for i in range(count):
            self.players.append(Player())

    def check_answer(self, answer):
        if self.check_with_possible_answer(answer) is True:
            self.send_message(answer)
            return False
        self.check_and_do_command(answer)
        return True

    def check_and_do_command(self, command):
        """Проверить команду"""
        for key in self.command.keys():
            if command == key:
                self.command[key](key)

    def check_with_possible_answer(self, answer):
        """Проверить подходить ответ или нет"""
        for possible_answer in self.possible_answers:
            if answer == possible_answer:
                return True
        return False

    def get_player_answer(self):
        if self.players == [] and self.sent_message is None:
            key = True
            count = input(Fore.LIGHTGREEN_EX + 'CONSOLE: ' + Style.RESET_ALL)
            try:
                self.create_players(int(count))
            except:
                pass
            return count
        return self.player_move.enter_answer()

    # Блок присоединения к серверу
    def connect_with_server(self):
        """Связаться с сервером"""
        self.client.connect((self.host, self.port))

    # Блок взаимодейсвтия с сервером
    def send_message(self, message):
        """Отправить данные"""
        self.save_sent_message(message)
        self.client.send(message.encode('utf-8'))

    def get_message(self):
        """Получить данные"""
        self.save_gotten_message(self.client.recv(30000).decode('utf-8'))
        self.player_move = self.get_move_player()

    # Блок вывода данных
    def print_message(self):
        """Вывод данных"""
        print(self.color + self.gotten_message + Style.RESET_ALL)

    # Блок записи данных
    def save_gotten_message(self, message):
        """Сохранить полученное сообщение"""
        try:
            jsonData = json.loads(message)
            self.color = jsonData['color']
            self.gotten_message = jsonData['message']
            self.possible_answers = jsonData['possible answer']
        except:
            print(message)

    def save_sent_message(self, message):
        """Сохранить отправленное сообщение"""
        self.sent_message = message

    def get_move_player(self):
        for player in self.players:
            if self.color == player.color:
                return player
        return None

    def exit_from_game(self, key):
        """Выйти из игры"""
        self.send_message(key)
        exit()

    # Блок закрытия клиента
    def close_client(self):
        """Закрыть клиент"""
        self.client.close()


# Пользовательский экран
time.sleep(0.1)
client = Client()
client.create_client()
client.connect_with_server()
init(convert=True)
while True:
    clear = lambda: os.system('cls')
    clear()
    key = True
    client.get_message()
    while key:
        # clear()
        client.print_message()
        answer = client.get_player_answer()
        key = client.check_answer(answer)
