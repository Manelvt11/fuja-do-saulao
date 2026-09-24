import pygame
import pytmx
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Map:
    def __init__(self):
        caminho_tmx = os.path.join(BASE_DIR, "assets", "cenario", "laboratorio", "laboratorio-tiled.tmx")
        self.tmx = pytmx.load_pygame(caminho_tmx)

        self.itens = []

        camada_itens = self.tmx.get_layer_by_name("itens")
        for obj in camada_itens:
            self.itens.append((obj.name, obj.x, obj.y))

        self.estranheza = []
        camada_estranheza = self.tmx.get_layer_by_name("estranheza")
        for obj in camada_estranheza:
            self.estranheza.append((obj.x, obj.y))


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

    def encontrar_posicao_livre(self, largura,altura):
        while True:
            x = random.randint(0, self.largura - largura)
            y = random.randint(0, self.altura - altura)
            rect = pygame.Rect(x, y, largura, altura)

            if not any(rect.colliderect(obs) for obs in self.obstaculos):
                return x, y

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

    def desenhar_debug(self, tela):
        for obs in self.obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obs, 2)