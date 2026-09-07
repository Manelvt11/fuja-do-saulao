import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_ICONES = os.path.join(BASE_DIR, "assets", "itens", "icons")

#cache para evitar carregar e redimensionar a mesma imagem várias vezes durante o jogo
_cache_icones = {}

MAPA_ARQUIVOS = {
    "Hidrogênio": "hidrogenio.png",
    "Oxigênio": "oxigenio.png",
    "Enxofre": "enxofre.png",
    "Cloro": "cloro.png",
    "Carbono": "carbono.png",
    "Sódio": "sodio.png",
    "Água": "agua.png",
    "Bromo": "bromo.png",
    "Dióxido de Enxofre": "dioxidoEnxofre.png",
    "Trióxido de Enxofre": "trioxidoEnxofre.png",
    "Ácido Sulfúrico": "AcidoSulfurico.png",
}

def _criar_icone_padrao(tamanho):
    #cria icone simples para itens que ainda não possuem imagem cadastrada
    superficie = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    pygame.draw.rect(superficie, (150,150,150), (0,0, tamanho, tamanho), border_radius=6)

def obter_icone(nome, tamanho=40):
    #retorna icone correspondente ao item
    #se o icone ja tiver sido carregado anteriormente, usa a versao armazenada no cache
    #caso o item não possua imagem cadastrada, retorna um ícone padrão
    chave = (nome, tamanho)

    if chave in _cache_icones:
        return _cache_icones[chave]

    arquivo = MAPA_ARQUIVOS.get(nome)

    if arquivo is None:
        superficie = _criar_icone_padrao(tamanho)

    else:
        caminho = os.path.join(PASTA_ICONES, arquivo)

        try:
            original = pygame.image.load(caminho).convert_alpha()

        except (pygame.error, FileNotFoundError):
            print(f"não foi possível carregar o ícone do item '{nome}'")

            superficie = _criar_icone_padrao(tamanho)

        else:
            superficie = pygame.transform.smoothscale(original,(tamanho, tamanho))

    _cache_icones[chave] = superficie

    return superficie