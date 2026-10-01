from sistema_personagens.ia_inimigo import InimigoIA
from sistema_personagens.estado_zumbi import EstadoZumbi
import pygame

class ZumbiIA(InimigoIA):
    def __init__(self, zumbi):
        super().__init__(zumbi)
        self.cooldown_ataque = 0
        self.tempo_ataque = 0

    def mudar_estado(self, novo_estado):
        if self.inimigo.estado != novo_estado:
            print(f"zumbi: {self.inimigo.estado.name} -> {novo_estado.name}")

    def atualizar(self, jogador, mapa):
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        distancia = pygame.Vector2(self.inimigo.rect.center).distance_to(jogador.rect.center)

        if self.inimigo.estado == EstadoZumbi.ATACANDO:
            self.tempo_ataque += 1

            if self.tempo_ataque >= 20:
                jogador.receber_dano()
                self.tempo_ataque = 0
                self.cooldown_ataque = 90
                self.mudar_estado(EstadoZumbi.PERSEGUINDO)
            return

        if distancia <= 30 and self.cooldown_ataque == 0:
            self.tempo_ataque = 0
            self.mudar_estado(EstadoZumbi.ATACANDO)
            return

        self.mudar_estado(EstadoZumbi.PERSEGUINDO)
        self.atualizar_perseguicao(jogador, mapa)