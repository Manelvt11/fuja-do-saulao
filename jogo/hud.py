import pygame
import os
from sistema_itens_mistura.icones import obter_icone

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

        tamanho_icone = 44
        espacamento = 6
        y_base = tela.get_height() - tamanho_icone - 10

        for i, item in enumerate(jogador.inventario.itens):
            icone = obter_icone(item.nome, tamanho=tamanho_icone)
            x = 10 + i * (tamanho_icone + espacamento)

            slot = pygame.Surface((tamanho_icone, tamanho_icone), pygame.SRCALPHA)
            slot.fill((0, 0, 0, 90))
            tela.blit(slot, (x, y_base))
            tela.blit(icone, (x, y_base))