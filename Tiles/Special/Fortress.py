from colorama import Style

from Tiles.Tile import Tile


class Fortress(Tile):
    """Класс форт"""
    name = "Форт"
    sign = 'F'

    sign_level = {1: ' _____ _____ ',
                  2: '|           |',
                  3: '|    ФОРТ   |',
                  4: '| {0}  {1}  {2}   |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Fortress, self).__init__()
        self.sign_paint_tile = Fortress.sign_level

    def activate_tile(self, player, unit):
        """Активировать форт"""
        super(Fortress, self).activate_tile(player, unit)
        if len(unit.backpack) > 0:
            unit.drop_coin()
        self.send_and_get_message(player.color, self.massage_welcome(unit))

    def massage_welcome(self, unit):
        """Сообщение игроку что он попал в форт"""
        data = '\n{0} поселился в форте и сейчас отдыхает\n\t' \
               'Нижмите ENTER чтобы продолжить'.format(unit.name)
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        units = self.search_unit(y, x)
        color = self.calculate_color(y, x)
        backlight_color = self.set_backlight_color(backlight)
        count_coin = self.search_coin(y, x)
        if level == 4:
            text = color + backlight_color + self.sign_paint_tile[level].format(units[0], units[1],
                                                                                units[2]) + Style.RESET_ALL
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
            print(text, end='')
