from colorama import Fore


class Player:
    """Класс игрока"""
    key = False
    index = 0
    color = (Fore.LIGHTRED_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX)

    def __init__(self):
        # Информация об игроке
        self.color = Player.color[Player.index]
        Player.index += 1
        self.index = Player.index

    def enter_answer(self):
        """Вставить команду"""
        answer = input('Ирок №{0}: '.format(self.index))
        return answer
