import pygame

class ObjetoMapa:
    #base para objetos fixos do mapa com os quais o jogador pode interagir.
    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(
            x,
            y,
            largura,
            altura
        )

    def jogador_proximo(self, jogador, raio_extra=12):
        area_interacao = self.rect.inflate(raio_extra * 2, raio_extra * 2)
        return area_interacao.colliderect(jogador.rect)

    def interagir(self, jogador, game):
        pass

    def desenhar(self, tela):
        pass