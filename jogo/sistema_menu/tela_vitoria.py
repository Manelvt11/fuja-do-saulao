import os
from sistema_menu.tela import Tela

class TelaVitoria(Tela):
    CAMINHO_VITORIA = os.path.join("assets", "telas", "tela_vitoria.png")

    def __init__(self, tela_pygame, relogio, largura, altura, caminho_fundo=None):
        super().__init__(tela_pygame, relogio, largura, altura, caminho_fundo=self.CAMINHO_VITORIA)

    def processar_evento_botao(self, evento):
        pass