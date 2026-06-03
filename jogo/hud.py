import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HUD:
    def __init__(self):
        cheio = pygame.image.load(os.path.join(BASE_DIR, "assets", "hud", "coracao_cheio.png")).convert_alpha()
        vazio = pygame.image.load(os.path.join(BASE_DIR, "assets", "hud", "coracao_vazio.png")).convert_alpha()

        self.coracao_cheio = pygame.transform.scale(cheio, (40, 40))
        self.coracao_vazio = pygame.transform.scale(vazio, (40, 40))

    def desenhar(self, tela, jogador):
        for i in range(3):
            if i < jogador.vida:
                imagem = self.coracao_cheio
            
            else:
                imagem = self.coracao_vazio

            tela.blit(imagem, (10 + i * 50, 10))