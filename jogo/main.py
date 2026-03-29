import pygame
from player import Player 

pygame.init() 

tela = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption("Fuja do Saulão") 

fundo = pygame.image.load("assets/lab.png").convert() 
novo_tamanho_fundo = (800, 600) 
fundo_redimensionado = pygame.transform.scale(fundo, novo_tamanho_fundo) 

clock = pygame.time.Clock() 
FPS = 60

LARGURA = 800
ALTURA = 600

largura_player = 150
altura_player = 140

x = LARGURA // 2 - largura_player // 2
y = ALTURA // 2 - altura_player // 2

player = Player(x, y, 5)

rodando = True 
while rodando: 
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            rodando = False 
            
    tela.blit(fundo_redimensionado, (0, 0)) 

    player.mover()
    player.desenhar(tela)

    pygame.display.flip()

    clock.tick(FPS) 

pygame.quit()
