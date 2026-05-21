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

    def mover(self,dx,dy,obstaculos):
        self.rect.x += dx

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                if dx > 0:
                    self.rect.right = obs.left

                if dx < 0:
                    self.rect.left = obs.right

        self.rect.y += dy

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                if dy > 0:
                    self.rect.bottom = obs.top

                if dy < 0:
                    self.rect.top = obs.bottom
        
        self.rect.clamp_ip(pygame.Rect(20, 20, 760, 540))
