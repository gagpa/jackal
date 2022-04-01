class Coin:
    """Класс монетки"""
    name = 'Монетка'
    sign = 'M'

    def __init__(self, y, x):
        self.y_coord = y
        self.x_coord = x
        self.name = Coin.name
        self.type = 'Монета'
        self.nominal = 1
