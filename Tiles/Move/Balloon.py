from colorama import Style

from Tiles.Tile import Tile


class Balloon(Tile):
    """Класс воздушный шар"""
    name = 'Воздушный шар'
    sign = 'B'

    sign_level = {1: ' _____ _____ ',
                  2: '|           |',
                  3: '| Воздушный |',
                  4: '|    шар    |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Balloon, self).__init__()
        self.sign_paint_tile = Balloon.sign_level

    def activate_tile(self, player, unit):
        """Активация воздушного шара"""
        super(Balloon, self).activate_tile(player, unit)
        self.transport_unit_to_ship(player, unit)
        self.send_and_get_message(player.color, self.message_from_board(unit))

    def transport_unit_to_ship(self, player, unit):
        """Переместить юнита на корабль"""
        ship = self.return_ship(player)
        unit.take_on_board(ship)
        unit.y_coord, unit.x_coord = ship.y_coord, ship.x_coord

    def return_ship(self, player):
        """Вывести объект корабля"""
        return player.units[0]

    def message_from_board(self, unit):
        """Сообщение что юнит отправился на корабль"""
        data = '{0} пролетает над островом на воздушном шаре\n\t' \
               'Нажмите ENTER чтобы продолжить'.format(unit.name)
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        backlight_color = self.set_backlight_color(backlight)
        text = backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
        print(text, end='')
