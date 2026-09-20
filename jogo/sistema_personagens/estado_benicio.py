from enum import Enum, auto

class EstadoBenicio(Enum):
    PARADO = auto()
    ANDANDO = auto()
    DANO = auto()
    MORTO = auto()