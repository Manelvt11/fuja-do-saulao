import pygame
from player import Player

pygame.init()

tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fuja do Saulão")

fundo = pygame.image.load("assets/img/lab.png").convert()
novo_tamanho_fundo = (800, 600)
fundo_redimensionado = pygame.transform.scale(fundo, novo_tamanho_fundo)

clock = pygame.time.Clock()
FPS = 60

LARGURA = 800
ALTURA = 600
TOPO = 180
BAIXO = 600

largura_player = 150
altura_player = 140
altura_area = BAIXO - TOPO

x = LARGURA // 2 - largura_player // 2
y = TOPO + (altura_area // 2) - altura_player // 2

player = Player(x, y, 5)

mesa1 = pygame.Rect(140, 230, 205, 50)  # mesa de cima esquerda
mesa2 = pygame.Rect(455, 230, 200, 50)  # mesa de cima direita

mesa3 = pygame.Rect(140, 420, 205, 33)  # baixo esquerda
mesa4 = pygame.Rect(455, 420, 200, 33)  # baixo direita

parede_cima = pygame.Rect(0, 120, 800, 20)
parede_baixo = pygame.Rect(0, 560, 800, 40)

parede_esquerda = pygame.Rect(0, 0, 40, 600)
parede_direita = pygame.Rect(740, 0, 40, 600)

obstaculos = [mesa1, mesa2, mesa3, mesa4, parede_cima, parede_baixo, parede_direita, parede_esquerda]

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.blit(fundo_redimensionado, (0, 0))

    player.mover(obstaculos)
    player.desenhar(tela)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()