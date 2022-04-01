from colorama import Style

from Tiles.Tile import Tile


class Trap(Tile):
    """Класс ловушки"""
    name = 'Ловушка'
    sign = 'X'
    sign_level = {1: ' _____ _____ ',
                  2: '| Ловушка  {0}|',
                  3: '| |VVVVVVV| |',
                  4: '|   {0}   {1}   |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Trap, self).__init__()
        self.trap = None
        self.sign_paint_tile = Trap.sign_level

    def activate_tile(self, player, unit):
        """Активировать ловушку"""
        super(Trap, self).activate_tile(player, unit)
        self.fight_on_tile(player, unit)
        units = self.get_units(unit.y_coord, unit.x_coord)
        if len(units) == 1:
            # Попал в ловушку
            self.trap = unit
            unit.under_effect_on()
            self.send_and_get_message(player.color, self.message_trap(unit))
        elif self.trap is not None:
            # Спасти из ловушки
            self.send_and_get_message(player.color, self.message_save(unit))
            self.trap.under_effect_off()
            self.trap = None

    def message_trap(self, unit):
        """Сообщить игроку что юнит попал в ловушку"""
        data = '\n{0} в ловушке и ему нужна помощь!\n\t' \
               'Нижмите ENTER чтобы продолжить'.format(unit.name)
        answer = Tile.answer
        return data, answer

    def message_save(self, unit):
        """Сообщить что юнит спас своего напарника"""
        data = '\n{0} спас своего напарниа {1}\n\t' \
               'Нижмите ENTER чтобы продолжить'.format(unit.name, self.trap.name)
        answer = Tile.answer
        return data, answer

    def get_units(self, y, x):
        units = []
        tile, status, *other = self.map.map[y][x]
        for unit in other:
            if unit.type in Tile.alive_creature:
                self.baclight_unit_with_coin(unit)
                units.append(unit)
        return units

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
                .format(units[0], units[1]) + Style.RESET_ALL
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
            print(text, end='')
