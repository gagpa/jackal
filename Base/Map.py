import os
from colorama import Fore, Style


class Map:
    """Класс карты"""

    alive_creature = 'Пират'
    vehicle = 'Пиратский корабль'

    close_cell = {1: '             ',
                  2: '             ',
                  3: '             ',
                  4: '             ',
                  5: '             '}
    close_target_cell = {1: ' _____ _____ ',
                         2: '|           |',
                         3: '|     {0}     |',
                         4: '|           |',
                         5: '|_____ _____|'}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Map, cls).__new__(cls)
        return cls.instance

    # Блок создания карты
    def create_map(self, deck, all_coin, dimension_map, players):
        # Игроки
        self.players = players
        # Игровая колода
        self.deck = deck
        # Список карты
        self.map = []
        # Список клетки
        self.cell = []
        # Размер карты
        self.dimension_map = dimension_map
        self.respawn_coord_units = {
            1: (0, self.dimension_map // 2),
            2: (self.dimension_map - 1, self.dimension_map // 2),
            3: (self.dimension_map // 2, self.dimension_map - 1),
            4: (self.dimension_map // 2, 0)
        }

        # Спец знак закртой клетки
        self.sign_fog = Fore.CYAN + '()'
        # Переменные для выполнения методов и актвации карт
        self.key = False
        self.ways_count = None
        # Переменные для сохранения истории хода
        self.history_y_coord = []
        self.history_x_coord = []
        # Сформировать игровое поле
        self.add_all_tile()
        # Добавить игроков на игровое поле
        self.insert_all_players_on_map()
        self.all_coin = all_coin

    def add_all_tile(self):
        """Дабавить все плитки на карту"""
        for y in range(self.dimension_map):
            # Создаём переменную для постепенного заполнения карты
            level = []
            for x in range(self.dimension_map):
                # Проверки координат для воды
                if x == 0 or x == self.dimension_map - 1 or y == 0 or y == self.dimension_map - 1:
                    self.add_water()
                elif x == 1 and y == 1:
                    self.add_water()
                elif x == 1 and y == self.dimension_map - 2:
                    self.add_water()
                elif x == self.dimension_map - 2 and y == 1:
                    self.add_water()
                elif x == self.dimension_map - 2 and y == self.dimension_map - 2:
                    self.add_water()
                # Иначе вставляем плитку не воды
                else:
                    self.add_tile()
                # Подставляем сформированную клетку в список
                level.append(self.cell)
            # Вставляем список в карту
            self.map.append(level)

    def add_water(self):
        """Добавить воду на карту"""
        # Создаём клетку
        self.cell = []
        # Вставляем плитку воды (вся вода находится в конце колоды)
        self.cell.append(self.deck[-1])
        # Вставляем статус открытости ячейки
        self.cell.append(True)
        # Удалить воду из колоды
        self.deck.pop(-1)

    def add_tile(self):
        """Добавить карту из колоды"""
        # Создаём клетку
        self.cell = []
        # Вставляем в клетку класс плитки из колоды
        self.cell.append(self.deck[0])
        # Вставляем в клетку статус закрытости клетки
        self.cell.append(False)
        # Убираем из колоды вставленную плитку
        self.deck.pop(0)

    def insert_all_players_on_map(self):
        """Вставить всех игроков на карту"""
        for player in self.players:
            self.set_ship_coord(player)
            self.insert_unit_in_cell(player.units[0])

    def set_ship_coord(self, player):
        """Место появления игроков"""
        for unit in player.units:
            unit.y_coord, unit.x_coord = self.respawn_coord_units[player.index]

    # Блок перемещения юнитов
    def action_on_map(self, player, unit):
        """Переместить юнита на карте"""
        # Выходим с корабля
        if self.check_ship_in_water(player, unit.y_coord, unit.x_coord) is True:
            self.move_unit_on_map(player, unit)
        else:
            y_new, x_new = self.get_change_unit_coord(unit)
            # Заходим на корабль
            if self.check_ship_in_water(player, y_new, x_new) is True:
                if unit in self.map[unit.y_coord][unit.x_coord]:
                    self.del_unit_from_cell(unit)
                unit.take_on_board(player.vehicle[0])
            # Не можем выйти из воды
            elif self.get_tile(unit.y_coord, unit.x_coord).name == 'Вода' \
                    and self.get_tile(y_new, x_new).name != 'Вода':
                player.set_way_unit()
            else:
                self.move_unit_on_map(player, unit)

    def move_unit_on_map(self, player, unit):
        self.save_coord_in_history(unit)
        if unit in self.map[unit.y_coord][unit.x_coord]:
            self.del_unit_from_cell(unit)
        self.change_unit_coord(unit)
        self.insert_unit_in_cell(unit)
        if False in self.map[unit.y_coord][unit.x_coord]:
            self.open_cell(player, unit)
        self.activate_cell(player, unit)

    def check_ship_in_water(self, player, y, x):
        cell = self.map[y][x]
        for ship in cell:
            if ship in player.vehicle:
                return True
        return False

    def get_tile(self, y, x):
        return self.map[y][x][0]

    def insert_unit_in_cell(self, unit):
        """Вставляем юнита в клетку"""
        self.map[unit.y_coord][unit.x_coord].append(unit)

    def del_unit_from_cell(self, unit):
        """Удалить юнита из клетки"""
        self.map[unit.y_coord][unit.x_coord].remove(unit)

    def open_cell(self, player, unit):
        """Открыть плитку"""
        # Вводим переменную для более удобного чтения
        cell = self.map[unit.y_coord][unit.x_coord]
        # Меняем статус плитку на открытый
        cell[1] = True
        tile = cell[0]
        # Создаём объект плитки
        cell[0] = tile()
        # Выбросить монетку если есть
        if len(unit.backpack) > 0:
            unit.drop_coin()

    def activate_cell(self, player, unit):
        """Активировать плитку"""
        # Вводим переменные для более удобного чтения
        tile, *_ = self.map[unit.y_coord][unit.x_coord]
        # Проверяем на форт
        tile.activate_tile(player, unit)
        if unit in player.alive_creature:
            check, coin = unit.check_coin()
            if check is True:
                unit.check_limit_backpack_and_put(coin)

    def get_change_unit_coord(self, unit):
        if unit.way == 'r':
            return unit.y_coord, unit.x_coord + 1
        elif unit.way == 'l':
            return unit.y_coord, unit.x_coord - 1
        elif unit.way == 'd':
            return unit.y_coord + 1, unit.x_coord
        elif unit.way == 'u':
            return unit.y_coord - 1, unit.x_coord

    def change_unit_coord(self, unit):
        """Метод изменения координат"""
        if unit.way == 'r':
            unit.x_coord += 1
        elif unit.way == 'l':
            unit.x_coord -= 1
        elif unit.way == 'd':
            unit.y_coord += 1
        elif unit.way == 'u':
            unit.y_coord -= 1

    def get_history_coord(self):
        """Вернуть историю хода"""
        return self.history_y_coord, self.history_x_coord

    def save_coord_in_history(self, unit):
        """Сохранить предыдущие координаты"""
        self.history_y_coord.append(unit.y_coord)
        self.history_x_coord.append(unit.x_coord)

    def clean_history(self):
        """Отчистить историю хода"""
        self.history_y_coord = []
        self.history_x_coord = []

    def create_list_history(self):
        history = []
        for x, y in enumerate(self.history_y_coord):
            history.append([y, self.history_x_coord[x]])
        return history

    # Отображение информации
    def print_massive(self):
        """Вывести массив карты"""
        for level in self.map:
            print(level)

    def print_map_opened(self):
        """Вывести открытую карту"""
        for level in self.map:
            for cell in level:
                tile, *_ = cell
                print(Fore.YELLOW + tile.sign * 2 + Style.RESET_ALL, end='')
            print()

    def print_map(self, ways=None):
        clear = lambda: os.system('cls')
        clear()
        if ways is None:
            ways = []
        for y in range(self.dimension_map):
            for level in range(1, 6):
                for x in range(self.dimension_map):
                    tile, status, *_ = self.map[y][x]
                    backlight = self.backlight_print(y, x, ways)
                    if status is True:
                        tile.print_tile(y, x, level, backlight)
                    else:
                        if backlight is False:
                            self.print_close_cell(level)
                        else:
                            self.print_close_target_cell(y, x, level, ways)
                print()

    def print_close_cell(self, level):
        print(Map.close_cell[level] + Style.RESET_ALL, end='')

    def print_close_target_cell(self, y, x, level, ways):
        if level == 3:
            text = Map.close_target_cell[level].format(self.check_index_ways(y, x, ways))
            print(Fore.LIGHTYELLOW_EX + text + Style.RESET_ALL, end='')
        else:
            print(Fore.LIGHTYELLOW_EX + Map.close_target_cell[level] + Style.RESET_ALL, end='')

    def backlight_print(self, y, x, ways):
        if len(ways) > 0:
            if [y, x] in ways:
                return True
        return False

    def check_index_ways(self, y, x, ways):
        if [y, x] in ways:
            return ways.index([y, x]) + 1
