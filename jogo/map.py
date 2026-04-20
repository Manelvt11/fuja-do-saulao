import pygame

class Map:
    def __init__(self):
        self.largura = 800
        self.altura = 600

        self.fundo = pygame.image.load("jogo/assets/cenario/labo.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

        #obstaculos
        self.obstaculos = [
            #mesas
            pygame.Rect(135, 220, 210, 120), #mesa superior esquerda
            pygame.Rect(455, 220, 230, 120), #mesa superior direita
            pygame.Rect(110, 400, 240, 120),  #mesa inferior esquerda
            pygame.Rect(455, 400, 233, 120),  #mesa inferior direita

            #paredes
            pygame.Rect(0, 175, 800, 20), #parede de cima
            pygame.Rect(0, 560, 800, 40), #parede de baixo
            pygame.Rect(10, 0, 60, 600), #parede do lado esquerdo
            pygame.Rect(750, 0, 90, 600) #parede do lado direito

        ]

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

    def desenhar_debug(self, tela):
        for obs in self.obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obs, 2)