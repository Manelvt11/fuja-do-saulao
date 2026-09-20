import pygame
import random

class Iluminacao:
    def __init__(self, raio=110):
        self.raio = raio
        raio_nucleo = int(self.raio * 0.55)
        intensidade_maxima = 235
        self.luz = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)

        for raio_atual in range(self.raio, 0, -1):
            if raio_atual <= raio_nucleo:
                alpha = intensidade_maxima
            else:
                frac = ((raio_atual - raio_nucleo) / (self.raio - raio_nucleo))
                alpha = int(intensidade_maxima * (1 - frac))

            pygame.draw.circle(self.luz, (0, 0, 0, alpha), (self.raio, self.raio), raio_atual)

    def aplicar(self, tela, x, y):
        dark = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        flicker = random.randint(-10, 10)
        dark.fill((0, 0, 0, 160 + flicker))

        dark.blit(self.luz, (x - self.raio, y - self.raio), special_flags=pygame.BLEND_RGBA_SUB)
        tela.blit(dark, (0, 0))