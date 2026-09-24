import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FendasEstranheza:
    def __init__(self, posicoes):
        caminho = os.path.join(BASE_DIR, "assets", "estranhesaulon", "efeitos", "fenda.png")
        self.imagem = pygame.image.load(caminho).convert_alpha()
        self.imagem = pygame.transform.scale_by(self.imagem, 0.10)
        self.posicoes = posicoes

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        for x, y in self.posicoes:
            rect = self.imagem.get_rect(center=(x, y))
            tela.blit(self.imagem, rect)