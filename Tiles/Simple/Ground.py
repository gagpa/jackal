from colorama import Style

from Tiles.Tile import Tile


class Ground(Tile):
    """Класс равнины"""
    sign = 'V'
    name = 'Равнина'

    sign_level = {1: ' _____ _____ ',
                  2: '|  Равнина {0}|',
                  3: '|           |',
                  4: '| {0}  {1}  {2}   |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Tile, self).__init__()
        self.name = Ground.name
        self.sign_paint_tile = Ground.sign_level

    def activate_tile(self, player, unit):
        super(Ground, self).activate_tile(player, unit)
        self.fight_on_tile(player, unit)

    def print_tile(self, y, x, level, backlight):
        units = self.search_unit(y, x)
        color = self.calculate_color(y, x)
        backlight_color = self.set_backlight_color(backlight)
        count_coin = self.search_coin(y, x)
        if level == 2:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(count_coin + color + backlight_color) + Style.RESET_ALL
            print(text, end='')
        elif level == 4:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(units[0], units[1], units[2]) + Style.RESET_ALL
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] \
                   + Style.RESET_ALL
            print(text, end='')
