import pygame
import os
from sistema_personagens.personagens import Personagem
from sistema_personagens.ia_saulao import SaulaoIA
from sistema_personagens.estado_saulao import EstadoSaulao

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

        self.frame_largura_ataque = 213
        self.frame_altura_ataque = 307
        self.frame_ataque = 0
        self.tempo_ataque = 0
        self.velocidade_ataque = 5

        self.direcoes = {
            "baixo": 0,
            "cima": 1,
            "direita": 3,
            "esquerda": 2,
        }

        self.direcoes_ataque = {
            "baixo": 0,
            "cima": 1,
            "direita": 2,
            "esquerda": 3
        }

        caminho = os.path.join( BASE_DIR, "assets", "inimigos", "saulao", "spritesaulao.png")
        self.spritesheet = pygame.image.load(caminho).convert_alpha()

        caminho_ataque = os.path.join(BASE_DIR, "assets", "inimigos", "saulao", "saulao_atacando.png")
        self.spritesheet_ataque = pygame.image.load(caminho_ataque).convert_alpha()

        self.glow_raio = 26  # também reduzi um pouco o tamanho, ajuste ao gosto
        self.glow = pygame.Surface((self.glow_raio * 2, self.glow_raio * 2), pygame.SRCALPHA)
        
        cor_nucleo = (90, 15, 130)
        raio_nucleo = int(self.glow_raio * 0.35)  # parte central com brilho mais forte
        
        for raio in range(self.glow_raio, 0, -1):
            if raio <= raio_nucleo:
                intensidade = 1.0
            else:
                frac = (raio - raio_nucleo) / (self.glow_raio - raio_nucleo)
                intensidade = 1 - frac
        
            r = int(cor_nucleo[0] * intensidade)
            g = int(cor_nucleo[1] * intensidade)
            b = int(cor_nucleo[2] * intensidade)
        
            pygame.draw.circle(self.glow, (r, g, b, 255), (self.glow_raio, self.glow_raio), raio)

        self.ia = SaulaoIA(self)
        self.estado = EstadoSaulao.PARADO
        self.dano_aplicado = False

    def atualizar_ia(self, jogador, mapa):
        self.ia.atualizar(jogador, mapa)

    def verificar_colisao_jogador(self, jogador):
        return self.rect.colliderect(jogador.rect)

    def verificar_ataque(self, jogador):
        alcance = 32

        if self.direcao == "direita":
            area = pygame.Rect(self.rect.right, self.rect.centery - 12, alcance, 24)
        elif self.direcao == "esquerda":
            area = pygame.Rect(self.rect.left - alcance, self.rect.centery - 12, alcance, 24)
        elif self.direcao == "baixo":
            area = pygame.Rect(self.rect.centerx - 12, self.rect.bottom, 24, alcance)
        else:
            area = pygame.Rect(self.rect.centerx - 12, self.rect.top - alcance, 24, alcance)

        return area.colliderect(jogador.rect)

    def mudar_estado(self, novo_estado):
        if self.estado == novo_estado:
            return

        print(f"Saulão: {self.estado.name} -> {novo_estado.name}")

        self.estado = novo_estado
        self.frame_atual = 0
        self.tempo_animacao = 0

        if novo_estado == EstadoSaulao.ATACANDO:
            self.frame_ataque = 0
            self.tempo_ataque = 0
            self.dano_aplicado = False

    def esta_perseguindo(self):
        return self.estado == EstadoSaulao.PERSEGUINDO

    def atualizar_animacao(self, jogador):
        if self.estado == EstadoSaulao.PERSEGUINDO:
            self.animar(True)

        elif self.estado == EstadoSaulao.ATACANDO:
            if self.animar_ataque(jogador):
                self.mudar_estado(EstadoSaulao.PERSEGUINDO)
                self.ia.cooldown_ataque = 30
        else:
            self.animar(False)

    def animar_ataque(self, jogador):
        self.tempo_ataque += 1
        if self.tempo_ataque >= self.velocidade_ataque:
            self.tempo_ataque = 0
            self.frame_ataque += 1

            if self.frame_ataque == 2 and not self.dano_aplicado:
                if self.verificar_ataque(jogador):
                    jogador.receber_dano()

                self.dano_aplicado = True

            if self.frame_ataque >= 6:
                self.frame_ataque = 0
                return True
            
        return False

    def desenhar(self, tela):
        glow_rect = self.glow.get_rect(center=(self.rect.centerx, self.rect.centery))

        tela.blit(self.glow, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)

        #animacao de ataque
        if self.estado == EstadoSaulao.ATACANDO:
            linha = self.direcoes_ataque[self.direcao]

            x_frame = self.frame_ataque * self.frame_largura_ataque
            y_frame = linha * self.frame_altura_ataque
            frame = self.spritesheet_ataque.subsurface(x_frame, y_frame, self.frame_largura_ataque, self.frame_altura_ataque)
            imagem = pygame.transform.scale(frame, (SPRITE_LARGURA, SPRITE_ALTURA))
            imagem_rect = imagem.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 5))
            tela.blit(imagem, imagem_rect)
            return

        # frame atual da animação
        linha = self.direcoes[self.direcao]

        x_frame = self.frame_atual * self.frame_largura
        y_frame = linha * self.frame_altura

        frame = self.spritesheet.subsurface((x_frame, y_frame, self.frame_largura, self.frame_altura))

        imagem = pygame.transform.scale(frame,(SPRITE_LARGURA, SPRITE_ALTURA))

        imagem_rect = imagem.get_rect(midbottom=(self.rect.centerx,self.rect.bottom + 5))
        tela.blit(imagem, imagem_rect)

        # sombra
        self.desenhar_sombra(tela)
        # debug
        # pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)