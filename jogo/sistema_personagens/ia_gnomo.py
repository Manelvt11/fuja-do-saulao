from sistema_personagens.ia_inimigo import InimigoIA
import pygame
from sistema_personagens.estado_gnomo import EstadoGnomo

class GnomoIA(InimigoIA):
    def __init__(self, gnomo):
        super().__init__(gnomo)
        self.cooldown_ataque = 0
        self.tempo_ataque = 0

    def atualizar(self, jogador, mapa):
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        distancia = pygame.Vector2(self.inimigo.rect.center).distance_to(jogador.rect.center)
        if self.inimigo.estado == EstadoGnomo.ATACANDO:
            self.tempo_ataque += 1

            if self.tempo_ataque >= 20:
                self.inimigo.lancar_chapeu()
                self.tempo_ataque = 0
                self.cooldown_ataque = 90
                self.mudar_estado(EstadoGnomo.PERSEGUINDO)
            return

        if distancia <= 60 and self.cooldown_ataque == 0:
            self.tempo_ataque = 0
            self.mudar_estado(EstadoGnomo.ATACANDO)
            return

        self.mudar_estado(EstadoGnomo.PERSEGUINDO)
        self.atualizar_perseguicao(jogador, mapa)
        print("Distância do Gnomo:", distancia)

    def mudar_estado(self, novo_estado):
        if self.inimigo.estado != novo_estado:
            print(f"Gnomo: {self.inimigo.estado.name} -> {novo_estado.name}")
            self.inimigo.estado = novo_estado