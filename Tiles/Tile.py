from colorama import Fore, Style

from Base.Map import Map
from Server.Server import Server


class Tile:
    """Класс плиток"""
    way_latter_to_word = {'r': 'Напрпво',
                          'l': 'Налево',
                          'u': 'Вверх',
                          'd': 'Вниз'}

    way_number_to_letter = {1: 'r',
                            2: 'l',
                            3: 'u',
                            4: 'd'}

    alive_creature = 'Пират'
    vehicle = 'Пиратский корабль'
    drop = 'Монета'
    answer = ' '

    def __init__(self):
        """Показатель перевёрнутости(False- лежит рубашкой вверх)"""
        self.unit = None
        self.server = None

    def add_map(self):
        """Вызвать синглтон карты"""
        self.map = Map()

    def add_server(self):
        """Вызвать синглтон сервера"""
        self.server = Server()

    def activate_tile(self, player, unit):
        """Активация плитки"""
        self.add_map()
        self.add_server()
        self.map.save_coord_in_history(unit)

    def fight_on_tile(self, player, unit):
        """Драка на плитке"""
        _, _, *units = self.map.map[unit.y_coord][unit.x_coord]
        for enemy in units:
            if enemy.type in Tile.alive_creature and enemy not in player.units:
                if len(enemy.backpack) > 0:
                    enemy.drop_coin()
                enemy.take_on_board(enemy.player.vehicle[0])
            elif enemy.type in Tile.vehicle and enemy not in player.units:
                unit.dead()
            elif unit.type in Tile.vehicle and enemy not in player.units and enemy.type not in Tile.drop:
                enemy.dead()

    def send_and_get_message(self, player_color, data):
        """Отправить сообщение"""
        self.server.send_message(player_color, data)
        self.server.get_message()

    def print_tile(self, y, x, level, backlight):
        pass

    def search_unit(self, y, x):
        self.add_map()
        units = []
        tile, status, *other = self.map.map[y][x]
        for unit in other:
            if unit.type in Tile.alive_creature:
                sign_colored = self.baclight_unit_with_coin(unit)
                units.append(sign_colored)
        while len(units) != 3:
            units.append(' ')
        return units

    def search_coin(self, y, x):
        count_coin = 0
        tile, status, *other = self.map.map[y][x]
        for drop in other:
            if drop.type in Tile.drop:
                count_coin += 1
        if count_coin > 0:
            return Fore.LIGHTYELLOW_EX + str(count_coin)
        return ' '

    def calculate_color(self, y, x):
        tile, status, *other = self.map.map[y][x]
        for unit in other:
            if unit.type in Tile.alive_creature or unit.type in Tile.vehicle:
                return unit.color
        return Style.RESET_ALL

    def set_backlight_color(self, backlight):
        if backlight is True:
            return Fore.LIGHTYELLOW_EX
        else:
            return ''

    def baclight_unit_with_coin(self, unit):
        if len(unit.backpack) > 0:
            return Fore.LIGHTYELLOW_EX + str(unit.index) + unit.player.color
        else:
            return unit.player.color + str(unit.index)
