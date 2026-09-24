import pygame
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ParticulasEstranheza:
    def __init__(self, quantidade=8):
        caminho = os.path.join(BASE_DIR, "assets", "estranhesaulon", "efeitos", "particula_estranheza.png")
        self.imagem = pygame.image.load(caminho).convert_alpha()
        self.quantidade = quantidade
        self.particulas = []

    def criar_particula(self):
        self.particulas.append({
            "x": random.uniform(-8, 8),
            "y": random.uniform(0, 8),
            "velocidade_x": random.uniform(-8, 8),
            "velocidade_y": random.uniform(-22, -10),
            "vida": random.uniform(0.7, 1.3),
            "vida_maxima": 0,
            "escala": random.uniform(0.10, 0.18)
        })
        self.particulas[-1]["vida_maxima"] = self.particulas[-1]["vida"]

    def atualizar(self, dt):
        while len(self.particulas) < self.quantidade:
            self.criar_particula()

        for particula in self.particulas:
            particula["x"] += particula["velocidade_x"] * dt
            particula["y"] += particula["velocidade_y"] * dt
            particula["velocidade_x"] += random.uniform(-5, 5) * dt
            particula["vida"] -= dt

        self.particulas = [p for p in self.particulas if p["vida"] > 0]

    def desenhar(self, tela, x, y):
        for particula in self.particulas:
            proporcao = particula["vida"] / particula["vida_maxima"]
            imagem = pygame.transform.scale_by(self.imagem, particula["escala"])
            imagem.set_alpha(int(255 * proporcao))
            rect = imagem.get_rect(center=(x + particula["x"], y + particula["y"]))
            tela.blit(imagem, rect)