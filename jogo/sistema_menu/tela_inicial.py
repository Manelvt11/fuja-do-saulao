import os
import pygame
import pygame_gui
from sistema_menu.tela import Tela
from sistema_menu.tela_creditos import TelaCreditos

#Classe filha
#TelaInicial herda de Tela. É o menu principal: Jogar, Créditos, Sair
class TelaInicial(Tela):
    CAMINHO_CAPA = os.path.join("assets", "telas", "capa.png")
    CAMINHO_MUSICA = os.path.join("assets", "sounds", "tela_inicial_som.wav")

    def __init__(self, tela_pygame, relogio, largura, altura):
        super().__init__(tela_pygame, relogio, largura, altura, caminho_fundo=self.CAMINHO_CAPA)

        pygame.mixer.music.load(self.CAMINHO_MUSICA)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        centro_x = largura // 2 - 100

        self.botao_jogar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((centro_x, 420), (220, 55)),
            text="Jogar",
            manager=self.gerenciador,
        )

        self.botao_creditos = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((centro_x, 490), (220, 55)),
            text="Créditos",
            manager=self.gerenciador,
        )

        self.botao_sair = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((centro_x, 560), (220, 55)),
            text="Sair",
            manager=self.gerenciador,
        )

        #a TelaInicial guarda uma TelaCreditos pronta pra abrir quando o jogador clicar
        self.tela_creditos = TelaCreditos(tela_pygame, relogio, largura, altura, self.CAMINHO_CAPA)


    def processar_evento_botao(self, evento):
        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_jogar:
                pygame.mixer.music.stop()
                self.resultado = "jogar"
                self.rodando = False

            elif evento.ui_element == self.botao_creditos:
                self.tela_creditos.executar()

            elif evento.ui_element == self.botao_sair:
                pygame.mixer.music.stop()
                self.resultado = "sair"
                self.rodando = False