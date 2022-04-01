from .Unit import Unit


class Ship(Unit):
    """Класс корабля"""
    sign_level = {1: ' _____ _____ ',
                  2: '|     |>>   |',
                  3: '|     |>    |',
                  4: '| <==+++==> |',
                  5: '|_____ _____|'}

    def __init__(self, player):
        super(Ship, self).__init__(player)
        self.type = 'Пиратский корабль'
        self.name = self.type
        self.sign = '+'
        self.backpack_max = 100
        """Борт на корабле"""
        self.board = []
        self.life = True
        self.player.count = len(self.backpack)

        self.sign_paint_tile = Ship.sign_level

    def take_on_board(self, unit):
        """Посадить на борт юнита"""
        self.add_map()
        try:
            if unit in self.map.map[unit.y_coord][unit.x_coord]:
                self.map.del_unit_from_cell(unit)
            self.board.append(unit)
            unit.y_coord = self.y_coord
            unit.x_coord = self.x_coord
        except AttributeError:
            self.board.append(unit)
            unit.y_coord = self.y_coord
            unit.x_coord = self.x_coord
        else:
            if len(unit.backpack) > 0:
                unit.give_coin(self)

    def take_off_board(self, unit, dimension_map=13):
        """Высадить юнита"""
        self.board.remove(unit)
        if self.y_coord == 0:
            return 'd'
        elif self.y_coord == dimension_map - 1:
            return 'u'
        elif self.x_coord == 0:
            return 'r'
        elif self.x_coord == dimension_map - 1:
            return 'l'

    def board_change_coord(self):
        """Передвинуть персонажей на борту вместе кораблём"""
        for unit in self.board:
            unit.y_coord = self.y_coord
            unit.x_coord = self.x_coord

    def calculate_ways(self):
        """Расчёт возможных путей"""
        for i in self.step:
            if self.y_coord == 0 or self.y_coord == self.map.dimension_map - 1:
                self.ways.append([self.y_coord, self.x_coord + i])
            elif self.x_coord == 0 or self.x_coord == self.map.dimension_map - 1:
                self.ways.append([self.y_coord + i, self.x_coord])
        self.ways.sort()

    def choose_way(self, dimension_map=13):
        """Метод передвижения коробля"""
        if self.y_coord == dimension_map - 1 or self.y_coord == 0:
            return 'r/l'
        elif self.x_coord == dimension_map - 1 or self.x_coord == 0:
            return 'u/d'
