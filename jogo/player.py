import pygame

class Player:
    def __init__(self, x, y, velocidade):
        self.rect = pygame.Rect(x, y + 40 , 60, 50)
        self.velocidade = velocidade

        self.imagem = pygame.image.load("jogo/assets/player/player.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (150, 140))

    def mover(self, obstaculos):
        teclado = pygame.key.get_pressed()

        if teclado[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        
        if teclado[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                if teclado[pygame.K_RIGHT]:
                    self.rect.right = obs.left

                if teclado[pygame.K_LEFT]:
                    self.rect.left = obs.right

        if teclado[pygame.K_UP]:
            self.rect.y -= self.velocidade

        if teclado[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        for obs in obstaculos:
            if self.rect.colliderect(obs):
                if teclado[pygame.K_DOWN]:
                    self.rect.bottom = obs.top

                if teclado[pygame.K_UP]:
                    self.rect.top = obs.bottom

        if self.rect.left < 20:
            self.rect.left = 20

        if self.rect.top < 20:
            self.rect.top = 20

        if self.rect.right > 800 - 20:
            self.rect.right = 800 - 20

        if self.rect.bottom > 600 - 40:
            self.rect.bottom = 600 - 40


    def desenhar(self, tela):
        imagem_rect = self.imagem.get_rect(midbottom=self.rect.midbottom)
        tela.blit(self.imagem, imagem_rect.topleft)

        pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)