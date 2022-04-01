from colorama import Fore

from Units.Pirate import Pirate
from Units.Ship import Ship
from Units.Unit import Unit


class Party:
    index = 0
    color = (Fore.LIGHTRED_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX)

    def __init__(self):
        # Все подконтрольные юниты
        self.units = []
        self.unit = None
        # Все подконтрольные живые существа
        self.alive_creature = []
        self.dead_creature = []
        # Транспорты передвижения
        self.vehicle = []
        Party.index += 1
        self.index = Party.index
        self.color = Party.color[self.index - 1]
        self.generate_units()

    def generate_units(self):
        """Генерируем юнитов, на 0-вом месте всегда корабль"""
        # Создаём корабль
        self.units.append(Ship(self))
        # Создаём пиратов
        for i in range(1, 4):
            self.units.append(Pirate(self, i))
        # Создание отдельных списков со всеми юнитами игрока
        self.create_list_vehicle_and_alive()
        # Добавить всеъ игроков на борт
        self.all_pirates_go_on_board()

    def insert_unit(self, unit):
        """Метод загрузки юнита"""
        if unit.type in Unit.alive_creature:
            self.alive_creature.append(unit)
        elif unit.type in Unit.vehicle:
            self.vehicle.append(unit)

    # Блок взаимодействия пирата с кораблём
    def all_pirates_go_on_board(self):
        """Посадить всех пиратов на корабль"""
        for pirate in self.alive_creature:
            self.vehicle[0].take_on_board(pirate)

    def create_list_vehicle_and_alive(self):
        """Метод загрузки транспорта"""
        for unit in self.units:
            self.insert_unit(unit)
