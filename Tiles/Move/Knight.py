from colorama import Style

from Tiles.Tile import Tile


class Knight(Tile):
    """Класс лошади"""
    name = 'Ход конём'
    sign = '@'
    sign_level = {1: ' _____ _____ ',
                  2: '|     {0}     |',
                  3: '|    Ход    |',
                  4: '|   конём   |',
                  5: '|_____ _____|'}

    def __init__(self):
        # Направление стрелки
        super(Knight, self).__init__()
        self.ways = []
        self.step = [-1, -2, 1, 2]
        self.sign_paint_tile = Knight.sign_level

    def activate_tile(self, player, unit):
        """Ход конём"""
        super(Knight, self).activate_tile(player, unit)
        self.fight_on_tile(player, unit)
        self.unit = unit
        self.calculate_coord(unit)
        unit.y_coord, unit.x_coord = self.change_coord(player, unit)
        self.move_unit(player, unit)

    def set_way(self, unit, choose):
        """Установить направление движения юнита"""
        unit.y_coord, unit.x_coord = self.ways[choose - 1]

    def calculate_coord(self, unit):
        """Расчёт координат куда можно ходить"""
        for i in self.step:
            for j in self.step:
                if abs(i) == abs(j):
                    continue
                elif 1 <= unit.y_coord + i <= self.map.dimension_map - 2 \
                        and 1 <= unit.x_coord + j <= self.map.dimension_map - 2:
                    self.ways.append([unit.y_coord + i, unit.x_coord + j])
        self.ways.sort()

    def change_coord(self, player, unit):
        self.map.print_map(self.ways)
        self.send_and_get_message(player.color, self.massage_choose_way(unit))
        if unit in self.map.map[unit.y_coord][unit.x_coord]:
            self.map.del_unit_from_cell(unit)
        return self.ways[int(self.server.gotten_message) - 1]

    def move_unit(self, player, unit):
        """Передвинуть юнита"""
        self.ways = []
        self.map.insert_unit_in_cell(unit)
        if False in self.map.map[unit.y_coord][unit.x_coord]:
            self.map.open_cell(player, unit)
            self.map.activate_cell(player, unit)
        else:
            self.map.activate_cell(player, unit)

    def massage_choose_way(self, unit):
        """Спросить у игрока, куда будет ходить"""
        data = unit.name + ' может сделать ход конём:'
        count = 1
        answer = []
        for way in self.ways:
            data += '\n\t' + str(count) + ') Y = ' + str(way[0]) + 'X = ' + str(way[1])
            count += 1
        data += '\nКуда будете ходить(введите порядковый номер): '
        for count in range(1, len(self.ways) + 1):
            answer.append(str(count))
        return data, answer

    def print_tile(self, y, x, level, backlight):
        units = self.search_unit(y, x)
        color = self.calculate_color(y, x)
        backlight_color = self.set_backlight_color(backlight)
        if level == 2:
            text = color + backlight_color + self.sign_paint_tile[level].format(units[0]) + Style.RESET_ALL
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
            print(text, end='')
