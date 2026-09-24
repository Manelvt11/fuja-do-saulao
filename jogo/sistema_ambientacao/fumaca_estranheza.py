import pygame
import random
import math

class FumacaEstranheza:
    def __init__(self, quantidade=12):
        self.quantidade = quantidade
        self.particulas = []

    def criar_particula(self):
        angulo = random.uniform(0, math.pi * 2)
        distancia = random.uniform(2, 8)
        self.particulas.append({
            "x": math.cos(angulo) * distancia,
            "y": random.uniform(5, 12),
            "velocidade_x": random.uniform(-4, 4),
            "velocidade_y": random.uniform(-12, -5),
            "tamanho": random.uniform(3, 7),
            "vida": random.uniform(0.8, 1.5),
            "vida_maxima": 0
        })
        self.particulas[-1]["vida_maxima"] = self.particulas[-1]["vida"]

    def atualizar(self, dt):
        while len(self.particulas) < self.quantidade:
            self.criar_particula()

        for particula in self.particulas:
            particula["x"] += particula["velocidade_x"] * dt
            particula["y"] += particula["velocidade_y"] * dt
            particula["velocidade_x"] += random.uniform(-2, 2) * dt
            particula["tamanho"] += 2 * dt
            particula["vida"] -= dt

        self.particulas = [p for p in self.particulas if p["vida"] > 0]

    def desenhar(self, tela, x, y):
        for particula in self.particulas:
            proporcao = particula["vida"] / particula["vida_maxima"]
            alpha = int(90 * proporcao)
            tamanho = int(particula["tamanho"])
            superficie = pygame.Surface((tamanho * 2, tamanho * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie, (110, 35, 160, alpha), (tamanho, tamanho), tamanho)

            tela.blit(superficie, (x + particula["x"] - tamanho, y + particula["y"] - tamanho))
