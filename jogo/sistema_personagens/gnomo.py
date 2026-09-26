import pygame
import os
from sistema_personagens.personagens import Personagem
from sistema_personagens.ia_gnomo import GnomoIA

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Gnomo(Personagem):
    def __init__(self, x, y, velocidade=1.2):
        super().__init__(x, y, 8, 6, velocidade)
        self.rect_corpo = pygame.Rect(self.rect.centerx - 4, self.rect.bottom - 5, 8, 5)
        self.frame_largura = 256
        self.frame_altura = 256
        self.frames_por_linha = 6
        self.velocidade_animacao = 8

        caminho = os.path.join(BASE_DIR, "assets", "estranhesaulon", "criaturas", "gnomo", "gnomo.png")
        self.spritesheet = pygame.image.load(caminho).convert_alpha()
        self.ia = GnomoIA(self)

    def atualizar(self,jogador, mapa):
        posicao_anterior = self.rect.topleft
        self.ia.atualizar(jogador, mapa)
        andando = self.pos_x != posicao_anterior[0] or self.pos_y != posicao_anterior[1]
        self.animar(andando)

    def desenhar(self, tela):
        linha = self.direcoes[self.direcao]
        x_frame = self.frame_atual * self.frame_largura
        y_frame = linha * self.frame_altura

        frame = self.spritesheet.subsurface((x_frame, y_frame, self.frame_largura, self.frame_altura))
        imagem = pygame.transform.scale(frame, (int(self.frame_largura * 0.15), int(self.frame_altura * 0.15)))
        imagem_rect = imagem.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 3))

        tela.blit(imagem, imagem_rect)
        self.desenhar_sombra(tela, largura=24, altura=10, alpha=100)