import pygame
import pygame_gui
import sys
import os

PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_TEMA = os.path.join(PASTA_RAIZ, "assets", "tema.json")

#Classe pai
#a classe Tela possui características comuns para todas as telas do jogo, como:
#janela, relógio, fundo, gerenciador de UI(pygame_gui) e o loop principal
class Tela:
    def __init__(self, tela_pygame, relogio, largura, altura, caminho_fundo=None):
        self.tela = tela_pygame
        self.relogio = relogio
        self.largura = largura
        self.altura = altura
        self.fps = 60

        #gerenciador da UI do pygame_gui
        if os.path.exists(CAMINHO_TEMA):
            self.gerenciador = pygame_gui.UIManager((largura, altura), CAMINHO_TEMA)
        
        else:
            self.gerenciador = pygame_gui.UIManager((largura, altura))

        self.fundo = self.carregar_fundo(caminho_fundo) if caminho_fundo else None

        self.rodando = True
        self.resultado = None  # cada tela filha define o que ela retorna no final

    def carregar_fundo(self, caminho):
        #se o caminho não for absoluto, monta a partir da raiz do projeto
        
        if not os.path.isabs(caminho):
            caminho = os.path.join(PASTA_RAIZ, caminho)

        try:
            imagem = pygame.image.load(caminho).convert()
            imagem = pygame.transform.smoothscale(imagem, (self.largura, self.altura))
        
        except (pygame.error, FileNotFoundError) as erro:
            print(f"Não foi possível carregar a imagem de fundo: {caminho}")
            print(f"Erro: {erro}")
            imagem = pygame.Surface((self.largura, self.altura))
            imagem.fill((10, 10, 10))
        
        return imagem

    def desenhar_fundo(self):
        if self.fundo:
            self.tela.blit(self.fundo, (0, 0))
        
        else:
            self.tela.fill((10, 10, 10))

    #esse método é sobrescrito (override) por cada tela filha,
    #pra tratar o clique dos seus próprios botões
    def processar_evento_botao(self, evento):
        raise NotImplementedError("A tela filha precisa implementar processar_evento_botao()")


    def executar(self):
        self.rodando = True
        self.resultado = None

        while self.rodando:
            delta_tempo = self.relogio.tick(self.fps) / 1000.0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.processar_evento_botao(evento)
                self.gerenciador.process_events(evento)

            self.gerenciador.update(delta_tempo)

            self.desenhar_fundo()

            sombra = pygame.Surface((280, 220), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 130))

            self.tela.blit(sombra, (self.largura // 2 - 140, 400))
            
            self.gerenciador.draw_ui(self.tela)

            pygame.display.flip()

        return self.resultado