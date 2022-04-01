import json
import socket
import platform
import subprocess

from Base.Map import Map


class Server:
    """Класс сервера"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Server, cls).__new__(cls)
        return cls.instance

    # Блок создания сервера
    def create_tcp_server(self):
        # Задание характеристик и переменных сервера
        self.host = '127.0.0.1'
        self.port = 65432
        # объекты соединения
        self.server = None
        self.client = None
        # Информация о клиенте
        self.addr = None
        # Полученное сообщение
        self.sent_message = ()
        # Ответ на сообщение
        self.gotten_message = None
        # Создание сервера
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

        self.command = {'exit': self.exit_from_game}

    # Блок связи с клиентом
    def connect_with_client(self):
        """Связть с клиентом"""
        Server.open_client()
        self.server.listen()
        self.client, self.addr = self.server.accept()

    @ classmethod
    def open_client(cls):
        """Открыть клиент в новой консоли"""
        if platform.system() == 'Windows':
            new_window_command = 'cmd.exe /c start'.split()
        else:
            new_window_command = 'x-terminal-emulator -e'.split()
        command = 'python3 Client.py'.split()
        subprocess.check_call(new_window_command + command)

    # Блок взаимодейсвия с клиентом
    def send_message(self, player_color, data):
        """Отправить данные клиенту"""
        message, possible_answer = data
        self.save_sent_message(player_color, message, possible_answer)
        self.client.send(self.convert_data_to_json
                         (player_color, message, possible_answer).encode('utf-8'))

    def get_message(self):
        """Получить данные от клиента"""
        self.save_gotten_message(self.client.recv(2048).decode('utf-8'))

    # Блок записи данных
    def save_sent_message(self, *message):
        """Записать сообщение"""
        self.sent_message = message

    def save_gotten_message(self, message):
        """Записать ответ"""
        self.check_comand(message)
        self.gotten_message = message

    def check_comand(self, command):
        """Проверить команду"""
        for key in self.command.keys():
            if key == command:
                self.command[key]()

    def exit_from_game(self):
        exit()

    def convert_data_to_json(self, player_color, message, possible_answer):
        """Конвертировать данные в Json"""
        jsonData = {
            'color': player_color,
            'message': message,
            'possible answer': possible_answer
        }
        return json.dumps(jsonData, ensure_ascii=False)

    # Блок закрытия клиента и сервера
    def close_client(self):
        """Закрыть клиент"""
        self.client.close()

    def close_server(self):
        """Закрытие сервера"""
        self.server.close()

    def add_map(self):
        """Добавить карту"""
        self.map = Map()

    @ staticmethod
    def message_info():
        """Отправить информацию о юнитах"""
        pass
