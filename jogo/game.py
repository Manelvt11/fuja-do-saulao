import pygame
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
from tema_ui import montar_tema
from sistema_diario.diario import Diario
from sistema_menu.tela_vitoria import TelaVitoria
from sistema_personagens.estado_benicio import EstadoBenicio
from sistema_menu.tela_derrota import TelaDerrota
from sistema_ambientacao.iluminacao import Iluminacao
from sistema_ambientacao.fendas_estranheza import FendasEstranheza

#tamanho da janela que o jogador vê (viewport), não é mais o tamanho do mapa
LARGURA_VIEWPORT = 800
ALTURA_VIEWPORT = 600

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Game:
    def __init__(self):
        #tela e configurações
        pygame.mixer.init()

        self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largura_tela, self.altura_tela = self.tela.get_size()

        pygame.display.set_caption("Fuja do Saulão")

        self.som_gameplay = os.path.join(BASE_DIR, "assets", "sounds", "som_jogo.wav")
        pygame.mixer.music.load(self.som_gameplay)
        pygame.mixer.music.set_volume(0.6)

        self.clock = pygame.time.Clock()
        self.FPS = 60

        #interface
        caminho_tema = montar_tema(BASE_DIR)
        self.gerente_ui = pygame_gui.UIManager((self.largura_tela, self.altura_tela), caminho_tema)
        self.gerente_ui.preload_fonts([
            {'name': 'arial', 'point_size': 18, 'style': 'bold', 'antialiased': '1'}
        ])

        #mapa
        self.mapa = Map()

        self.fendas_estranheza = FendasEstranheza(self.mapa.estranheza)

        #sistemas do mapa
        self.mesa_mistura = MesaMistura(464, 800)
        self.porta = Porta(446, 870)
        self.mapa.obstaculos.append(self.mesa_mistura.rect_colisao)

        #superficies do jogo
        #tela_base = viewport (o que realmente aparece na tela, antes de escalar pra fullscreen)
        self.tela_base = pygame.Surface((LARGURA_VIEWPORT, ALTURA_VIEWPORT))
        self.mundo = pygame.Surface((self.mapa.largura, self.mapa.altura))

        #personagens
        x,y = self.mapa.encontrar_posicao_livre(16, 18)
        self.player = Benício(x,y, 1.3)
        self.saulao = Saulao(200, 200, velocidade=1.0)
        self.saulao.estranhesaulon = True

        #telas de resultado
        #cena de vitoria
        self.tela_vitoria = TelaVitoria(self.tela, self.clock, self.largura_tela, self.altura_tela)
        #cena de derrota
        self.tela_derrota = TelaDerrota(self.tela, self.clock, self.largura_tela, self.altura_tela)

        #interface do jogo
        self.hud = HUD()

        self.diario = Diario(self.tela_base, self.clock)
        self.diario_aberto = False

        #câmera
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

        #itens
        self.itens = [
            Item(nome, x, y)
            for nome,x,y in self.mapa.itens
        ]

        #ambientação
        self.iluminacao = Iluminacao()

        #estado do jogo
        self.rodando = True
        self.DEBUG = False
        self.estado = Estado.JOGANDO
        self.tempo_restante = 7 * 60


        

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if self.diario_aberto:
                if evento.type == pygame.QUIT:
                    self.rodando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.diario_aberto = False

                    elif evento.key == pygame.K_RIGHT:
                        if self.diario.pagina_atual + 2 < len(self.diario.paginas):
                            self.diario.pagina_atual += 2

                    elif evento.key == pygame.K_LEFT:
                        if self.diario.pagina_atual - 2 >= 0:
                            self.diario.pagina_atual -= 2
                continue

            self.gerente_ui.process_events(evento)
            self.mesa_mistura.processar_evento(evento)

            if evento.type == pygame.QUIT:
                self.rodando = False
                continue

            if evento.type != pygame.KEYDOWN:
                continue

            if evento.key == pygame.K_ESCAPE:
                    self.rodando = False

            elif evento.key == pygame.K_F1:
                if self.estado == Estado.JOGANDO:
                    self.diario_aberto = True

            elif evento.key == pygame.K_e:
                if self.estado != Estado.JOGANDO:
                    continue

                if self.mesa_mistura.jogador_proximo(self.player):
                    self.mesa_mistura.interagir(self.player, self)

                elif self.porta.jogador_proximo(self.player):
                    self.porta.interagir(self.player, self)

                else:
                    self.coletar_item()

            elif evento.key == pygame.K_q:
                if self.estado == Estado.JOGANDO:
                    self.dropar_item()

    def atualizar(self, dt):
        self.gerente_ui.update(dt)

        if self.diario_aberto:
            return

        if self.estado != Estado.JOGANDO:
            return

        self.tempo_restante -= dt

        self.fendas_estranheza.atualizar(dt)

        if self.tempo_restante <= 0:
            self.tempo_restante = 0
            self.iniciar_derrota()
            return

        if self.mesa_mistura.aberta:
            return

        self.player.controlar(
            self.mapa.obstaculos,
            self.mapa.largura,
            self.mapa.altura
        )
        self.player.atualizar_estado()

        if self.player.estado == EstadoBenicio.MORTO:
            self.iniciar_derrota()
            return

        self.saulao.atualizar_ia(self.player, self.mapa)
        self.saulao.atualizar_animacao(self.player)
        self.saulao.atualizar_flutuacao(dt)

    def desenhar(self):
        #mundo
        self.mundo.fill((0, 0, 0))
        self.mapa.desenhar(self.mundo)

        for item in self.itens:
            item.desenhar(self.mundo)

        self.mesa_mistura.desenhar(self.mundo)
        self.porta.desenhar(self.mundo)

        self.fendas_estranheza.desenhar(self.mundo)

        personagens = [self.player, self.saulao]
        personagens.sort(key=lambda personagem: personagem.rect.bottom)
        for personagem in personagens:
            personagem.desenhar(self.mundo)

        #debug
        if self.DEBUG:
            self.mapa.desenhar_debug(self.mundo)

        #câmera
        #atualiza a câmera, recorta a área capturada e amplia pra caber na viewport
        self.camera.atualizar(self.player.rect)
        self.recorte.blit(self.mundo, (0, 0), self.camera.area_visivel())

        recorte_escalado = pygame.transform.scale(
            self.recorte, (LARGURA_VIEWPORT, ALTURA_VIEWPORT)
        )
        self.tela_base.blit(recorte_escalado, (0, 0))

        #HUD e ambientação
        # HUD e lanterna só aparecem durante o jogo normal
        if self.estado != Estado.VITORIA:
            self.hud.desenhar(self.tela_base, self.player, self.tempo_restante)

            px_tela, py_tela = self.camera.mundo_para_tela(
                self.player.rect.centerx, self.player.rect.centery
            )

            self.iluminacao.aplicar(self.tela_base, px_tela, py_tela)

        #tela fullscreen
        tela_escalada = pygame.transform.scale(self.tela_base, (self.largura_tela, self.altura_tela))
        self.tela.blit(tela_escalada, (0, 0))

        #interfaces sobre a tela
        if self.diario_aberto:
            fundo = self.tela.copy()
            self.diario.desenhar(self.tela, fundo)
        else:
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

    def dropar_item(self):
        if not self.player.inventario.itens:
            return

        item = self.player.inventario.itens[-1]
        self.player.inventario.remover_item(item)
        item.coletado = False
        item.rect.center = self.player.rect.center

    def iniciar_vitoria(self):
        self.estado = Estado.VITORIA
        self.rodando = False
        pygame.mixer.music.fadeout(1000)

    def iniciar_derrota(self):
        self.estado = Estado.DERROTA
        self.rodando = False
        pygame.mixer.music.fadeout(1000)

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

        if self.estado == Estado.VITORIA:
            self.tela_vitoria.executar()

        if self.estado == Estado.DERROTA:
            self.tela_derrota.executar(self.tela.copy())