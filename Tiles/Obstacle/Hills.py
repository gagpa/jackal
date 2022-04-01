from colorama import Style

from Tiles.Obstacle.Obstacle import Obstacle


class Hills(Obstacle):
    """"Класс горы"""
    sign = '&'
    name = 'Холмы'

    sign_level = {1: ' _____ _____ ',
                  2: '|  Холмы   {0}|',
                  3: '|  ({0}) ({1})  |',
                  4: '|({0}) ({1}) ({2})|',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Hills, self).__init__()
        self.name = Hills.name
        self.create_obstacle(self.name)
        self.sign_paint_tile = Hills.sign_level

    def print_tile(self, y, x, level, backlight):
        units = self.search_unit(y, x)
        color = self.calculate_color(y, x)
        backlight_color = self.set_backlight_color(backlight)
        count_coin = self.search_coin(y, x)
        if level == 2:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(count_coin + color + backlight_color) + Style.RESET_ALL
            print(text, end='')
        elif level == 3:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(units[1], units[3])
            print(text, end='')
        elif level == 4:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(units[0], units[2], units[4])
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
            print(text, end='')
