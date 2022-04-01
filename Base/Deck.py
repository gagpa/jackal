from random import shuffle

from Tiles.Move.Arrow import Arrow
from Tiles.Move.Balloon import Balloon
from Tiles.Move.Cannon import Cannon
from Tiles.Move.Crocodile import Crocodile
from Tiles.Move.Ice import Ice
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
from Tiles.Special.Ogre import Ogre
from Tiles.Special.Trap import Trap
from Tiles.Special.Water import Water
from Tiles.Treasure.Treasure1 import Treasure1
from Tiles.Treasure.Treasure2 import Treasure2
from Tiles.Treasure.Treasure3 import Treasure3
from Tiles.Treasure.Treasure4 import Treasure4
from Tiles.Treasure.Treasure5 import Treasure5


class Deck:
    """Класс колоды"""
    # Картеж из всех плиток
    all_tile = (
        (Arrow, 21),
        (Knight, 2),
        (Jungle, 5),
        (Desert, 4),
        (Swamp, 2),
        (Hills, 1),
        (Ice, 6),
        (Trap, 3),
        (Cannon, 2),
        (Barrel, 4),
        (Crocodile, 4),
        (Ogre, 1),
        (Balloon, 2),
        (Plane, 1),
        (Fortress, 2),
        (FortressWithAborigine, 1),
        (Treasure1, 5),
        (Treasure2, 5),
        (Treasure3, 3),
        (Treasure4, 2),
        (Treasure5, 1),
    )

    tile_simple_move = (Ground.name, Water.name, Jungle.name, Desert.name,
                        Swamp.name, Hills.name, Trap.name,
                        Barrel.name, Plane.name, Fortress.name, FortressWithAborigine.name,
                        Treasure1.name, Treasure2.name, Treasure3.name, Treasure4.name,
                        Treasure5.name, Ice.name)

    tile_complex_move = (Arrow.name, Knight.name)

    def __init__(self, dimension_map):
        """Колода на игру"""
        self.deck = []
        # Размер карты и колоды
        self.dimension_map = dimension_map
        self.quantity_tile = self.dimension_map ** 2
        # Счётчик карт
        self.count = 0
        self.all_coin = 0
        self.create_deck()

    # Блок создания колоды
    def create_deck(self):
        """Создание колоды"""
        for tile in Deck.all_tile:
            for quantity in range(tile[1]):
                self.deck.append(tile[0])
                self.count += 1
        self.add_ground()
        self.shuffle_deck()
        self.add_water()
        self.calculate_all_coin()

    def add_ground(self):
        """Добавление равнины до полноты острова"""
        quantity_ground = (self.dimension_map - 2) ** 2 - 4 - self.count
        for quantity in range(quantity_ground):
            self.deck.append(Ground)

    def add_water(self):
        """Добавление воды вокруг острова"""
        quantity_water = self.quantity_tile - ((self.dimension_map - 2) ** 2 - 4)
        for quantity in range(quantity_water):
            self.deck.append(Water())

    def shuffle_deck(self):
        """Перемешивает колоду"""
        shuffle(self.deck)

    def calculate_all_coin(self):
        """Расчёт всех монет"""
        for tile in self.deck:
            try:
                self.all_coin += tile.quantity_coin
            except AttributeError:
                continue
