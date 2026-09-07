import pygame
from sistema_itens_mistura.objeto_mapa import ObjetoMapa
from sistema_itens_mistura.receitas import buscar_receita
from sistema_itens_mistura.item_resultado import ItemResultado
import os
from sistema_itens_mistura.interface_mistura import InterfaceMistura
import pygame_gui

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class MesaMistura(ObjetoMapa):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 24)

        self.imagem = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "objetos", "mesa_mistura.png")
        ).convert_alpha()

        self.imagem = pygame.transform.scale(self.imagem, (60, 57))

        self.imagem_rect = self.imagem.get_rect(
            midbottom=(self.rect.centerx, self.rect.bottom + 8)
        )

        # Colisão física da mesa
        self.rect_colisao = pygame.Rect(
            self.imagem_rect.left + 4,
            self.imagem_rect.top + 18,
            self.imagem_rect.width - 8,
            self.imagem_rect.height - 18
        )

        # Área de interação
        self.rect_interacao = pygame.Rect(
            self.rect_colisao.left - 9,
            self.rect_colisao.top - 9,
            self.rect_colisao.width + 18,
            self.rect_colisao.height + 18
        )

        self.interface = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "objetos", "interface_mesa_mistura.jpg")
        ).convert()

        self.ui = None

        self.aberta = False
        self.jogador_ref = None
        self.game_ref = None
        self.selecionados = []

    def jogador_proximo(self, jogador, raio_extra=0):
        return self.rect_interacao.colliderect(jogador.rect)

    def interagir(self, jogador, game):
        if self.aberta:
            return

        self.abrir(jogador, game)

    def abrir(self, jogador, game):
        if self.aberta:
            return

        self.aberta = True
        self.jogador_ref = jogador
        self.game_ref = game

        self.selecionados.clear()

        self.ui = InterfaceMistura(game)

        #interface precisa acessar a imagem da mesa
        game.mesa_mistura = self
        self.ui.abrir(jogador)

    def fechar(self):
        if self.ui:
            self.ui.fechar()

        self.ui = None
        self.aberta = False
        self.selecionados.clear()
        self.jogador_ref = None
        self.game_ref = None

    def processar_evento(self, evento):
        if not self.aberta:
            return

        if evento.type != pygame_gui.UI_BUTTON_PRESSED:
            return

        #sair
        if evento.ui_element == self.ui.botao_fechar:
            self.fechar()
            return

        #misturar
        if evento.ui_element == self.ui.botao_misturar:
            self._tentar_misturar()
            return

        #item clicado
        item_clicado = self.ui.botoes_itens.get(evento.ui_element)

        if item_clicado is None:
            return

        #remover se ja tiver selecionado
        if item_clicado in self.selecionados:
            self.selecionados.remove(item_clicado)

            evento.ui_element.unselect()

        #adicionar
        else:
            if len(self.selecionados) >= 3:
                self.ui.mostrar_feedback("Você pode selecionar no máximo 3 itens")
                return

            self.selecionados.append(item_clicado)
            evento.ui_element.select()

        self.ui.atualizar_selecionados(self.selecionados)

    def _tentar_misturar(self):
        if len(self.selecionados) < 2:
            self.ui.mostrar_feedback(
                "Selecione pelo menos 2 itens"
            )
            return

        #buscar receita
        nomes = [item.nome for item in self.selecionados]
        resultado_nome = buscar_receita(nomes)

        #receita inexistente
        if resultado_nome is None:
            self.ui.mostrar_feedback("Nada aconteceu...")

            self._limpar_selecao()
            return

        #remover ingredientes
        for item in self.selecionados:
            self.jogador_ref.inventario.remover_item(item)

        #criar resultado
        novo_item = ItemResultado(resultado_nome)

        self.jogador_ref.inventario.adicionar_item(novo_item)

        #mensagem
        mensagem = f"Você criou: {resultado_nome}!"

        #limpar seleção
        self._limpar_selecao()

        #atualizar interface
        self.ui.abrir(self.jogador_ref)
        self.ui.mostrar_feedback(mensagem)

    def _limpar_selecao(self):
        for botao in self.ui.botoes_itens:
            botao.unselect()

        self.selecionados.clear()
        self.ui.atualizar_selecionados(self.selecionados)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.imagem_rect)