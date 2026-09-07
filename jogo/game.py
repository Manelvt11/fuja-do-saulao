import pygame
import random
from sistema_personagens.player import Benício
from sistema_personagens.inimigo import Saulao
from map import Map
from hud import HUD
from camera import Camera
from sistema_itens_mistura.item import Item
from sistema_menu.tela_inicial import TelaInicial
from estado import Estado
import os
import pygame_gui
from sistema_itens_mistura.mesa_mistura import MesaMistura
from sistema_itens_mistura.porta import Porta

#tamanho da janela que o jogador vê (viewport), não é mais o tamanho do mapa
LARGURA_VIEWPORT = 800
ALTURA_VIEWPORT = 600

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Game:
    def __init__(self):
        pygame.mixer.init()

        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura_tela, self.altura_tela = self.tela.get_size()

        self.som_gameplay = os.path.join(BASE_DIR, "assets", "sounds", "som_jogo.wav")
        pygame.mixer.music.load(self.som_gameplay)
        pygame.mixer.music.set_volume(0.6)

        self.grito_morte = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "morte_estourado.wav"))
        pygame.mixer.music.set_volume(0.9)
        self.canal_morte = None
        self.grito_iniciado = False

        pygame.display.set_caption("Fuja do Saulão")

        self.gerente_ui = pygame_gui.UIManager((self.largura_tela, self.altura_tela))
        self.mesa_mistura = MesaMistura(464, 800)
        self.porta = Porta(446, 870)

        self.mapa = Map()
        self.mapa.obstaculos.append(self.mesa_mistura.rect_colisao)

        #tela_base = viewport (o que realmente aparece na tela, antes de escalar pra fullscreen)
        self.tela_base = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT))

        self.mundo = pygame.Surface((self.mapa.largura, self.mapa.altura))

        self.clock = pygame.time.Clock()
        self.FPS = 60

        x,y = self.encontrar_posicao_livre(16, 18)
        self.player = Benício(x,y, 1.3)
        self.saulao = Saulao(200, 200, velocidade=1.0)

        #cena de vitoria
        self.fase_vitoria = None
        self.tempo_fase_vitoria = 0.0
        self.pos_alvo_benicio = None
        self.pos_alvo_saulao = None
        self.fade_vitoria = 0
        self.fonte_vitoria_titulo = pygame.font.SysFont("georgia", 54, bold=True)
        self.fonte_vitoria_sub = pygame.font.SysFont("georgia", 22)

        self.hud = HUD()

        ZOOM = 2.6

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
            Item("Hidrogênio", 290, 300),
            Item("Oxigênio", 520, 510),
            Item("Oxigênio", 352, 644),
            Item("Oxigênio", 296, 236),
            Item("Enxofre", 700, 340),
            Item("Cloro", 180, 420),
            Item("Carbono", 500, 420),
            Item("Sódio", 650, 350),
            Item("Bromo", 164, 168),
            Item("Ferro", 700, 850),
        ]

        self.raio_luz = 110
        raio_nucleo = int(self.raio_luz * 0.55)
        INTENSIDADE_MAXIMA = 235

        self.luz = pygame.Surface((self.raio_luz * 2, self.raio_luz * 2), pygame.SRCALPHA)
        for raio in range(self.raio_luz, 0, -1):
            if raio <= raio_nucleo:
                alpha = INTENSIDADE_MAXIMA
            else:
                frac = (raio - raio_nucleo) / (self.raio_luz - raio_nucleo)
                alpha = int(INTENSIDADE_MAXIMA * (1 - frac))
            pygame.draw.circle(self.luz, (0, 0, 0, alpha), (self.raio_luz, self.raio_luz), raio)

        self.rodando = True
        self.DEBUG = False

        self.estado = Estado.JOGANDO
        self.tempo_morte = 0
        self.fade = 0

        self.tela_morte = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "telas", "tela_morte.jpeg")
        ).convert()



    def encontrar_posicao_livre(self, largura,altura):
        while True:
            x = random.randint(0, self.mapa.largura - largura)
            y = random.randint(0, self.mapa.altura - altura)

            rect = pygame.Rect(x, y, largura, altura)

            if not any(rect.colliderect(obs) for obs in self.mapa.obstaculos):
                return x, y

    def tratar_eventos(self):
        for evento in pygame.event.get():
            self.gerente_ui.process_events(evento)
            self.mesa_mistura.processar_evento(evento)

            if evento.type == pygame.QUIT:
                self.rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

                elif evento.key == pygame.K_e:
                    if self.estado != Estado.JOGANDO:
                        continue

                    if self.mesa_mistura.jogador_proximo(self.player):
                        self.mesa_mistura.interagir(self.player, self)

                    elif self.porta.jogador_proximo(self.player):
                        self.porta.interagir(self.player, self)

                    else:
                        self.coletar_item()

    def atualizar(self, dt):
        self.gerente_ui.update(dt)

        if self.estado == Estado.MORTE:
            self.tempo_morte += dt

            self.fade += 3

            if self.fade >= 255:
                self.fade = 255

                if not self.grito_iniciado:
                    self.canal_morte = self.grito_morte.play()
                    self.grito_iniciado = True

            if self.grito_iniciado and self.canal_morte:
                if self.tempo_morte >= 2.0:
                    self.canal_morte.fadeout(1500)

            return

        if self.estado == Estado.VITORIA:
            self.atualizar_cena_vitoria(dt)
            return

        if self.mesa_mistura.aberta:
            return

        self.player.controlar(
            self.mapa.obstaculos,
            self.mapa.largura,
            self.mapa.altura
        )

        self.saulao.atualizar_ia(self.player, self.mapa)
    
        if self.saulao.verificar_colisao_jogador(self.player):
            self.player.receber_dano()
    
        if self.player.vida <= 0:
            self.estado = Estado.MORTE
            self.tempo_morte = 0
            self.fade = 0

            pygame.mixer.music.fadeout(1000)

            self.canal_morte = None
            self.grito_iniciado = False

    def desenhar(self):
        self.mundo.fill((0, 0, 0))
        self.mapa.desenhar(self.mundo)

        for item in self.itens:
            item.desenhar(self.mundo)

        self.mesa_mistura.desenhar(self.mundo)
        self.porta.desenhar(self.mundo)

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

        # HUD e lanterna só aparecem durante o jogo normal (somem na cutscene de vitória)
        if self.estado != Estado.VITORIA:
            self.hud.desenhar(self.tela_base, self.player)

            px_tela, py_tela = self.camera.mundo_para_tela(
                self.player.rect.centerx, self.player.rect.centery
            )

            dark = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT), pygame.SRCALPHA)
            flicker = random.randint(-10, 10)
            dark.fill((0, 0, 0, 160 + flicker))
            dark.blit(
                self.luz,
                (px_tela - self.raio_luz, py_tela - self.raio_luz),
                special_flags=pygame.BLEND_RGBA_SUB
            )
            self.tela_base.blit(dark, (0, 0))

        # tela de morte
        if self.estado == Estado.MORTE:
            if self.fade < 255:
                fade = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT))
                fade.fill((0, 0, 0))
                fade.set_alpha(self.fade)
                self.tela_base.blit(fade, (0, 0))
            else:
                imagem = pygame.transform.scale(
                    self.tela_morte,
                    (LARGURA_VIEWPORT, ALTURA_VIEWPORT)
                )
                self.tela_base.blit(imagem, (0, 0))

        # overlay final da cutscene de vitória (só aparece quando ela "congela")
        if self.estado == Estado.VITORIA and self.fase_vitoria == "congelado":
            overlay = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.fade_vitoria))
            self.tela_base.blit(overlay, (0, 0))

            alpha_texto = min(255, int(self.fade_vitoria * 1.5))
            titulo = self.fonte_vitoria_titulo.render("PARABÉNS!", True, (255, 240, 210))
            subtitulo = self.fonte_vitoria_sub.render("Você venceu!", True, (230, 220, 210))
            titulo.set_alpha(alpha_texto)
            subtitulo.set_alpha(alpha_texto)

            self.tela_base.blit(
                titulo,
                titulo.get_rect(center=(LARGURA_VIEWPORT // 2, ALTURA_VIEWPORT // 2 - 20)),
            )
            self.tela_base.blit(
                subtitulo,
                subtitulo.get_rect(center=(LARGURA_VIEWPORT // 2, ALTURA_VIEWPORT // 2 + 30)),
            )

        # escala tudo pra resolução real da tela (fullscreen)
        tela_escalada = pygame.transform.scale(
            self.tela_base,
            (self.largura_tela, self.altura_tela)
        )

        self.tela.blit(tela_escalada, (0, 0))

        # UI do pygame_gui (mesa de mistura) sempre por cima de tudo, sem escalar
        self.gerente_ui.draw_ui(self.tela)

        pygame.display.flip()

    def coletar_item(self):
        for item in self.itens:
            if item.coletado:
                continue

            if item.rect.colliderect(self.player.rect):
                if self.player.inventario.adicionar_item(item):
                    item.coletado = True
                return

    def iniciar_cena_vitoria(self):
        self.estado = Estado.VITORIA
        self.fase_vitoria = "correndo"
        self.tempo_fase_vitoria = 0.0
        self.pos_inicial_benicio = (self.player.rect.x, self.player.rect.y)

        # ponto um pouco além da porta
        self.pos_alvo_benicio = (self.porta.rect.centerx + 120, self.porta.rect.centery)
        self.pos_alvo_saulao = (self.porta.rect.centerx, self.porta.rect.centery)

        pygame.mixer.music.fadeout(1000)

    def atualizar_cena_vitoria(self, dt):
        self.tempo_fase_vitoria += dt

        if self.fase_vitoria == "correndo":
            duracao = 1.6
            t = min(self.tempo_fase_vitoria / duracao, 1.0)

            x0, y0 = self.pos_inicial_benicio
            x1, y1 = self.pos_alvo_benicio
            self.player.rect.x = int(x0 + (x1 - x0) * t)
            self.player.rect.y = int(y0 + (y1 - y0) * t)

            dx, dy = x1 - x0, y1 - y0
            if abs(dx) > abs(dy):
                self.player.direcao = "direita" if dx > 0 else "esquerda"
            else:
                self.player.direcao = "baixo" if dy > 0 else "cima"

            self.player.animar(True)
            self.camera.atualizar(self.player.rect)

            if t >= 1.0:
                self.fase_vitoria = "saulao_aparece"
                self.tempo_fase_vitoria = 0.0
                self.saulao.rect.x, self.saulao.rect.y = self.pos_alvo_saulao
                self.saulao.direcao = "baixo"
                self.saulao.frame_atual = 0

        elif self.fase_vitoria == "saulao_aparece":
            duracao = 0.9
            self.player.animar(False)  #Benício parado, olhando pra trás
            self.camera.atualizar(self.player.rect)

            if self.tempo_fase_vitoria >= duracao:
                self.fase_vitoria = "congelado"
                self.tempo_fase_vitoria = 0.0
                self.fade_vitoria = 0

        elif self.fase_vitoria == "congelado":
            self.fade_vitoria = min(self.fade_vitoria + 4, 200)
        

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

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.som_gameplay)
        pygame.mixer.music.play(loops=-1)#-1 = repete pra sempre

        while self.rodando:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()