import pygame
from sistema_personagens.ia_inimigo import InimigoIA
from sistema_personagens.estado_saulao import EstadoSaulao

class SaulaoIA(InimigoIA):
    def __init__(self, saulao):
        super().__init__(saulao)
        self.cooldown_ataque = 0

    def atualizar(self, jogador, mapa):
        distancia = pygame.Vector2(jogador.rect.center).distance_to(self.inimigo.rect.center)

        if self.inimigo.estado == EstadoSaulao.ATACANDO:
            return

        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        self.inimigo.mudar_estado(EstadoSaulao.PERSEGUINDO)

        if distancia <= 30:
            if self.cooldown_ataque == 0:
                self.inimigo.mudar_estado(EstadoSaulao.ATACANDO)
                return

        self.atualizar_perseguicao(jogador, mapa)