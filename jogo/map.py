import pygame
import pytmx
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Map:
    def __init__(self):
        self.largura = 800
        self.altura = 600

        caminho_tmx = os.path.join(BASE_DIR, "assets", "cenario", "laboratorio.tmx")
        self.tmx = pytmx.load_pygame(caminho_tmx)

        caminho_fundo = os.path.join(BASE_DIR, "assets", "cenario", "labo.png")
        self.fundo = pygame.image.load(caminho_fundo).convert()
        self.fundo = pygame.transform.scale(self.fundo, (self.largura, self.altura))

        #tamanho original da img do laboratorio
        largura_original = 1536
        altura_original = 1024

        #proporção entre o tamanho original e o tamanho do jogo
        escala_x = self.largura / largura_original
        escala_y = self.altura / altura_original

        #obstaculos com a biblioteca pytmx e tiled
        self.obstaculos = [
            pygame.Rect(
                int(obj.x * escala_x), 
                int(obj.y * escala_y), 
                int(obj.width * escala_x), 
                int(obj.height * escala_y)
            )
            for obj in self.tmx.get_layer_by_name("colisoes")
        ]

        self.tile_size = 32
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

    
