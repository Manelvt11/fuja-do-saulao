import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Diario:
    def __init__(self, tela=None, clock=None):
        self.tela = tela
        self.clock = clock
        self.paginas = []

        for numero in range(1, 13):
            caminho = os.path.join(BASE_DIR, "assets", "diario", f"pag{numero}.png")
            pagina = pygame.image.load(caminho).convert_alpha()
            self.paginas.append(pagina)

        self.pagina_atual = 0

        caminho_estrutura = os.path.join(BASE_DIR, "assets", "diario", "estrutura_diario.png")
        self.estrutura = pygame.image.load(caminho_estrutura).convert_alpha()

    def desenhar(self, tela, fundo):
        largura_tela = tela.get_width()
        altura_tela = tela.get_height()

        #fundo do laboratório
        tamanho_blur = (max(1, largura_tela // 10), max(1, altura_tela // 10))
        fundo_blur = pygame.transform.smoothscale(fundo, tamanho_blur)
        fundo_blur = pygame.transform.smoothscale(fundo_blur, tela.get_size())
        tela.blit(fundo_blur, (0, 0))

        sombra = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 150))
        tela.blit(sombra, (0, 0))

        #tamanho do diário
        largura_diario = int(largura_tela * 0.94)
        altura_diario = int(self.estrutura.get_height() * (largura_diario / self.estrutura.get_width()))
        estrutura = pygame.transform.smoothscale(self.estrutura, (largura_diario, altura_diario))

        x_diario = (largura_tela - largura_diario) // 2
        y_diario = (altura_tela - altura_diario) // 2
        tela.blit(estrutura, (x_diario, y_diario))

        #area das páginas
        esquerda_x = int(largura_diario * 0.095)
        esquerda_y = int(altura_diario * 0.135)
        esquerda_largura = int(largura_diario * 0.35)
        esquerda_altura = int(altura_diario * 0.73)
        
        direita_x = int(largura_diario * 0.555)
        direita_y = int(altura_diario * 0.135)
        direita_largura = int(largura_diario * 0.35)
        direita_altura = int(altura_diario * 0.73)

        #página esquerda
        if self.pagina_atual < len(self.paginas):
            pagina_esquerda = pygame.transform.smoothscale(self.paginas[self.pagina_atual], (esquerda_largura, esquerda_altura))
            tela.blit(pagina_esquerda, (x_diario + esquerda_x, y_diario + esquerda_y))

        #página direita
        proxima_pagina = self.pagina_atual + 1

        if proxima_pagina < len(self.paginas):
            pagina_direita = pygame.transform.smoothscale(self.paginas[proxima_pagina], (direita_largura, direita_altura))
            tela.blit(pagina_direita, (x_diario + direita_x, y_diario + direita_y))

        #número das páginas
        fonte = pygame.font.SysFont("arial", 18, bold=True)

        if proxima_pagina < len(self.paginas):
            texto = fonte.render(f"{self.pagina_atual + 1}-{proxima_pagina + 1} / {len(self.paginas)}", True, (190, 190, 190))

        else:
            texto = fonte.render(f"{self.pagina_atual + 1} / {len(self.paginas)}", True, (190, 190, 190))

        texto_rect = texto.get_rect(center=(largura_tela // 2, altura_tela - 28))
        tela.blit(texto, texto_rect)