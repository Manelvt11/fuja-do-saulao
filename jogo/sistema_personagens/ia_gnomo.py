from sistema_personagens.ia_inimigo import InimigoIA
import pygame

class GnomoIA(InimigoIA):
    def __init__(self, gnomo):
        super().__init__(gnomo)
        self.cooldown_ataque = 0

    def atualizar(self, jogador, mapa):
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        distancia = pygame.Vector2(self.inimigo.rect.center).distance_to(jogador.rect.center)
        if distancia <= 30:
            if self.cooldown_ataque == 0:
                jogador.receber_dano(0.5)
                self.cooldown_ataque = 30
            return
        
        self.atualizar_perseguicao(jogador, mapa)