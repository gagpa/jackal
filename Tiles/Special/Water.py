from colorama import Style

from Tiles.Tile import Tile
from Units.Unit import Unit


class Water(Tile):
    name = 'Вода'
    sign = '~'
    sign_level = {1: ' ~ ~ ~ ~ ~ ~ ',
                  2: '~ ~ ~ ~ ~ ~ ~',
                  3: ' ~ ~ ~ ~ ~ ~ ',
                  4: '~ ~{0}~{1}~{2}~ ~ ~',
                  5: ' ~ ~ ~ ~ ~ ~ '}

    def __init__(self):
        super(Tile, self).__init__()
        self.sign_paint_tile = Water.sign_level

    def activate_tile(self, player, unit):
        """Ограничение по передвижению"""
        super(Water, self).activate_tile(player, unit)
        self.map.save_coord_in_history(unit)
        self.fight_on_tile(player, unit)
        if unit in player.vehicle:
            self.search_swimmer(player, unit)
        elif len(unit.backpack) > 0 and unit.type in Tile.alive_creature:
            unit.drop_coin()

    def search_swimmer(self, player, ship):
        print(ship)
        tile, status, *other = self.map.map[ship.y_coord][ship.x_coord]
        for pirate in other:
            if pirate.type == Tile.alive_creature:
                pirate.take_on_board(ship)

    def search_ship(self, y, x):
        tile, status, *other = self.map.map[y][x]
        for unit in other:
            if unit.type == Tile.vehicle:
                return unit
        return False

    def print_tile(self, y, x, level, backlight):
        self.add_map()
        units = self.search_unit(y, x)
        ship = self.search_ship(y, x)
        color = self.calculate_color(y, x)
        backlight_color = self.set_backlight_color(backlight)
        if ship is False:
            if level == 4:
                text = color + backlight_color + self.sign_paint_tile[level].format(units[0], units[1],
                                                                                    units[2]) + Style.RESET_ALL
                print(text, end='')
            else:
                text = color + backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
                print(text, end='')
        else:
            text = color + backlight_color + ship.sign_paint_tile[level] + Style.RESET_ALL
            print(text, end='')
