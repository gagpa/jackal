from colorama import Fore
import time

from Server.Server import Server
from Base.Deck import Deck
from Base.Map import Map
from Base.Party import Party
from Base.Turns import Turns


class GM:
    """Класс игры"""

    def __init__(self):
        """Создание игры"""
        self.color_interface = Fore.WHITE
        self.all_groups = []
        self.deck = None
        self.map = None
        self.server = None
        self.turns = None
        self.dimension_map = 13
        self.quantity_players = None

    # Блок начала игры
    def game_create_all_object(self):
        """Метода запуска игры"""
        print('Игра зупущена', end='\n\n')
        """Создание игрока"""
        self.create_server()
        self.create_units()
        self.create_deck()
        self.create_map()
        self.create_turns()

    def create_server(self):
        """Метод создания сервера"""
        self.server = Server()
        self.server.create_tcp_server()
        self.server.connect_with_client()

    def create_turns(self):
        """Создать фазу хода"""
        self.turns = Turns()

    def create_units(self):
        """Создание игроков"""
        self.set_quantity_players()
        for i in range(self.quantity_players):
            self.all_groups.append(Party())

    def create_deck(self):
        """Создание колоды"""
        self.deck = Deck(self.dimension_map)

    def create_map(self):
        """Создать карту"""
        self.map = Map()
        self.map.create_map(self.deck.deck, self.deck.all_coin, self.dimension_map, self.all_groups)

    def set_quantity_players(self):
        """Установить количество игроков"""
        self.server.send_message(self.color_interface, self.message_players())
        self.server.get_message()
        self.quantity_players = int(self.server.gotten_message)

    def message_players(self):
        data = 'Сколько игроков будет играть?'
        answer = '1/2/3/4'.split('/')
        return data, answer

    # Блок смены раунда
    def start(self):
        """Смена хода"""
        while True:
            for party in self.all_groups:
                self.turns.do_round(party)

    # Методы вывода информации
    def print_map(self):
        self.map.print_map()


game = GM()
game.game_create_all_object()
game.start()
