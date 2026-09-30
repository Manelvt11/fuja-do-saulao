import pygame
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Cogumelos:
    def __init__(self, posicoes):
        cogumelo1 = os.path.join(BASE_DIR, "assets", "itens", "itens_ambientacao", "cogumelo1.png")
        cogumelo2 = os.path.join(BASE_DIR, "assets", "itens", "itens_ambientacao", "cogumelo2.png")
        cogumelo3 = os.path.join(BASE_DIR, "assets", "itens", "itens_ambientacao", "cogumelo3.png")

        self.cogumelos = [
            pygame.transform.scale_by(pygame.image.load(cogumelo1).convert_alpha(), 0.10),
            pygame.transform.scale_by(pygame.image.load(cogumelo2).convert_alpha(), 0.10),
            pygame.transform.scale_by(pygame.image.load(cogumelo3).convert_alpha(), 0.10),
        ]

        self.posicoes = [(x, y, random.choice(self.cogumelos)) for x, y in posicoes]

    def atualizar(self, dt):
        pass

    def desenhar(self, tela):
        for x, y, imagem in self.posicoes:
            rect = imagem.get_rect(center=(x,y))
            tela.blit(imagem, rect)