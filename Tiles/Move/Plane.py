from colorama import Style

from Tiles.Tile import Tile


class Plane(Tile):
    """Класс самолёт"""
    name = 'Самолёт'
    sign = 'P'
    sign_level = {1: ' _____ _____ ',
                  2: '|          {0}|',
                  3: '|  {0}={1}={2}=   |',
                  4: '|           |',
                  5: '|_____ _____|'}

    def __init__(self):
        super(Plane, self).__init__()
        self.work = True
        self.sign_paint_tile = Plane.sign_level

    def activate_tile(self, player, unit):
        """Активация самолёта"""
        super(Plane, self).activate_tile(player, unit)
        self.fight_on_tile(player, unit)
        self.map.print_map()
        if self.work is True:
            self.plane_in_cell(player, unit)

        else:
            self.send_and_get_message(player.color, self.message_plane_is_broken())

    def choose_cell(self, player):
        """Выбрать клетку"""
        self.send_and_get_message(player.color, self.message_choose_y_coord())
        y = int(self.server.gotten_message)
        self.send_and_get_message(player.color, self.message_choose_x_coord())
        x = int(self.server.gotten_message)
        self.work = False
        return y, x

    def plane_in_cell(self, player, unit):
        """Полететь в выбранную клетку"""
        if unit in self.map.map[unit.y_coord][unit.x_coord]:
            self.map.del_unit_from_cell(unit)
        unit.y_coord, unit.x_coord = self.choose_cell(player)
        self.map.insert_unit_in_cell(unit)
        if False in self.map.map[unit.y_coord][unit.x_coord]:
            self.map.open_cell(player, unit)
        self.map.activate_cell(player, unit)

    def message_choose_y_coord(self):
        """Сообщение в какую клетку хотите полететь. Y = """
        data = 'В какую клетку хотите полететь?\nY = '
        answer = []
        for count in range(self.map.dimension_map):
            answer.append(str(count))
        return data, answer

    def message_choose_x_coord(self):
        """Сообщение для выбора X"""
        data = 'X = '
        answer = []
        for count in range(self.map.dimension_map):
            answer.append(str(count))
        return data, answer

    def message_plane_is_broken(self):
        """Сообщение что самолёт сломан"""
        data = 'Самолёт сломан\n\tНажмите ENTER чтобы продолжить'
        answer = Tile.answer
        return data, answer

    def print_tile(self, y, x, level, backlight):
        units = self.search_unit(y, x)
        color = self.calculate_color(y, x)
        backlight_color = self.set_backlight_color(backlight)
        count_coin = self.search_coin(y, x)
        if level == 2:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(count_coin) + Style.RESET_ALL
            print(text, end='')
        elif level == 3:
            text = color + backlight_color + self.sign_paint_tile[level] \
                .format(units[0], units[1], units[2]) + Style.RESET_ALL
            print(text, end='')
        else:
            text = color + backlight_color + self.sign_paint_tile[level] + Style.RESET_ALL
            print(text, end='')
