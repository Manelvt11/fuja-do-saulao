import pygame 

pygame.init() 

tela = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption("Fuja do Saulão") 

fundo = pygame.image.load("assets/lab.png").convert() 
novo_tamanho_fundo = (800, 600) 
fundo_redimensionado = pygame.transform.scale(fundo, novo_tamanho_fundo) 

clock = pygame.time.Clock() 
FPS = 60 

rodando = True 
while rodando: 
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            rodando = False 
            
        tela.blit(fundo_redimensionado, (0, 0)) 

        clock.tick(FPS) 

        pygame.display.flip() 
        
pygame.quit()