import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TelaDerrota:
    def __init__(self, tela, clock, largura, altura):
        self.tela = tela
        self.clock = clock
        self.largura = largura
        self.altura = altura

        self.imagem = pygame.image.load(os.path.join(BASE_DIR, "assets", "telas", "tela_morte.jpeg")).convert()
        self.imagem = pygame.transform.scale(self.imagem, (self.largura, self.altura))

        self.grito_morte = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sounds", "morte_estourado.wav"))

    def executar(self, tela_anterior):
        fade = 0
        terminou_fade = False
        grito_iniciado = False
        rodando = True

        while rodando:
            self.clock.tick(60)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False

            if not terminou_fade:
                self.tela.blit(tela_anterior, (0, 0))

                camada = pygame.Surface((self.largura, self.altura))
                camada.fill((0, 0, 0))
                camada.set_alpha(fade)

                self.tela.blit(camada, (0, 0))

                fade += 5

                if fade >= 255:
                    fade = 255
                    terminou_fade = True

            else:
                self.tela.blit(self.imagem, (0, 0))

                if not grito_iniciado:
                    self.grito_morte.play()
                    grito_iniciado = True

            pygame.display.flip()