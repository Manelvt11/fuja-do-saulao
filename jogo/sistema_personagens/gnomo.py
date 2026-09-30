import pygame
import os
from sistema_personagens.personagens import Personagem
from sistema_personagens.ia_gnomo import GnomoIA
import math
from sistema_personagens.estado_gnomo import EstadoGnomo

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

        caminho_chapeu = os.path.join(BASE_DIR, "assets", "estranhesaulon", "criaturas", "gnomo", "chapeu.png")
        self.imagem_chapeu = pygame.image.load(caminho_chapeu).convert_alpha()
        self.imagem_chapeu = pygame.transform.smoothscale(self.imagem_chapeu, (32, 32))

        self.chapeus = []

        self.estado = EstadoGnomo.PERSEGUINDO

    def atualizar(self,jogador, mapa):
        posicao_anterior = self.rect.topleft
        self.ia.atualizar(jogador, mapa)
        andando = self.pos_x != posicao_anterior[0] or self.pos_y != posicao_anterior[1]
        self.animar(andando)

        for chapeu in self.chapeus:
            chapeu.atualizar(jogador, mapa)

        self.chapeus = [chapeu for chapeu in self.chapeus if chapeu.ativo]

    def lancar_chapeu(self):
        direcoes = {
            "baixo": (0, 1),
            "cima": (0, -1),
            "esquerda": (-1, 0),
            "direita": (1, 0)
        }
        direcao = direcoes[self.direcao]
        chapeu = Chapeu(self.rect.centerx - 6, self.rect.centery - 6, direcao, self.imagem_chapeu)
        self.chapeus.append(chapeu)

    def desenhar(self, tela):
        linha = self.direcoes[self.direcao]
        x_frame = self.frame_atual * self.frame_largura
        y_frame = linha * self.frame_altura

        frame = self.spritesheet.subsurface((x_frame, y_frame, self.frame_largura, self.frame_altura))
        imagem = pygame.transform.scale(frame, (int(self.frame_largura * 0.15), int(self.frame_altura * 0.15)))
        imagem_rect = imagem.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 3))

        tela.blit(imagem, imagem_rect)
        self.desenhar_sombra(tela, largura=24, altura=10, alpha=100)

        for chapeu in self.chapeus:
            chapeu.desenhar(tela)


class Chapeu:
    def __init__(self,x , y, direcao,imagem, velocidade=4):
        self.rect = pygame.Rect(x,y, 12, 12)
        self.direcao = pygame.Vector2(direcao).normalize()
        self.velocidade = velocidade
        self.ativo = True

        self.imagem = imagem

    def atualizar(self, jogador, mapa):
        self.rect.x += int(self.direcao.x * self.velocidade)
        self.rect.y += int(self.direcao.y * self.velocidade)

        if self.rect.colliderect(jogador.rect):
            jogador.receber_dano(0.5)
            self.ativo = False
            return

        if self.rect.left < 0 or self.rect.right > mapa.largura or self.rect.top < 0 or self.rect.bottom > mapa.altura:
            self.ativo = False

    def desenhar(self, tela):
        if self.direcao.x > 0:
            imagem = pygame.transform.rotate(self.imagem, -90)
        elif self.direcao.x < 0:
            imagem = pygame.transform.rotate(self.imagem, 90)
        elif self.direcao.y > 0:
            imagem = pygame.transform.rotate(self.imagem, 180)
        else:
            imagem = self.imagem
        imagem_rect = imagem.get_rect(center=self.rect.center)
        tela.blit(imagem, imagem_rect)