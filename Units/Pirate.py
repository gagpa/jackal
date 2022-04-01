from Drops.Coin import Coin
from .Unit import Unit


class Pirate(Unit):
    """Под класс пират"""

    names_of_possible_drop = Coin.name

    def __init__(self, player, index):
        """Переменный взаимодействия с картой"""
        super(Pirate, self).__init__(player)
        self.life = True
        self.skip_time = 0
        self.in_sex = False
        self.backpack_max = 1
        self.sign = str(index)
        self.index = index
        self.type = 'Пират'
        self.name = self.type + ' ' + str(self.index)
        self.way = None

    # Блок взаимодействия с плитками
    def dead(self):
        """Умереть"""
        self.life = False
        self.add_map()
        if self in self.map.map[self.y_coord][self.x_coord]:
            self.map.del_unit_from_cell(self)
        self.y_coord = None
        self.x_coord = None
        self.player.dead_creature.append(self)
        self.player.alive_creature.remove(self)

    def rise_unit(self, unit):
        """Воскресить юнита"""
        self.add_map()
        self.in_sex = False
        unit.life = True
        unit.y_coord = self.y_coord
        unit.x_coord = self.x_coord
        self.map.insert_unit_in_cell(unit)
        self.player.dead_creature.remove(unit)
        self.player.alive_creature.append(unit)

    def sex_with_aborigine(self, skip_time):
        self.in_sex = True
        self.skip_time = skip_time

    def drop_coin(self):
        """Выкинуть монетку"""
        self.add_map()
        coin, *_ = self.backpack
        self.backpack.remove(coin)
        if len(self.map.history_x_coord) == 0:
            coin.y_coord, coin.x_coord = self.y_coord, self.x_coord
        else:
            coin.y_coord, coin.x_coord = self.map.history_y_coord[0], self.map.history_x_coord[0]
        self.map.insert_unit_in_cell(coin)

    def put_coin(self, coin):
        """Поднять монету"""
        self.backpack.append(coin)

    def check_coin(self):
        """Проверить наличие монетки"""
        self.add_map()
        tile, status, *drops = self.map.map[self.y_coord][self.x_coord]
        for drop in drops:
            if drop.name == Coin.name:
                return True, drop
        return False, None

    def check_limit_backpack_and_put(self, drop):
        """Проверить вместится предмет в рюкзакак"""
        if len(self.backpack) < self.backpack_max:
            self.put_coin(drop)
            if drop in self.map.map[self.y_coord][self.x_coord]:
                self.map.del_unit_from_cell(drop)

    # Блок передвижения по карте
    def take_off_board(self, ship):
        """Высадить юнита"""
        ship.take_off_board(self)

    def take_on_board(self, ship):
        """Зайти на борт"""
        ship.take_on_board(self)

    def choose_way(self):
        """Вывести возможные пути"""
        return 'r/l/d/u'

    def reverse_way(self):
        """Изменить направление ходьбы на противоложенный"""
        self.way = Unit.revers_way[self.way]

    # Блок сообщений юнита
    def massage_in_the_trap(self):
        """Сообщить что юнит не может двигаться"""
        data = '{0}: Я в ловушке, Капитан, и мне нужна помощь!' \
               '\nВыебрите другого юнита.\n\t' \
               'Нажмите ENTER чтобы продолжить'.format(self.name)
        return data
