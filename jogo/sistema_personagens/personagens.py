import pygame

#Classe pai
#a classe Personagem possui características comuns para todos os personagens do jogo, como:
#posição, velocidade e colisão
class Personagem:
    def __init__(self, x, y, largura, altura, velocidade):
        #posição real do personagem
        self.pos_x = float(x)
        self.pos_y = float(y)

        #rect responsavel pela colisão e posição
        self.rect = pygame.Rect(x, y, largura, altura)

        #velocidade
        self.velocidade = velocidade

    def mover(self, dx, dy, obstaculos, largura_mapa=800, altura_mapa=600):
        #posição anterior para verificar colisões
        antigo_x = self.pos_x
        antigo_y = self.pos_y

        self.pos_x += dx
        self.pos_y += dy

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.pos_x = antigo_x
                self.rect.x = int(self.pos_x)

                break

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.pos_y = antigo_y
                self.rect.y = int(self.pos_y)

                break

        #limite do mapa
        self.pos_x = max(0, min(self.pos_x, largura_mapa - self.rect.width))
        self.pos_y = max(0, min(self.pos_y, altura_mapa - self.rect.height))
        
        # atualiza o Rect
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)