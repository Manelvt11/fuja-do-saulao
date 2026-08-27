import pygame
import random
from sistema_personagens.player import Benício
from sistema_personagens.inimigo import Saulao
from map import Map
from hud import HUD
from camera import Camera
from sistema_itens_mistura.item import Item
from sistema_menu.tela_inicial import TelaInicial

#tamanho da janela que o jogador vê (viewport), não é mais o tamanho do mapa
LARGURA_VIEWPORT = 800
ALTURA_VIEWPORT = 600

class Game:
    def __init__(self):
        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura_tela, self.altura_tela = self.tela.get_size()

        pygame.display.set_caption("Fuja do Saulão")

        self.mapa = Map()

        #tela_base = viewport (o que realmente aparece na tela, antes de escalar pra fullscreen)
        self.tela_base = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT))

        self.mundo = pygame.Surface((self.mapa.largura, self.mapa.altura))

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.player = Benício(self.mapa.largura // 2, self.mapa.altura // 2, 1.5)
        self.saulao = Saulao(200, 200, velocidade=1)
        self.hud = HUD()

        ZOOM = 2

        self.camera = Camera(
            LARGURA_VIEWPORT, ALTURA_VIEWPORT,
            self.mapa.largura, self.mapa.altura,
            zoom=ZOOM
        )

        #superfície reutilizada todo frame pra guardar o recorte do mundo
        #antes de ampliar (evita recriar a Surface a cada desenhar())
        self.recorte = pygame.Surface(
            (self.camera.largura_captura, self.camera.altura_captura)
        )

        self.itens = [
            Item("Hidrogênio", 0, 290, 300),
            Item("Oxigênio", 1, 520, 510),
            Item("Enxofre", 2, 700, 340),
            Item("Cloro", 3, 180, 420),
            Item("Carbono", 4, 500, 420),
            Item("Sódio", 5, 650, 350),
        ]

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

                elif evento.key == pygame.K_e:
                    self.coletar_item()


    def atualizar(self):
        self.player.controlar(self.mapa.obstaculos, self.mapa.largura, self.mapa.altura)
        self.saulao.perseguir(self.player, self.mapa)

        if self.saulao.verificar_colisao_jogador(self.player):
            self.player.receber_dano()

    def desenhar(self):
        self.mundo.fill((0, 0, 0))
        self.mapa.desenhar(self.mundo)

        for item in self.itens:
            item.desenhar(self.mundo)

        self.player.desenhar(self.mundo)
        self.saulao.desenhar(self.mundo)

        if self.DEBUG:
            self.mapa.desenhar_debug(self.mundo)

        #atualiza a câmera, recorta a área capturada e amplia pra caber na viewport
        self.camera.atualizar(self.player.rect)
        self.recorte.blit(self.mundo, (0, 0), self.camera.area_visivel())

        recorte_escalado = pygame.transform.scale(
            self.recorte, (LARGURA_VIEWPORT, ALTURA_VIEWPORT)
        )
        self.tela_base.blit(recorte_escalado, (0, 0))

        self.hud.desenhar(self.tela_base, self.player)

        # iluminação: posição do jogador precisa ser convertida de mundo pra tela
        px_tela, py_tela = self.camera.mundo_para_tela(
            self.player.rect.centerx, self.player.rect.centery
        )

        dark = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT), pygame.SRCALPHA)
        flicker = random.randint(-10, 10)
        dark.fill((0, 0, 0, 140 + flicker))
        dark.blit(
            self.luz,
            (px_tela - 150, py_tela - 150),
            special_flags=pygame.BLEND_RGBA_SUB
        )
        self.tela_base.blit(dark, (0, 0))

        tela_escalada = pygame.transform.scale(self.tela_base, (self.largura_tela, self.altura_tela))
        self.tela.blit(tela_escalada, (0, 0))
        pygame.display.flip()

    def coletar_item(self):
        for item in self.itens:
            if item.coletado:
                continue

            if self.player.rect.colliderect(item.rect):
                sucesso = self.player.inventario.adicionar_item(item)

                if sucesso:
                    item.coletado = True
                    print(f"{item.nome} coletado!")

                return

    def rodar(self):
        tela_inicial = TelaInicial(
            self.tela,
            self.clock,
            self.largura_tela,
            self.altura_tela
        )

        resultado = tela_inicial.executar()

        if resultado != "jogar":
            return

        while self.rodando:
            self.tratar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(self.FPS)