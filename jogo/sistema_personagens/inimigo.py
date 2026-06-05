import pygame
from sistema_personagens.personagens import Personagem
import os
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Classe Filha
#A classe Saulao também herda características da classe Personagem
#Saulão será o inimigo do jogo

class Saulao(Personagem):
    def __init__(self, x, y, velocidade=2):
        super().__init__(x, y, 30, 20, velocidade)

        caminho = os.path.join(BASE_DIR,"..", "assets", "inimigo", "saulao.png")
        imagem = pygame.image.load(caminho).convert_alpha()
        self.imagem = pygame.transform.scale(imagem, (80, 120))

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
            super().mover(dx, dy, mapa.obstaculos)
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

        super().mover(dx, dy, mapa.obstaculos)

    def verificar_colisao_jogador(self, jogador):
        return self.rect.colliderect(jogador.rect)
    
    def desenhar(self, tela):
        imagem_rect = self.imagem.get_rect(
            midbottom=(self.rect.centerx, self.rect.bottom + 5)
        )
        tela.blit(self.imagem, imagem_rect)

        #sombra
        sombra = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 100), sombra.get_rect())
        tela.blit(sombra, (self.rect.centerx - 25, self.rect.bottom - 5))

        #debug
        #pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)