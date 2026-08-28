import pygame
from sistema_personagens.personagens import Personagem
import os
from sistema_itens_mistura.inventario import Inventario

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#classe filha
#A classe Benicio herda atributos e métodos da classe Personagem
#Além das características herdadas, Benício possui:
#sprites
#animação
#direção
#controle pelo teclado

#tamanho do sprite desenhado na tela
ESCALA_SPRITE = 0.19
SPRITE_LARGURA = int(155 * ESCALA_SPRITE)
SPRITE_ALTURA = int(246 * ESCALA_SPRITE)

class Benício(Personagem):
    def __init__(self, x, y, velocidade=float):
        super().__init__(x, y, 16, 18, velocidade)

        spritesheet = os.path.join(BASE_DIR, "..", "assets", "player", "spritesheet.png")
        self.spritesheet = pygame.image.load(spritesheet).convert_alpha()

        #vida
        self.vida = 3
        self.cooldown_dano = 0

        #tamanho de cada frame no arquivo de origem
        self.frame_largura = 155
        self.frame_altura = 246

        self.frames_por_linha = 6

        self.frame_atual = 0
        self.tempo_animacao = 0
        self.velocidade_animacao = 8

        self.direcao = "baixo"

        self.direcoes = {
            "baixo": 0,
            "cima": 1,
            "esquerda": 2,
            "direita": 3
        }

        self.inventario = Inventario()

    #movimentacao com teclado
    def controlar(self, obstaculos, largura_mapa=800, altura_mapa=600):
        if self.cooldown_dano > 0:
            self.cooldown_dano -= 1

        teclas = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= self.velocidade
            self.direcao = "esquerda"

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += self.velocidade
            self.direcao = "direita"

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= self.velocidade
            self.direcao = "cima"

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += self.velocidade
            self.direcao = "baixo"

        if dx != 0 and dy != 0:
            dx = int(dx * 0.92)
            dy = int(dy * 0.92)

        super().mover(dx, dy, obstaculos, largura_mapa, altura_mapa)

        #animação: avança o ciclo de passos só enquanto ele está realmente andando,
        #e volta pro frame parado (0) assim que solta a tecla
        if dx != 0 or dy != 0:
            self.tempo_animacao += 1

            if self.tempo_animacao >= self.velocidade_animacao:
                self.frame_atual = (self.frame_atual + 1) % self.frames_por_linha
                self.tempo_animacao = 0

        else:
            self.frame_atual = 0
            self.tempo_animacao = 0

    def receber_dano(self):
        if self.cooldown_dano <= 0:
            self.vida -= 1
            self.cooldown_dano = 120 #2 segundos

    def desenhar(self, tela):
        linha = self.direcoes[self.direcao]

        x_frame = self.frame_atual * self.frame_largura
        y_frame = linha * self.frame_altura

        frame = self.spritesheet.subsurface(
            (x_frame, y_frame, self.frame_largura, self.frame_altura)
        )

        #sprite
        imagem = pygame.transform.scale(frame, (SPRITE_LARGURA, SPRITE_ALTURA))

        imagem.set_alpha(230)

        offset_x = -5
        imagem_rect = imagem.get_rect(
            midbottom=(self.rect.centerx + offset_x, self.rect.bottom)
        )

        tela.blit(imagem, imagem_rect)

        #sombra
        sombra = pygame.Surface((36, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())

        tela.blit(sombra, (self.rect.centerx - 18, self.rect.bottom - 4))

        #debug da hitbox
        #pygame.draw.rect(tela, (0, 255, 0), self.rect, 2)