import pygame
from sistema_personagens.personagens import Personagem
import os
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Classe Filha
#A classe Saulao também herda características da classe Personagem
#Saulão será o inimigo do jogo

#tamanho do sprite desenhado na tela
ESCALA_SPRITE = 0.7
SPRITE_LARGURA = int(48 * ESCALA_SPRITE)
SPRITE_ALTURA = int(72 * ESCALA_SPRITE)

class Saulao(Personagem):
    def __init__(self, x, y, velocidade=float):
        super().__init__(x, y, 13, 9, velocidade)

        caminho = os.path.join(BASE_DIR,"..", "assets", "inimigo", "saulao.png")
        imagem = pygame.image.load(caminho).convert_alpha()
        self.imagem = pygame.transform.scale(imagem, (SPRITE_LARGURA, SPRITE_ALTURA))

        self.glow_raio = 30
        self.glow = pygame.Surface((self.glow_raio * 2, self.glow_raio * 2), pygame.SRCALPHA)

        cor_nucleo = (90, 15, 130)   # roxo escuro
        cor_borda = (25, 5, 40)      # quase preto com tom roxo nas bordas

        for raio in range(self.glow_raio, 0, -1):
            t = raio / self.glow_raio

            r = int(cor_borda[0] + (cor_nucleo[0] - cor_borda[0]) * (1 - t))
            g = int(cor_borda[1] + (cor_nucleo[1] - cor_borda[1]) * (1 - t))
            b = int(cor_borda[2] + (cor_nucleo[2] - cor_borda[2]) * (1 - t))
            alpha = int(70 * (1 - t))

            pygame.draw.circle(
                self.glow, (r, g, b, alpha),
                (self.glow_raio, self.glow_raio), raio
            )

        self.tempo_path = 0
        self.caminho = []


    def perseguir(self, jogador, mapa):
        tile = mapa.tile_size

        colunas = len(mapa.grid[0])
        linhas = len(mapa.grid)

        inicio_x = max(0, 
                   min(self.rect.centerx // tile, colunas - 1))
        inicio_y = max(0, 
                   min(self.rect.centery // tile, linhas - 1))

        fim_x = max(0, 
                min(jogador.rect.centerx // tile, colunas - 1))
        fim_y = max(0, 
                min(jogador.rect.centery // tile, linhas - 1))


        self.tempo_path += 1
        if self.tempo_path >= 45 or (fim_x, fim_y) != getattr(self, 'ultimo_fim', None) or (inicio_x, inicio_y) != getattr(self, 'ultimo_inicio', None):
            self.tempo_path = 0
            self.ultimo_fim = (fim_x, fim_y)
            self.ultimo_inicio = (inicio_x,inicio_y)

            grid = Grid(matrix=mapa.grid)
            inicio = grid.node(inicio_x, inicio_y)
            fim = grid.node(fim_x, fim_y)

            finder = AStarFinder()

            self.caminho, _ = finder.find_path(inicio, fim, grid)

        # pega o alvo, usa tile 2 à frente se possível pra movimento mais suave
        if len(self.caminho) > 2:
            alvo = self.caminho[2]

        elif len(self.caminho) > 1:
            alvo = self.caminho[1]

        else:
            #fallback: perseguição direta quando A* não encontra caminho
            dx =0
            dy =0
            
            if self.rect.centerx < jogador.rect.centerx:
                dx = self.velocidade

            elif self.rect.centerx > jogador.rect.centerx:
                dx = -self.velocidade

            if self.rect.centery < jogador.rect.centery:
                dy = self.velocidade

            elif self.rect.centery > jogador.rect.centery:
                dy = -self.velocidade

            super().mover(dx, dy, mapa.obstaculos, mapa.largura, mapa.altura)
            return

        alvo_x = alvo.x * tile + tile // 2
        alvo_y = alvo.y * tile + tile // 2

        dx =0
        dy = 0

        if self.rect.centerx < alvo_x:
            dx = self.velocidade

        elif self.rect.centerx > alvo_x:
            dx = -self.velocidade

        if self.rect.centery < alvo_y:
            dy = self.velocidade
            
        elif self.rect.centery > alvo_y:
            dy = -self.velocidade

        super().mover(dx, dy, mapa.obstaculos, mapa.largura, mapa.altura)

    def verificar_colisao_jogador(self, jogador):
        return self.rect.colliderect(jogador.rect)
    
    def desenhar(self, tela):
        glow_rect = self.glow.get_rect(center=(self.rect.centerx, self.rect.centery))
        tela.blit(self.glow, glow_rect, special_flags=pygame.BLEND_RGBA_ADD)

        imagem_rect = self.imagem.get_rect(
            midbottom=(self.rect.centerx, self.rect.bottom + 5)
        )
        tela.blit(self.imagem, imagem_rect)

        #sombra
        sombra = pygame.Surface((36, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())
        tela.blit(sombra, (self.rect.centerx - 18, self.rect.bottom - 4))

        #debug
        #pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)
