from sistema_itens_mistura.objeto_mapa import ObjetoMapa
from sistema_itens_mistura.receitas import ITEM_FINAL

class Porta(ObjetoMapa):
    def __init__(self, x, y):
        super().__init__(x, y, 48, 64)
        self.trancada = True

    def interagir(self, jogador, game):
        tem_item_final = any(item.nome == ITEM_FINAL for item in jogador.inventario.itens)

        if tem_item_final:
            self.trancada = False
            game.iniciar_cutscene_vitoria()
        else:
            print("A porta está trancada. Falta algo...")

    def desenhar(self, tela):
        import pygame
        cor = (60, 60, 70) if self.trancada else (40, 200, 90)
        pygame.draw.rect(tela, cor, self.rect)