from colorama import Style

from Tiles.Move.Arrow import Arrow
from Tiles.Move.Knight import Knight
from Tiles.Move.Plane import Plane
from Tiles.Obstacle.Desert import Desert
from Tiles.Obstacle.Hills import Hills
from Tiles.Obstacle.Jungle import Jungle
from Tiles.Obstacle.Swamp import Swamp
from Tiles.Simple.Ground import Ground
from Tiles.Special.Barrel import Barrel
from Tiles.Special.Fortress import Fortress
from Tiles.Special.FortressWithAborigine import FortressWithAborigine
from Tiles.Special.Trap import Trap
from Tiles.Special.Water import Water
from Tiles.Tile import Tile
from Tiles.Treasure.Treasure1 import Treasure1
from Tiles.Treasure.Treasure2 import Treasure2
from Tiles.Treasure.Treasure3 import Treasure3
from Tiles.Treasure.Treasure4 import Treasure4
from Tiles.Treasure.Treasure5 import Treasure5


class Ice(Tile):
    """Класс лёд"""
    name = 'Лёд'
    sign = '*'
    tile_simple_move = (Ground.name, Water.name, Jungle.name, Desert.name,
                        Swamp.name, Hills.name, Trap.name,
                        Barrel.name, Plane.name, Fortress.name, FortressWithAborigine.name,
                        Treasure1.name, Treasure2.name, Treasure3.name, Treasure4.name,
                        Treasure5.name, name)
    tile_complex_move = (Arrow.name, Knight.name)

    sign_level = {1: ' _____ _____ ',
                  2: '|  // // // |',
                  3: '|// //  //  |',
                  4: '|    ЛЁД    |',
                  5: '|_____ _____|'}

    def __init__(self):
        """Лёд повторяет движение"""
        super(Ice, self).__init__()
        self.tile = None
        self.sign_paint_tile = Ice.sign_level

    def activate_tile(self, player, unit):
        """Повторить предыдущее движение"""
        super(Ice, self).activate_tile(player, unit)
        self.calculate_tile()
        # self.server.send_data(player, self.massage_choose_way(unit))
        tile = self.calculate_tile()
        if tile.name in Ice.tile_complex_move:
            tile.activate_tile(player, unit)
        else:
            self.map.action_on_map(player, unit)

    def calculate_tile(self):
        """Вычсисляем предыдущие координаты и плитку"""
        history_y, history_x = self.map.get_history_coord()
        check = -1
        while self.map.map[history_y[check]][history_x[check]][0].name == Ice.name:
            check -= 1
        return self.map.map[history_y[check]][history_x[check]][0]

    def massage_choose_way(self, unit):
        """Отправить сообщение что юнит подскользнулся"""
        data = '{0} подскользнулся!\n\t' \
               'Нижмите ENTER чтобы продолжить'.format(unit.name)
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        backlight_color = self.set_backlight_color(backlight)
        text = backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
        print(text, end='')
