import pygame
import random
from sistema_personagens.player import Benício
from sistema_personagens.inimigo import Saulao
from map import Map
from hud import HUD

LARGURA = 800
ALTURA = 600

class Game:
    def __init__(self):
        self.tela_base = pygame.Surface((LARGURA, ALTURA))

        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura_tela, self.altura_tela = self.tela.get_size()

        pygame.display.set_caption("Fuja do Saulão")

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.player = Benício(LARGURA // 2, 350, 2)
        self.saulao = Saulao(400, 500, velocidade=1)
        self.mapa = Map()
        self.hud = HUD()

        self.luz = pygame.Surface((300, 300), pygame.SRCALPHA)
        for raio in range(150, 0, -1):
            transparencia = int(raio * 1.7)
            pygame.draw.circle(self.luz, (0, 0, 0, 255 - transparencia), (150, 150), raio)

        self.rodando = True
        self.DEBUG = False

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

    def atualizar(self):
        self.player.controlar(self.mapa.obstaculos)
        self.saulao.perseguir(self.player, self.mapa)

        if self.saulao.verificar_colisao_jogador(self.player):
            self.player.receber_dano()

    def desenhar(self):
        self.tela_base.fill((0, 0, 0))
        self.mapa.desenhar(self.tela_base)

        self.player.desenhar(self.tela_base)
        self.saulao.desenhar(self.tela_base)
        self.hud.desenhar(self.tela_base, self.player)

        if self.DEBUG:
            self.mapa.desenhar_debug(self.tela_base)

        # iluminação
        dark = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        flicker = random.randint(-10, 10)
        dark.fill((0, 0, 0, 140 + flicker))
        dark.blit(
            self.luz,
            (self.player.rect.centerx - 150, self.player.rect.centery - 150),
            special_flags=pygame.BLEND_RGBA_SUB
        )
        self.tela_base.blit(dark, (0, 0))

        tela_escalada = pygame.transform.scale(self.tela_base, (self.largura_tela, self.altura_tela))
        self.tela.blit(tela_escalada, (0, 0))
        pygame.display.flip()

    def rodar(self):
        while self.rodando:
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(self.FPS)