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

        self.inventario_hud = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "hud", "inventarioHud.png")
        ).convert_alpha()

        self.inventario_largura = 220
        self.inventario_altura = 124    

        self.inventario_hud = pygame.transform.smoothscale(
            self.inventario_hud, (self.inventario_largura, self.inventario_altura)
        )

        self.posicoes_slots = [
            (54, 61),
            (110, 61),
            (166, 61)
        ]

        self.tamanho_icone = 48

        self.fonte_tempo = pygame.font.Font(None, 32)

    def desenhar(self, tela, jogador, tempo_restante):
        minutos = int(tempo_restante // 60)
        segundos = int(tempo_restante % 60)
        texto_tempo = f"{minutos:02d}:{segundos:02d}"

        tempo = self.fonte_tempo.render(texto_tempo, True, (255, 255, 255))
        rect_tempo = tempo.get_rect()
        rect_tempo.top = 20
        rect_tempo.right = 780
        tela.blit(tempo, rect_tempo)

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

        x_inventario = (tela.get_width() - self.inventario_largura) // 2
        y_inventario = (tela.get_height() - self.inventario_altura - 5)

        tela.blit(self.inventario_hud, (x_inventario, y_inventario))

        for i, item in enumerate(jogador.inventario.itens):
            if i >= 3:
                break

            slot_x, slot_y = self.posicoes_slots[i]

            icone = obter_icone(item.nome, tamanho=self.tamanho_icone)

            icone_x = (x_inventario + slot_x - self.tamanho_icone // 2)

            icone_y = (y_inventario + slot_y - self.tamanho_icone // 2)

            tela.blit(icone, (icone_x, icone_y))