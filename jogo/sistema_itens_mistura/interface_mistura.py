import pygame
import pygame_gui
from sistema_itens_mistura.icones import obter_icone

class InterfaceMistura:
    LARGURA_BASE = 1365
    ALTURA_BASE = 768

    def __init__(self, game):
        self.game = game

        self.aberta = False
        self.fundo = None

        self.botoes_itens = {}
        self.icones_itens = []

        self.labels_selecionados = []
        self.icones_selecionados = []

        self.botao_misturar = None
        self.botao_fechar = None

        self.label_feedback = None

    #escala
    def sx(self, valor):
        return int(valor * self.game.largura_tela / self.LARGURA_BASE)

    def sy(self, valor):
        return int(valor * self.game.altura_tela / self.ALTURA_BASE)

    def abrir(self, jogador):
        self.aberta = True
        self.limpar()

        largura = self.game.largura_tela
        altura = self.game.altura_tela

        self.fundo = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(
                0, 
                0, 
                largura, 
                altura
            ),
            image_surface=pygame.transform.smoothscale(
                self.game.mesa_mistura.interface,
                (largura, altura)
            ),
            manager=self.game.gerente_ui
        )

        #itens do inventario
        self.botoes_itens = {}
        self.icones_itens = []

        itens = list(jogador.inventario.itens)

        posicoes = [
            (125, 190),
            (125, 300),
            (125, 410),
        ]

        for i, item in enumerate(itens[:3]):
            x,y = posicoes[i]

            icone_surface = obter_icone(
                item.nome,
                tamanho=50
            )

            icone =pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(
                    self.sx(x),
                    self.sy(y) + self.sy(7),
                    self.sx(50),
                    self.sy(50)
                ),
                image_surface=icone_surface,
                manager=self.game.gerente_ui
            )

            self.icones_itens.append(icone)

            #botao
            botao = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    self.sx(x + 63),
                    self.sy(y),
                    self.sx(227),
                    self.sy(65)
                ),
                text=item.nome,
                manager=self.game.gerente_ui
            )

            self.botoes_itens[botao] = item

        #botao misturar
        self.botao_misturar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                self.sx(500),
                self.sy(670),
                self.sx(190),
                self.sy(55)
            ),
            text="MISTURAR",
            manager=self.game.gerente_ui
        )

        #botao sair
        self.botao_fechar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                self.sx(1030),
                self.sy(670),
                self.sx(190),
                self.sy(55)
            ),
            text="SAIR",
            manager=self.game.gerente_ui
        )

        #feedback
        self.label_feedback = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                self.sx(480),
                self.sy(610),
                self.sx(410),
                self.sy(45)
            ),
            text="",
            manager=self.game.gerente_ui
        )


    def atualizar_selecionados(self, selecionados):
        self.limpar_selecionados()

        for i, item in enumerate(selecionados):
            if i>=3:
                break

            y=240 + i * 100

            #icone
            icone_surface = obter_icone(item.nome, tamanho=45)
            icone = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(
                    self.sx(510),
                    self.sy(y) + self.sy(5),
                    self.sx(45),
                    self.sy(45)
                ),
                image_surface=icone_surface,
                manager=self.game.gerente_ui
            )
            self.icones_selecionados.append(icone)

            #nome
            label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(
                    self.sx(565),
                    self.sy(y),
                    self.sx(335),
                    self.sy(55)
                ),
                text=item.nome,
                manager=self.game.gerente_ui
            )
            self.labels_selecionados.append(label)

    def mostrar_feedback(self, mensagem):
        if self.label_feedback:
            self.label_feedback.set_text(mensagem)

    def limpar_selecionados(self):
        for label in self.labels_selecionados:
            label.kill()

        for icone in self.icones_selecionados:
            icone.kill()

        self.labels_selecionados.clear()
        self.icones_selecionados.clear()

    def limpar(self):
        if self.fundo:
            self.fundo.kill()

        if self.label_feedback:
            self.label_feedback.kill()

        if self.botao_misturar:
            self.botao_misturar.kill()

        if self.botao_fechar:
            self.botao_fechar.kill()

        for botao in self.botoes_itens:
            botao.kill()

        for icone in self.icones_itens:
            icone.kill()

        self.limpar_selecionados()

        self.fundo = None
        self.label_feedback = None
        self.botao_fechar = None
        self.botoes_itens.clear()
        self.icones_itens.clear()

    def fechar(self):
        self.limpar()
        self.aberta = False