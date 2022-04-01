from colorama import Style

from .Treasure import Treasure


class Treasure2(Treasure):
    """Сокровище 2"""
    name = 'Сокровище'
    sign = 'X'
    quantity_coin = 2
    sign_level = {1: ' _____ _____ ',
                  2: '| Сокровище{0}|',
                  3: '|    LVL 2  |',
                  4: '| {0}  {1}  {2}   |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Treasure2, self).__init__()
        self.quantity_coin = Treasure2.quantity_coin
        self.sign_paint_tile = Treasure2.sign_level

    def activate_tile(self, player, unit):
        super(Treasure2, self).activate_tile(player, unit)
        if self.open is False:
            self.open = True
            self.generate_coins(unit)
            self.send_and_get_message(player.color, self.massage_find_treasure(unit))
        print(self.map.map[unit.y_coord][unit.x_coord])

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
