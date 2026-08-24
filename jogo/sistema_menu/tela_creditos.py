import pygame
import pygame_gui
from sistema_menu.tela import Tela

#Classe filha
#TelaCreditos herda de Tela e só implementa o que é específico dela
class TelaCreditos(Tela):
    INTEGRANTES = [
        "Manoel Vitor do Nascimento Brito",
        "Adaylton José Rodrigues Borges",
    ]

    def __init__(self, tela_pygame, relogio, largura, altura, caminho_fundo=None):
        super().__init__(tela_pygame, relogio, largura, altura, caminho_fundo)

        texto = "<br>".join([
            "<font size=6><b>FUJA DO SAULÃO</b></font>",
            "",
            "<b>Disciplina:</b> Programação Orientada a Objetos",
            "",
            "<b>Integrantes:</b>",
            "",
            *self.INTEGRANTES
        ])

        self.painel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (largura // 2 - 250, 60),
                (500, 320)
            ),
            manager=self.gerenciador
        )

        pygame_gui.elements.UITextBox(
            html_text=texto,
            relative_rect=pygame.Rect((20, 20), (460, 280)),
            manager=self.gerenciador,
            container=self.painel
        )

        self.botao_voltar = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((largura // 2 - 100, altura - 90), (220, 55)),
            text="Voltar",
            manager=self.gerenciador,
        )

    def processar_evento_botao(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.resultado = "voltar"
            self.rodando = False

        if evento.type == pygame_gui.UI_BUTTON_PRESSED:
            if evento.ui_element == self.botao_voltar:
                self.resultado = "voltar"
                self.rodando = False