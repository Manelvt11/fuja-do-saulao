import pygame

#Classe responsável por controlar qual parte do mapa é visível na tela
#Segue o jogador e nunca deixa a janela mostrar área fora do mapa
#Também suporta "zoom": quanto maior o zoom, menor a área do mundo capturada
class Camera:
    def __init__(self, largura_viewport, altura_viewport, largura_mapa, altura_mapa, zoom=1.0):
        self.largura_viewport = largura_viewport
        self.altura_viewport = altura_viewport
        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa
        self.zoom = zoom

        #tamanho real da área que a câmera captura antes de ampliar
        self.largura_captura = int(largura_viewport / zoom)
        self.altura_captura = int(altura_viewport / zoom)

        self.x = 0
        self.y = 0

    def atualizar(self, alvo_rect):
        #centraliza a câmera no jogador, usando a área de captura (não o viewport)
        self.x = alvo_rect.centerx - self.largura_captura // 2
        self.y = alvo_rect.centery - self.altura_captura // 2

        #clampa pra não mostrar área fora do mapa
        self.x = max(0, min(self.x, self.largura_mapa - self.largura_captura))
        self.y = max(0, min(self.y, self.altura_mapa - self.altura_captura))

    def area_visivel(self):
        return pygame.Rect(self.x, self.y, self.largura_captura, self.altura_captura)

    def mundo_para_tela(self, x, y):
        #converte uma coordenada do mundo pra coordenada de tela já considerando o zoom
        rel_x = x - self.x
        rel_y = y - self.y
        return int(rel_x * self.zoom), int(rel_y * self.zoom)