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

        margem_x = 7
        margem_y = 5

        for obs in self.obstaculos:
            obstaculo = obs.inflate(margem_x * 2, margem_y * 2)
        
            for y in range(linhas):
                for x in range(colunas):
                    tile_rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
        
                    if tile_rect.colliderect(obstaculo):
                        self.grid[y][x] = 0
    
    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

    def desenhar_debug(self, tela):
        for obs in self.obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obs, 2)