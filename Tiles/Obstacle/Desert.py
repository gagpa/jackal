from colorama import Style

from Tiles.Obstacle.Obstacle import Obstacle


class Desert(Obstacle):
    """"Класс пустыня"""
    sign = '$'
    name = 'Пустыня'
    sign_level = {1: ' _____ _____ ',
                  2: '| Пустыня  {0}|',
                  3: '| ({0})   ({1}) |',
                  4: '|    ({0})    |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Desert, self).__init__()
        self.name = Desert.name
        self.create_obstacle(self.name)
        self.sign_paint_tile = Desert.sign_level

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
                .format(units[0], units[2])
            print(text, end='')
        elif level == 4:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(units[1]) + Style.RESET_ALL
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] \
                   + Style.RESET_ALL
            print(text, end='')
