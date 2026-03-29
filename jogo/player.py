import pygame

class Player:
    def __init__(self, x, y, velocidade):
        self.rect = pygame.Rect(x, y + 40, 80, 90)
        self.velocidade = velocidade

        self.imagem = pygame.image.load("assets/player.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (150, 140))

    def mover(self, obstaculos):
        teclado = pygame.key.get_pressed()

        posicao_antiga_x = self.rect.x

        if teclado[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        
        if teclado[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.rect.x = posicao_antiga_x

        posicao_antiga_y = self.rect.y

        if teclado[pygame.K_UP]:
            self.rect.y -= self.velocidade

        if teclado[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                self.rect.y = posicao_antiga_y

        if self.rect.left < 20:
            self.rect.left = 20

        if self.rect.top < 20:
            self.rect.top = 20

        if self.rect.right > 800 - 20:
            self.rect.right = 800 - 20

        if self.rect.bottom > 600 - 40:
            self.rect.bottom = 600 - 40


    def desenhar(self, tela):
        tela.blit(self.imagem, (self.rect.x - 30, self.rect.y - 40))
