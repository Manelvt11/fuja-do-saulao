import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TelaEstranha:
    def __init__(self, tamanho):
        caminho = os.path.join(BASE_DIR, "assets", "estranhesaulon", "manifestacao", "tela_estranhesaulon.png")
        self.imagem = pygame.image.load(caminho).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, tamanho)
        self.ativa = False
        self.tempo = 0
        self.duracao = 3

    def ativar(self):
        self.ativa = True
        self.tempo = 0

    def atualizar(self, dt):
        if not self.ativa:
            return

        self.tempo += dt
        if self.tempo >= self.duracao:
            self.ativa = False

    def desenhar(self, tela):
        if self.ativa:
            tela.blit(self.imagem, (0, 0))