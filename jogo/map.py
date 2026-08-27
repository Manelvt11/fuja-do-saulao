import pygame
import pytmx
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Map:
    def __init__(self):
        caminho_tmx = os.path.join(BASE_DIR, "assets", "cenario", "laboratorio", "laboratorio-tiled.tmx")
        self.tmx = pytmx.load_pygame(caminho_tmx)

        #tamanho do mundo agora vem direto do próprio mapa (tiles x tamanho do tile)
        self.largura = self.tmx.width * self.tmx.tilewidth
        self.altura = self.tmx.height * self.tmx.tileheight

        caminho_fundo = os.path.join(BASE_DIR, "assets", "cenario", "laboratorio", "mapa.png")
        self.fundo = pygame.image.load(caminho_fundo).convert()
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

        #obstaculos com a biblioteca pytmx e tiled
        #como o mapa novo já nasce no tamanho final, não vou mais escalar
        self.obstaculos = [
            pygame.Rect(
                int(obj.x), 
                int(obj.y), 
                int(obj.width), 
                int(obj.height)
            )
            for obj in self.tmx.get_layer_by_name("colisoes")
        ]

        self.tile_size = self.tmx.tilewidth
        colunas = self.largura // self.tile_size
        linhas = self.altura // self.tile_size

        self.grid = [[1 for _ in range(colunas)] for _ in range(linhas)]

        for obs in self.obstaculos:
            inicio_x = obs.left // self.tile_size
            fim_x = obs.right // self.tile_size

            inicio_y = obs.top // self.tile_size
            fim_y = obs.bottom // self.tile_size

            for y in range(inicio_y, fim_y):
                for x in range(inicio_x, fim_x):
                    if 0 <= y < linhas and 0 <= x < colunas:
                        self.grid[y][x] = 0
    
    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

    def desenhar_debug(self, tela):
        for obs in self.obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obs, 2)