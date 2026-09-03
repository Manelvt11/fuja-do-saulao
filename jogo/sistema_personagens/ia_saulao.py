import pygame
import heapq

class SaulaoIA:
    def __init__(self, saulao):
        self.saulao = saulao

        self.rota = []
        self.indice_rota = 0
        self.alvo_anterior = None

        self.intervalo_rota = 20
        self.tempo_rota = 0

    def atualizar(self, jogador, mapa):
        self.tempo_rota += 1

        tile = mapa.tile_size

        inicio = (
            self.saulao.rect.centerx // tile,
            self.saulao.rect.centery // tile
        )

        alvo = (
            jogador.rect.centerx // tile,
            jogador.rect.centery // tile
        )

        # Se estiver perto, vai direto para o jogador
        distancia = pygame.Vector2(
            jogador.rect.center
        ).distance_to(self.saulao.rect.center)

        if distancia < tile * 2:
            dx = jogador.rect.centerx - self.saulao.rect.centerx
            dy = jogador.rect.centery - self.saulao.rect.centery

            self._mover(dx, dy, mapa)
            return

        # Cria uma nova rota quando necessário
        if (
            not self.rota
            or self.tempo_rota >= self.intervalo_rota
            or self.alvo_anterior != alvo
        ):
            self.rota = self._calcular_rota(
                inicio,
                alvo,
                mapa
            )

            self.indice_rota = 0
            self.alvo_anterior = alvo
            self.tempo_rota = 0

        if not self.rota:
            return

        # Pega o próximo ponto da rota
        if self.indice_rota >= len(self.rota):
            return

        coluna, linha = self.rota[self.indice_rota]

        destino_x = coluna * tile + tile // 2
        destino_y = linha * tile + tile // 2

        dx = destino_x - self.saulao.rect.centerx
        dy = destino_y - self.saulao.rect.centery

        distancia_ponto = pygame.Vector2(dx, dy).length()

        # Chegou no ponto
        if distancia_ponto < 3:
            self.indice_rota += 1

            if self.indice_rota >= len(self.rota):
                return

            coluna, linha = self.rota[self.indice_rota]

            destino_x = coluna * tile + tile // 2
            destino_y = linha * tile + tile // 2

            dx = destino_x - self.saulao.rect.centerx
            dy = destino_y - self.saulao.rect.centery

        self._mover(dx, dy, mapa)

    def _mover(self, dx, dy, mapa):

        direcao = pygame.Vector2(dx, dy)

        if direcao.length() == 0:
            return

        direcao = direcao.normalize()

        velocidade = self.saulao.velocidade

        movimento_x = direcao.x * velocidade
        movimento_y = direcao.y * velocidade

        antigo_x = self.saulao.pos_x
        antigo_y = self.saulao.pos_y

        # Movimento horizontal
        self.saulao.pos_x += movimento_x
        self.saulao.rect.x = int(self.saulao.pos_x)

        if any(
            self.saulao.rect.colliderect(obs)
            for obs in mapa.obstaculos
        ):
            self.saulao.pos_x = antigo_x
            self.saulao.rect.x = int(antigo_x)

        # Movimento vertical
        self.saulao.pos_y += movimento_y
        self.saulao.rect.y = int(self.saulao.pos_y)

        if any(
            self.saulao.rect.colliderect(obs)
            for obs in mapa.obstaculos
        ):
            self.saulao.pos_y = antigo_y
            self.saulao.rect.y = int(antigo_y)

        self.saulao.pos_x = max(
            0,
            min(
                self.saulao.pos_x,
                mapa.largura - self.saulao.rect.width
            )
        )

        self.saulao.pos_y = max(
            0,
            min(
                self.saulao.pos_y,
                mapa.altura - self.saulao.rect.height
            )
        )

        self.saulao.rect.x = int(self.saulao.pos_x)
        self.saulao.rect.y = int(self.saulao.pos_y)

        self.saulao.atualizar_direcao(
            movimento_x,
            movimento_y
        )

        self.saulao.animar(True)

    def _calcular_rota(self, inicio, alvo, mapa):
        if not self._celula_livre(alvo[0], alvo[1], mapa):
            alvo = self._encontrar_celula_livre(
                alvo,
                mapa
            )

            if alvo is None:
                return []

        fila = []
        heapq.heappush(fila, (0, inicio))

        veio_de = {}
        custo = {inicio: 0}

        direcoes = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        while fila:
            _, atual = heapq.heappop(fila)

            if atual == alvo:
                return self._reconstruir_rota(
                    veio_de,
                    atual
                )

            for dx, dy in direcoes:

                vizinho = (
                    atual[0] + dx,
                    atual[1] + dy
                )

                if not self._celula_livre(
                    vizinho[0],
                    vizinho[1],
                    mapa
                ):
                    continue

                novo_custo = custo[atual] + 1

                if (
                    vizinho not in custo
                    or novo_custo < custo[vizinho]
                ):
                    custo[vizinho] = novo_custo

                    prioridade = (
                        novo_custo
                        + abs(vizinho[0] - alvo[0])
                        + abs(vizinho[1] - alvo[1])
                    )

                    heapq.heappush(
                        fila,
                        (prioridade, vizinho)
                    )

                    veio_de[vizinho] = atual

        return []

    def _reconstruir_rota(self, veio_de, atual):
        rota = [atual]

        while atual in veio_de:
            atual = veio_de[atual]
            rota.append(atual)

        rota.reverse()

        # Não precisa voltar para a própria célula
        if len(rota) > 1:
            rota.pop(0)

        return rota

    def _celula_livre(self, coluna, linha, mapa):
        colunas = mapa.largura // mapa.tile_size
        linhas = mapa.altura // mapa.tile_size

        if not (0 <= coluna < colunas):
            return False

        if not (0 <= linha < linhas):
            return False

        tile = mapa.tile_size

        x = (
            coluna * tile
            + tile // 2
            - self.saulao.rect.width // 2
        )

        y = (
            linha * tile
            + tile // 2
            - self.saulao.rect.height // 2
        )

        teste = pygame.Rect(
            x,
            y,
            self.saulao.rect.width,
            self.saulao.rect.height
        )

        return not any(
            teste.colliderect(obs)
            for obs in mapa.obstaculos
        )

    def _encontrar_celula_livre(self, alvo, mapa):
        for distancia in range(1, 5):

            candidatos = [
                (alvo[0] + distancia, alvo[1]),
                (alvo[0] - distancia, alvo[1]),
                (alvo[0], alvo[1] + distancia),
                (alvo[0], alvo[1] - distancia)
            ]

            for candidato in candidatos:

                if self._celula_livre(
                    candidato[0],
                    candidato[1],
                    mapa
                ):
                    return candidato

        return None