import pygame
from jogo.player import Player
from jogo.map import Map
import random

pygame.init()

LARGURA = 800
ALTURA = 600

# tela base
tela_base = pygame.Surface((LARGURA, ALTURA))

# tela real
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
largura_tela, altura_tela = tela.get_size()

pygame.display.set_caption("Fuja do Saulão")

clock = pygame.time.Clock()
FPS = 60

# posição inicial
x = LARGURA // 2
y = ALTURA // 2

player = Player(x, y, 3)

# obstáculos
mapa = Map()

luz = pygame.Surface((300, 300), pygame.SRCALPHA)

for i in range(150, 0, -1):
    alpha = int(i * 1.7)
    pygame.draw.circle(luz, (0, 0, 0, 255 - alpha), (150, 150), i)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

    tela_base.fill((0, 0, 0))
    mapa.desenhar(tela_base)

    player.mover(mapa.obstaculos)
    player.desenhar(tela_base)

    DEBUG = False

    if DEBUG:
        mapa.desenhar_debug(tela_base)

    #iluminação
    dark = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    
    flicker = random.randint(-10, 10)

    dark.fill((0, 0, 0, 140 + flicker))

    dark.blit(
        luz,
        (player.rect.centerx - 150, player.rect.centery - 150),
        special_flags=pygame.BLEND_RGBA_SUB
    )

    tela_base.blit(dark, (0, 0))

    tela_escalada = pygame.transform.scale(tela_base, (largura_tela, altura_tela))
    tela.blit(tela_escalada, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()