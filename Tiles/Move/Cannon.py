from random import randint

from colorama import Style

from Tiles.Tile import Tile


class Cannon(Tile):
    """Класс пушки"""
    name = 'Пушка'
    sign = '!'

    sign_level_right = {1: ' _____ _____ ',
                        2: '|         + |',
                        3: '| ======)+ +|',
                        4: '| /O\       |',
                        5: '|_____ _____|'}

    sign_level_left = {1: ' _____ _____ ',
                       2: '| +         |',
                       3: '|+ +(====== |',
                       4: '|       /O\ |',
                       5: '|_____ _____|'}

    sign_level_up = {1: ' _____ _____ ',
                     2: '|           |',
                     3: '|   ПУШКА   |',
                     4: '|   ВВЕРХ   |',
                     5: '|_____ _____|'}

    sign_level_dawn = {1: ' _____ _____ ',
                       2: '|           |',
                       3: '|   ПУШКА   |',
                       4: '|     ВНИЗ  |',
                       5: '|_____ _____|'}

    sign_level = {1: sign_level_right,
                  2: sign_level_left,
                  3: sign_level_up,
                  4: sign_level_dawn}

    def __init__(self):
        super(Cannon, self).__init__()
        self.choose = randint(1, 4)
        self.sign_paint_tile = Cannon.sign_level[self.choose]

    def activate_tile(self, player, unit):
        """ВЫстерл из пушки"""
        super(Cannon, self).activate_tile(player, unit)
        unit.way = self.choose_way()
        self.choose_way()
        self.move_from_cannon(player, unit)
        self.send_and_get_message(player.color, self.message_from_cannon(unit))

    def choose_way(self):
        """Случайный вбор направления выстрела"""
        return Tile.way_number_to_letter[self.choose]

    def move_from_cannon(self, player, unit):
        """Полёт из пушки"""
        if unit in self.map.map[unit.y_coord][unit.x_coord]:
            self.map.del_unit_from_cell(unit)
        while 0 < unit.y_coord < self.map.dimension_map - 1 and 0 < unit.x_coord < self.map.dimension_map - 1:
            self.map.change_unit_coord(unit)
        self.map.insert_unit_in_cell(unit)
        cell = self.map.map[unit.y_coord][unit.x_coord]
        # Проверяем наличие других юнитов в клетке
        if len(cell) > 3:
            another_unit = cell[-2]
            if another_unit not in player.units:
                if another_unit.type == Tile.vehicle:
                    unit.dead()
                else:
                    self.map.activate_cell(player, unit)
            else:
                if another_unit.type == Tile.vehicle:
                    unit.take_on_board(another_unit)
        else:
            self.map.activate_cell(player, unit)

    def message_from_cannon(self, unit):
        """Сообщение из пушки"""
        data = '{0} полетел из пушки {1} в воду.'.format(unit.name, Tile.way_latter_to_word[unit.way])
        if unit.life is False:
            data += 'Но он разбился об корабль'
        data += '\n\tНижмите ENTER чтобы продолжить'
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        backlight_color = self.set_backlight_color(backlight)
        text = backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
        print(text, end='')
