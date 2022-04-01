from colorama import Style

from Tiles.Tile import Tile


class Barrel(Tile):
    """Класс бочки с ромом"""
    name = 'Бочка рома'
    sign = '?'

    sign_level = {1: ' _____ _____ ',
                  2: '|    Бочка {0}|',
                  3: '|    рома!  |',
                  4: '| {0}  {1}  {2}   |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Barrel, self).__init__()
        self.skip_time = 1
        self.sign_paint_tile = Barrel.sign_level

    def activate_tile(self, player, unit):
        """Активировать бочку с ромом"""
        super(Barrel, self).activate_tile(player, unit)
        self.fight_on_tile(player, unit)
        if unit.under_effect is False:
            unit.under_effect_on()
            unit.skip_time = self.skip_time
            self.send_and_get_message(player.color, self.message_drunk(unit))
        else:
            unit.skip_time -= 1
            if unit.skip_time == 0:
                self.send_and_get_message(player.color, self.message_sober_up(unit))
                unit.under_effect_off()

    def message_drunk(self, unit):
        """Сообщить игроку что его юнит выпил ром"""
        data = '{0} выпил ром и теперь пропускает {1} ходов\n\t' \
               'Нижмите ENTER чтобы продолжить'.format(unit.name, self.skip_time)
        answer = Tile.answer
        return data, answer

    def message_sober_up(self, unit):
        data = unit.name + ' протрезвел!\n\t' \
               'Нижмите ENTER чтобы продолжить'
        answer = Tile.answer
        return data, answer

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
