from sistema_itens_mistura.icones import obter_icone
import pygame

class Item:
    #aparece no mapa e é coletado pelo jogador
    def __init__(self, nome, x, y, tamanho=48):
        self.nome = nome
        self.rect = pygame.Rect(0, 0, tamanho, tamanho)
        self.rect.center = (x, y)
        self.coletado = False
        self.imagem = obter_icone(nome, tamanho=tamanho)

    def desenhar(self, tela):
        if self.coletado:
            return

        if self.imagem is not None:
            tela.blit(self.imagem, self.rect)
