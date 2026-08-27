import pygame

#Classe pai
#a classe Personagem possui características comuns para todos os personagens do jogo, como:
#posição, velocidade e colisão
class Personagem:
    def __init__(self, x, y, largura, altura, velocidade):
        #rect responsavel pela colisão e posição
        self.rect = pygame.Rect(x, y, largura, altura)

        #velocidade
        self.velocidade = velocidade

    def mover(self, dx, dy, obstaculos, largura_mapa=800, altura_mapa=600):
        dx = int(dx)
        dy = int(dy)

        if dx != 0:
            self.rect.x += dx
            for obs in obstaculos:
                if self.rect.colliderect(obs):
                    if dx > 0:
                        self.rect.right = obs.left

                    if dx < 0:
                        self.rect.left = obs.right

        if dy != 0:
            self.rect.y += dy
            for obs in obstaculos:
                if self.rect.colliderect(obs):
                    if dy > 0:
                        self.rect.bottom = obs.top

                    if dy < 0:
                        self.rect.top = obs.bottom

        #agora o limite acompanha o tamanho real do mapa, não mais a tela
        self.rect.clamp_ip(pygame.Rect(0, 0, largura_mapa, altura_mapa))