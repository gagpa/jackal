from colorama import Style

from Tiles.Tile import Tile


class Crocodile(Tile):
    """Класс крокодила"""
    name = 'Крокодил'
    sign = '<'

    sign_level = {1: ' _____ _____ ',
                  2: '|           |',
                  3: '| Кхаа!!!   |',
                  4: '|   КРОКОДИЛ|',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Crocodile, self).__init__()
        self.sign_paint_tile = Crocodile.sign_level

    def activate_tile(self, player, unit):
        """Активировать отмену хода"""
        super(Crocodile, self).activate_tile(player, unit)
        self.back_turn(player, unit)
        self.send_and_get_message(player.color, self.message_crocodile(unit))
        self.map.activate_cell(player, unit)

    def back_turn(self, player, unit):
        """Откатить ход"""
        if unit in self.map.map[unit.y_coord][unit.x_coord]:
            self.map.del_unit_from_cell(unit)
        unit.y_coord, unit.x_coord = self.turn_back_coord()
        if self.check_ship(player, unit) is True:
            unit.take_on_board(player.vehicle[0])
        else:
            self.map.insert_unit_in_cell(unit)

    def check_ship(self, player, unit):
        _, _, *units = self.map.map[unit.y_coord][unit.x_coord]
        for unit in units:
            if unit in player.vehicle:
                return True
        return False

    def turn_back_coord(self):
        """Вернуть координаты из начала хода"""
        history_y, history_x = self.map.get_history_coord()
        check = 0
        return history_y[check], history_x[check]

    def message_crocodile(self, unit):
        """Сообщить что пират испугался крокодила"""
        data = '{0}: Мой Капитан! Тут крокодил! Лучше обходить его стороной.\n\t' \
               'Нажмите ENTER чтобы продолжить'.format(unit.name)
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        backlight_color = self.set_backlight_color(backlight)
        text = backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
        print(text, end='')
