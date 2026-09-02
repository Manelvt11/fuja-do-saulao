import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HUD:
    def __init__(self):
        sprite = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "hud", "spritecoracao.png")
        ).convert_alpha()

        self.tamanho = 40

        self.frames = [
            self.recortar(sprite, (46, 90, 229, 203)),
            self.recortar(sprite, (364, 94, 245, 207)),
            self.recortar(sprite, (694, 94, 245, 202)),
            self.recortar(sprite, (1027, 94, 262, 213)),
        ]

        self.coracao_vazio = self.recortar(
            sprite,
            (1400, 395, 235, 230)
        )

        #Controle da animação
        self.animando = False
        self.frame_atual = 0
        self.tempo_frame = 0

        self.vida_anterior = 3

    def recortar(self, sprite, area):

        x, y, largura, altura = area

        frame = sprite.subsurface(
            pygame.Rect(x, y, largura, altura)
        ).copy()

        escala = min(
            self.tamanho / largura,
            self.tamanho / altura
        )

        nova_largura = int(largura * escala)
        nova_altura = int(altura * escala)

        frame = pygame.transform.scale(
            frame,
            (nova_largura, nova_altura)
        )

        resultado = pygame.Surface(
            (self.tamanho, self.tamanho),
            pygame.SRCALPHA
        )

        pos_x = (self.tamanho - nova_largura) // 2
        pos_y = (self.tamanho - nova_altura) // 2

        resultado.blit(frame, (pos_x, pos_y))

        return resultado

    def desenhar(self, tela, jogador):
        #Detecta perda de vida
        if jogador.vida < self.vida_anterior:

            self.animando = True
            self.frame_atual = 0
            self.tempo_frame = 0

        self.vida_anterior = jogador.vida

        #animação
        if self.animando:

            self.tempo_frame += 1

            # Quanto maior, mais lenta
            if self.tempo_frame >= 15:

                self.tempo_frame = 0
                self.frame_atual += 1

                if self.frame_atual >= len(self.frames):

                    self.animando = False
                    self.frame_atual = 0

        #Desenha os 3 corações
        for i in range(3):

            x = 10 + i * 50
            y = 10

            #Coração que acabou de ser perdido
            if self.animando and i == jogador.vida:

                imagem = self.frames[self.frame_atual]

            #Corações cheios
            elif i < jogador.vida:

                imagem = self.frames[0]

            #Corações vazios
            else:

                imagem = self.coracao_vazio

            tela.blit(imagem, (x, y))