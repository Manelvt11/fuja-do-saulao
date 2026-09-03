import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HUD:
    def __init__(self):
        sprite = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "hud", "spritecoracao.png")
        ).convert_alpha()

        self.frames = [
            sprite.subsurface((0, 0, 48, 48)),
            sprite.subsurface((48, 0, 48, 48)),
            sprite.subsurface((96, 0, 48, 48)),
            sprite.subsurface((144, 0, 48, 48))
        ]

        self.coracao_vazio = sprite.subsurface(
            (192, 0, 48, 48)
        )

        self.animando = False
        self.frame_atual = 0
        self.tempo_frame = 0
        self.vida_anterior = 3

    def desenhar(self, tela, jogador):
        if jogador.vida < self.vida_anterior:
            self.animando = True
            self.frame_atual = 0
            self.tempo_frame = 0

        self.vida_anterior = jogador.vida

        if self.animando:

            self.tempo_frame += 1

            if self.tempo_frame >= 15:
                self.tempo_frame = 0
                self.frame_atual += 1

                if self.frame_atual >= len(self.frames):
                    self.animando = False
                    self.frame_atual = 0

        for i in range(3):

            if self.animando and i == jogador.vida:
                imagem = self.frames[self.frame_atual]

            elif i < jogador.vida:
                imagem = self.frames[0]

            else:
                imagem = self.coracao_vazio

            tela.blit(imagem, (10 + i * 50, 10))