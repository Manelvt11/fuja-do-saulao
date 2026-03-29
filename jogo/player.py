import pygame

class Player:
    def __init__(self, x, y, velocidade):
        self.x = x
        self.y = y
        self.velocidade = velocidade

        self.imagem = pygame.image.load("assets/player.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (150, 140))

    def mover(self):
        teclado = pygame.key.get_pressed()

        if teclado[pygame.K_LEFT]:
            self.x -= self.velocidade
        
        if teclado[pygame.K_RIGHT]:
            self.x += self.velocidade

        if teclado[pygame.K_UP]:
            self.y -= self.velocidade

        if teclado[pygame.K_DOWN]:
            self.y += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

        

