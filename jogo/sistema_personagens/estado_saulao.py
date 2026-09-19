from enum import Enum, auto

class EstadoSaulao(Enum):
    PARADO = auto()
    PERSEGUINDO = auto()
    ATACANDO = auto()
    DANO = auto()
    MORTO = auto()