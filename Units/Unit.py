from abc import ABC

from Base.Map import Map


class Unit(ABC):
    """Класс юнита"""
    revers_way = {'r': 'l',
                  'l': 'r',
                  'u': 'd',
                  'd': 'u'}

    revers_effect = {True: False,
                     False: True}

    alive_creature = 'Пират'
    vehicle = 'Пиратский корабль'

    def __init__(self, player):
        self.under_effect = False
        self.player = player
        self.type = None
        self.color = player.color
        self.backpack = []
        self.backpack_max = None
        self.map = None
        self.x_coord = None
        self.y_coord = None
        self.way = None
        self.ways = []
        self.step = [-1, 1]

    def under_effect_on(self):
        self.under_effect = True

    def under_effect_off(self):
        self.under_effect = False

    def change_under_effect(self):
        """Снять, накинуть эффект"""
        self.under_effect = Unit.revers_effect[self.under_effect]

    def calculate_ways(self):
        """Расчёт возможных путей"""
        if self.under_effect is False:
            for i in self.step:
                if 1 <= self.y_coord + i <= self.map.dimension_map - 2:
                    self.ways.append([self.y_coord + i, self.x_coord])
                if 1 <= self.x_coord + i <= self.map.dimension_map - 2:
                    self.ways.append([self.y_coord, self.x_coord + i])
            self.ways.sort()

    # Блок взаимодействия с монетой
    def get_coin(self, unit, coin):
        """Получить монетку"""
        if len(self.backpack) < self.backpack_max:
            self.backpack.append(coin)
        else:
            unit.get_coin(self, coin)

    def give_coin(self, unit):
        """Дать монетку"""
        coin, *_ = self.backpack
        self.backpack.remove(coin)
        unit.get_coin(self, coin)

    # Блок взаимодействия с картой
    def add_map(self):
        self.map = Map()
