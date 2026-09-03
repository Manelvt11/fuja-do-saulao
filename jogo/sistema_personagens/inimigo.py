import pygame
import os
from sistema_personagens.personagens import Personagem
from sistema_personagens.ia_saulao import SaulaoIA


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Classe Filha
# A classe Saulao também herda características da classe Personagem
# Saulão será o inimigo do jogo
# tamanho do sprite desenhado na tela

ESCALA_SPRITE = 0.19
SPRITE_LARGURA = int(161 * ESCALA_SPRITE)
SPRITE_ALTURA = int(256 * ESCALA_SPRITE)

class Saulao(Personagem):
    def __init__(self, x, y, velocidade=float):
        super().__init__(x, y, 13, 9, velocidade)

        self.frame_largura = 161
        self.frame_altura = 256
        self.frames_por_linha = 6

        caminho = os.path.join( BASE_DIR, "..", "assets", "inimigo", "spritesaulao.png")
        self.spritesheet = pygame.image.load(caminho).convert_alpha()

        self.glow_raio = 30
        self.glow = pygame.Surface((self.glow_raio * 2, self.glow_raio * 2), pygame.SRCALPHA)

        cor_nucleo = (90, 15, 130)
        cor_borda = (25, 5, 40)

        for raio in range(self.glow_raio, 0, -1):
            t = raio / self.glow_raio
            r = int(cor_borda[0] + (cor_nucleo[0] - cor_borda[0]) * (1 - t))
            g = int(cor_borda[1] + (cor_nucleo[1] - cor_borda[1]) * (1 - t))
            b = int(cor_borda[2] +(cor_nucleo[2] - cor_borda[2]) * (1 - t))

            alpha = int(70 * (1 - t))

            pygame.draw.circle(self.glow,(r, g, b, alpha),(self.glow_raio, self.glow_raio),raio)

        self.ia = SaulaoIA(self)

    def atualizar_ia(self, jogador, mapa):
        self.ia.atualizar(jogador, mapa)

    def verificar_colisao_jogador(self, jogador):
        return self.rect.colliderect(jogador.rect)

    def desenhar(self, tela):
        glow_rect = self.glow.get_rect(center=(self.rect.centerx, self.rect.centery))

        tela.blit(self.glow, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)

        # frame atual da animação
        linha = self.direcoes[self.direcao]

        x_frame = self.frame_atual * self.frame_largura
        y_frame = linha * self.frame_altura

        frame = self.spritesheet.subsurface((x_frame, y_frame, self.frame_largura, self.frame_altura))

        imagem = pygame.transform.scale(frame,(SPRITE_LARGURA, SPRITE_ALTURA))

        imagem_rect = imagem.get_rect(midbottom=(self.rect.centerx,self.rect.bottom + 5))
        tela.blit(imagem, imagem_rect)

        # sombra
        sombra = pygame.Surface((36, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra,(0, 0, 0, 100),sombra.get_rect())

        tela.blit(sombra,(self.rect.centerx - 18,self.rect.bottom - 4))
        # debug
        # pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)