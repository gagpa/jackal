import time

from Drops.Coin import Coin
from Tiles.Tile import Tile


class Treasure(Tile):
    """Класс скоровищ"""
    name = 'Сокровище'
    sign = 'T'

    def __init__(self):
        super(Treasure, self).__init__()
        self.open = False
        self.quantity_coin = None

    def activate_tile(self, player, unit):
        super(Treasure, self).activate_tile(player, unit)
        self.fight_on_tile(player, unit)

    def generate_coins(self, unit):
        """Генерирует монетки"""
        count = 0
        for coin in range(self.quantity_coin):
            count += 1
            coin = Coin(unit.y_coord, unit.x_coord)
            self.map.insert_unit_in_cell(coin)

    def massage_find_treasure(self, unit):
        """Сообщения что юнит нашёл сокровище"""
        data = '{0} нащёл сокровище с {1} монетами'.format(unit.name, self.quantity_coin)
        answer = Tile.answer
        return data, answer
