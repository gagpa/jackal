import time
from colorama import Fore

from Base.Map import Map
from Server.Server import Server


class Turns:
    """Класс игрового хода"""

    def __init__(self):

        self.map = None
        self.server = None
        self.unit = None

    def add_map(self):
        """Подгрузка синглтон карты"""
        self.map = Map()

    def add_server(self):
        """Подгрузка синглтон сервера"""
        self.server = Server()

    def activate_all_singleton(self):
        """Активация всех синглтонов"""
        self.add_map()
        self.add_server()

    def do_round(self, party):
        """Осуществить ход"""
        self.activate_all_singleton()
        self.map.print_map()
        # Проверка на глобальный пропуск
        if self.check_global_skip_turn(party) is False:
            self.set_unit(party)
            # Проверка типа юнита(живые существа)
            if self.unit in party.alive_creature:
                self.turn_alive_creature(party)
            # Проверка типа юнита(транспорт)
            elif self.unit in party.vehicle:
                self.turn_vehicle(party)
        # Если юнит воскрешает своего напарника
        elif self.unit.in_sex is True:
            self.unit.rise_unit(self.search_dead_unit(party))
        self.map.clean_history()

        # Условие победы
        if party.count > self.map.all_coin // 2:
            exit()

    def turn_alive_creature(self, party):
        """Ход живых существ"""
        self.check_coin_for_unit(party)
        if self.unit.under_effect is True:
            self.map.activate_cell(party, self.unit)
        # Выходим с корабля
        elif self.check_on_board(party) is True:
            self.unit.way = party.vehicle[0].take_off_board(self.unit, 13)
            self.map.action_on_map(party, self.unit)
        # Если юниту ничего не мешает
        else:
            self.set_way_unit(party)

    def turn_vehicle(self, party):
        """Ход транспорта"""
        self.set_way_unit(party)
        self.unit.board_change_coord()

    def check_on_board(self, party):
        if self.unit in party.vehicle[0].board:
            return True
        return False

    def set_unit(self, party):
        """Дать ход юниту"""
        # Спрашиваем у игрока каким юнитом будет ходить
        self.server.send_message(party.color, self.message_choose_unit(party))
        # Получаем ответ от игрока каким юнитом будет ходить
        self.server.get_message()
        # Выделяем юнита которым игрок будет ходить
        self.unit = party.units[int(self.server.gotten_message)]


    def check_coin_for_unit(self, party):
        """Смотрим монету под ногами и спршиваем пойдём с ней или нет"""
        # Проверить наличие монет под ногами
        check, coin = self.unit.check_coin()
        if check is True:
            # Проверить хавтает ли места и взять монету
            self.unit.check_limit_backpack_and_put(coin)
        # Спросить игрока брать монету или нет
        if len(self.unit.backpack) > 0:
            self.server.send_message(party.color, self.message_coin())
            self.server.get_message()
            if self.server.gotten_message == 'n':
                self.unit.drop_coin()

    def set_way_unit(self, party):
        """Установить направление движения"""
        self.unit.calculate_ways()
        self.map.print_map(self.unit.ways)
        self.unit.ways = []
        # Спрашиваем у игрока куда он будет ходить
        self.server.send_message(party.color, self.message_choose_way())
        # Получаем ответ куда он будет ходить
        self.server.get_message()
        # Выделяем напрваление движение юнита
        self.unit.way = self.server.gotten_message
        # Передвигаем юнита на карте
        self.map.action_on_map(party, self.unit)

    def search_dead_unit(self, party):
        """Найти мёртвого юнита"""
        for unit in party.units:
            if unit.life is False:
                return unit
        return None

    def check_global_skip_turn(self, party):
        """Проверить глобальный пропуск хода"""
        for unit in party.alive_creature:
            if unit.in_sex is True:
                self.unit = unit
                return True
        return False

    # Блок вывода информации
    def message_choose_unit(self, party):
        """Вопрос игроку, кем будет ходить"""
        self.add_map()
        data = '\n{0:>30}ХОДИТ ИГРОК № {1}'.format('', str(party.index))
        for line in range(20):
            for unit in party.vehicle:
                if line == 2:
                    data += '{0:^30}'.format(unit.name)
                elif line == 4:
                    tile = self.map.map[unit.y_coord][unit.x_coord][0]
                    data += '{0:^30}'.format(tile.name)
                elif line == 6:
                    data += '{0:^30}'.format(' ')
                elif line == 7:
                    data += '{0:^30}'.format(' ')
                elif line == 9:
                    if len(unit.backpack) == 1:
                        coin_message = '{0} монета'.format(len(unit.backpack))
                    elif len(unit.backpack) > 0:
                        coin_message = '{0} монеты'.format(len(unit.backpack))
                    else:
                        coin_message = '{0} монет'.format(len(unit.backpack))

                    data += Fore.YELLOW + '{0:^30}'.format(coin_message) + party.color

            for unit in party.alive_creature:
                if line == 2:
                    data += '{0:^15}'.format(unit.name)

                if line == 4:
                    tile = self.map.map[unit.y_coord][unit.x_coord][0]
                    data += '{0:^15}'.format(tile.name)
                elif line == 6:
                    if unit.under_effect is True:
                        data += '{0:^15}'.format('Негативный')
                    else:
                        data += '{0:^15}'.format(' ')
                elif line == 7:
                    if unit.under_effect is True:
                        data += '{0:^15}'.format('эффект')
                    else:
                        data += '{0:^15}'.format(' ')
                elif line == 9:
                    if len(unit.backpack) > 0:
                        coin_message = 'O'
                    else:
                        coin_message = ' '
                    data += Fore.LIGHTYELLOW_EX + '{0:^15}'.format(coin_message) + party.color
            data += '\n'

        answer = '0'
        for pirate in party.alive_creature:
            answer += '/' + str(pirate.index)
        answer = answer.split('/')
        return data, answer

    def message_choose_way(self):
        """Вопрос игроку, куда будет ходить?"""
        data = 'Выберите куда будете ходите: {0}'.format(self.unit.choose_way())
        answer = self.unit.choose_way().split('/')
        return data, answer

    def message_coin(self):
        """Вопрос игроку, что он будет делать с монетой?"""
        data = 'У {0} есть монета. Хотите пойти дальше с монетой?'.format(self.unit.name)
        answer = ['y', 'n']
        return data, answer
