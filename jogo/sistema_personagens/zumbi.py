from sistema_personagens.personagens import Personagem
from sistema_personagens.ia_zumbi import ZumbiIA
import pygame
import os
from sistema_personagens.estado_zumbi import EstadoZumbi

class Zumbi(Personagem):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, 10, 7, velocidade)

        