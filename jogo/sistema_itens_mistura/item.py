import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Item:
    COLUNAS = 3
    LINHAS = 2

    def __init__(self, nome, frame, x, y):
        self.nome = nome
        self.rect = pygame.Rect(x, y, 48, 48)

        self.coletado = False

        spritesheet = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "itens", "frascos.png")
        ).convert_alpha()

        frame_largura = spritesheet.get_width() // self.COLUNAS
        frame_altura = spritesheet.get_height() // self.LINHAS

        coluna = frame % self.COLUNAS
        linha = frame // self.COLUNAS

        x_frame = coluna * frame_largura
        y_frame = linha * frame_altura

        self.imagem = spritesheet.subsurface(
            (
                x_frame,
                y_frame,
                frame_largura,
                frame_altura
            )
        )

        self.imagem = pygame.transform.scale(
            self.imagem,
            (48, 48)
        )

    def desenhar(self, tela):
        if not self.coletado:
            tela.blit(self.imagem, self.rect)