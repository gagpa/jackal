from colorama import Style

from Tiles.Tile import Tile


class Ogre(Tile):
    """Класс огра"""
    name = 'Огр'
    sign = 'O'
    sign_level = {1: ' _____ _____ ',
                  2: '|           |',
                  3: '|    ОГР    |',
                  4: '|   o,..,o  |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Ogre, self).__init__()
        self.sign_paint_tile = Ogre.sign_level

    def activate_tile(self, player, unit):
        """Активировать огра"""
        super(Ogre, self).activate_tile(player, unit)
        self.ogre_kill_unit(unit)
        self.send_and_get_message(player.color, self.message_by_ogre())

    def ogre_kill_unit(self, unit):
        """Огр убивает юнита"""
        if len(unit.backpack) > 0:
            unit.drop_coin()
        unit.dead()

    def message_by_ogre(self):
        """Сообщение от огра"""
        data = Ogre.name + ': Не лезьте ко мне жалкие люди!!!'
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        backlight_color = self.set_backlight_color(backlight)
        text = backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
        print(text, end='')
