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

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

    def desenhar_debug(self, tela):
        for obs in self.obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obs, 2)