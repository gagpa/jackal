from Tiles.Tile import Tile


class Obstacle(Tile):
    """Класс препятсвие"""
    obstacle_dict = {'Джунгли': 2,
                     'Пустыня': 3,
                     'Болото': 4,
                     'Холмы': 5}

    def __init__(self):
        super(Obstacle, self).__init__()
        self.name = None
        self.obstacle = []

    def activate_tile(self, player, unit):
        """Активировать пропуск хода"""
        self.add_map()
        self.add_server()
        self.fight_on_tile(player, unit)

        if unit.under_effect is True:
            self.move_unit_in_obstacle(player, unit)
        else:
            self.add_unit_in_obstacle(player, unit)

    def create_obstacle(self, kind):
        """Создать препятсвие"""
        for dimension in range(Obstacle.obstacle_dict[kind]):
            self.obstacle.append([])

    def add_unit_in_obstacle(self, player, unit):
        """Добавить юнита в препятсвие"""
        unit.change_under_effect()
        self.obstacle[0].append(unit)
        self.check_enemy_in_same_obstacle_level(player, unit, 0)

    def move_unit_in_obstacle(self, player, unit):
        """Передвинуть юнита из препятсвия"""
        place = self.give_unit_place(unit)
        if place == len(self.obstacle) - 1:
            """Выйти из препятсвия"""
            unit.change_under_effect()
            self.send_and_get_message(player.color, self.message_exit(unit))
            unit.way = self.server.gotten_message
            self.obstacle[-1].remove(unit)
            self.set_way_unit(player, unit)
        else:
            self.obstacle[place].remove(unit)
            self.obstacle[place + 1].append(unit)
            self.check_enemy_in_same_obstacle_level(player, unit, place + 1)
            self.send_and_get_message(player.color, self.message_in_obstacle(unit))

    def set_way_unit(self, player, unit):
        """Установить направление движения"""
        unit.calculate_ways()
        self.map.print_map(unit.ways)
        unit.ways = []
        # Спрашиваем у игрока куда он будет ходить
        self.server.send_message(player.color, self.message_choose_way(unit))
        # Получаем ответ куда он будет ходить
        self.server.get_message()
        # Выделяем напрваление движение юнита
        unit.way = self.server.gotten_message
        # Передвигаем юнита на карте
        self.map.action_on_map(player, unit)

    def give_unit_place(self, unit):
        """Вернуть индекс ячейки в которой находится персонаж"""
        for index, cell in enumerate(self.obstacle):
            if unit in cell:
                return index

    def check_enemy_in_same_obstacle_level(self, player, unit, place):
        """Проверить врага на своём уровне препятсвия"""
        cell = self.map.map[unit.y_coord][unit.x_coord]
        if len(cell) > 4:
            another_unit = cell[-2]
            if another_unit not in player.units:
                if another_unit in self.obstacle[place]:
                    self.fight_on_tile(player, unit)
                    self.obstacle[place].remove(another_unit)

    def message_choose_way(self, unit):
        """Вопрос игроку, куда будет ходить?"""
        data = 'Выберите куда будете ходите: {0}'.format(unit.choose_way())
        answer = unit.choose_way()
        return data, answer

    def message_in_obstacle(self, unit):
        """Сообщение сколько он прошёл"""
        late_way = str(len(self.obstacle) - self.obstacle.index([unit]) - 1)
        data = '{0} сейчас находится в {1}. Ему осталось пройти {2}.' \
               '\n\tНажмите Enter, чтобы продолжить!'\
            .format(unit.name, self.name, late_way)
        answer = Tile.answer
        return data, answer

    def message_exit(self, unit):
        """Сообщение что юнит вышел"""
        data = '{0} вышел из {1}. Теперь он может продолжить свою ' \
               'охоту на сокровища.\n\tНажмите Enter, чтобы продолжить!'\
            .format(unit.name, self.name)
        answer = Tile.answer
        return data, answer

    def search_unit(self, y, x):
        units = []
        for unit in self.obstacle:
            if unit == []:
                units.append(' ')
            elif unit[0].type == Tile.alive_creature:
                sign_colored = self.baclight_unit_with_coin(unit[0])
                units.append(sign_colored)
        return units
