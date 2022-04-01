from random import randint

from colorama import Style

from Tiles.Tile import Tile


class Arrow(Tile):
    """Класс прямой стрелки"""
    name = 'Стрелка'
    sign = '^'

    sign_level_up = {1: ' _____ _____ ',
                     2: '|  ^     ^  |',
                     3: '|  |     |  |',
                     4: '|  |     |  |',
                     5: '|_____ _____|'}

    sign_level_dawn = {1: ' _____ _____ ',
                       2: '|  |     |  |',
                       3: '|  |     |  |',
                       4: '|  V     V  |',
                       5: '|_____ _____|'}

    sign_level_right = {1: ' _____ _____ ',
                        2: '|           |',
                        3: '| --------> |',
                        4: '| --------> |',
                        5: '|_____ _____|'}

    sign_level_left = {1: ' _____ _____ ',
                       2: '|           |',
                       3: '| <-------- |',
                       4: '| <-------- |',
                       5: '|_____ _____|'}

    sign_level = {1: sign_level_right,
                  2: sign_level_left,
                  3: sign_level_up,
                  4: sign_level_dawn}

    def __init__(self):
        # Направление стрелки
        super(Tile, self).__init__()
        self.choose = randint(1, 4)
        self.count = 0
        self.sign_paint_tile = Arrow.sign_level[self.choose]

    def activate_tile(self, player, unit):
        """Движение по стрелки"""
        super(Arrow, self).activate_tile(player, unit)
        self.unit = unit
        unit.way = self.choose_way()
        if self.check_infinity_loop(unit) is True:
            unit.dead()
        else:
            self.map.action_on_map(player, unit)

    def choose_way(self):
        """Дать направление стрелки"""
        return Tile.way_number_to_letter[self.choose]

    def check_infinity_loop(self, unit):
        if len(self.map.history_y_coord) > 5:
            history = self.map.create_list_history()
            if [unit.y_coord, unit.x_coord] in history:
                return True
        return False

    def message_move(self, unit):
        """Сообщение что юнит передвинулся по стрелки"""
        data = '{0} передвинулся по стрелки {1}' \
            .format(unit.name, Tile.way_latter_to_word[unit.way])
        answer = self.unit.choose_way()
        return data, answer

    def print_tile(self, y, x, level, backlight):
        backlight_color = self.set_backlight_color(backlight)
        text = backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
        print(text, end='')
