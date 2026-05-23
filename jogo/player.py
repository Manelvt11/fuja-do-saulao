import pygame
from personagens import Personagem

#classe filha
#A classe Benicio herda atributos e métodos da classe Personagem
#Além das características herdadas, Benício possui:
#sprites
#animação
#direção
#controle pelo teclado

class Benício(Personagem):
    def __init__(self, x, y, velocidade):

        super().__init__(x, y, 40, 40, velocidade)

        self.sheet = pygame.image.load("jogo/assets/player/spritesheet.png").convert_alpha()

        #tamanho de benicio
        self.frame_largura = 256
        self.frame_altura = 384

        self.frames_por_linha = 4

        self.frame_atual = 0
        self.tempo_animacao = 0
        self.velocidade_animacao = 10

        self.direcao = "baixo"

        self.direcoes = {
            "baixo": 0,
            "cima": 1,
            "esquerda": 2,
            "direita": 3
        }

    #movimentacao com teclado
    def controlar(self, obstaculos):
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
            dx = int(dx * 0.7071)
            dy = int(dy * 0.7071)

        super().mover(dx, dy, obstaculos)

        # animação
        #if dx != 0 or dy != 0:
        #    self.tempo_animacao += 1

        #    if self.tempo_animacao >= self.velocidade_animacao:
        #        self.frame_atual = (self.frame_atual + 1) % self.frames_por_linha
        #        self.tempo_animacao = 0

        #else:
            #self.frame_atual = 0

    def desenhar(self, tela):
        linha = self.direcoes[self.direcao]

        x_frame = self.frame_atual * self.frame_largura
        y_frame = linha * self.frame_altura

        frame = self.sheet.subsurface(
            (x_frame, y_frame, self.frame_largura, self.frame_altura)
        )

        #sprite
        imagem = pygame.transform.scale(frame, (80, 120))

        imagem.set_alpha(230)

        offset_x = -12
        imagem_rect = imagem.get_rect(
            midbottom=(self.rect.centerx + offset_x, self.rect.bottom)
        )

        tela.blit(imagem, imagem_rect)

        #sombra
        sombra = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())

        tela.blit(sombra, (self.rect.centerx - 25, self.rect.bottom - 5))

        #debug da hitbox
        pygame.draw.rect(tela, (0, 255, 0), self.rect, 2)