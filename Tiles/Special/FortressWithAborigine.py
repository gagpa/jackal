from colorama import Style

from Tiles.Special.Fortress import Fortress


class FortressWithAborigine(Fortress):
    """Класс форта с аборигеном"""
    name = 'Форт с аборигеном'
    sign = 'A'
    answer = {'y': True,
              'n': False}

    sign_level = {1: ' _____ _____ ',
                  2: '|    ФОРТ   |',
                  3: '| c жителем |',
                  4: '| {0}  {1}  {2}   |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(FortressWithAborigine, self).__init__()
        self.skip_time = 1
        self.sign_paint_tile = FortressWithAborigine.sign_level

    def activate_tile(self, player, unit):
        """Активировать форт с аборигеном"""
        super(FortressWithAborigine, self).activate_tile(player, unit)
        self.map.print_map()
        answer = self.rise_dead_unit(player)
        if answer is True:
            unit.sex_with_aborigine(self.skip_time)

    def rise_dead_unit(self, player):
        check_dead_unit = self.search_dead_unit(player)
        if check_dead_unit is True:
            self.send_and_get_message(player.color, self.massage_rise())
            answer = FortressWithAborigine.answer[self.server.gotten_message]
            return answer
        else:
            answer = False
            return answer

    def search_dead_unit(self, player):
        """Проверить наличие мёртвых юнитов"""
        for unit in player.units:
            if unit.life is False:
                return True
        return False

    def massage_rise(self):
        """Сообщить игроку что он может воскресить юнита"""
        data = 'У вас есть мёртвый.\nХотите воскресить его?'
        answer = 'y/n'.split('/')
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
