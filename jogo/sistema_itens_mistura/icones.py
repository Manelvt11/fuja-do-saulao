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
    "Ferro": "ferro.png",
    "Rubídio": "rubidio.png",
    "Nitrogênio": "nitrogenio.png",
    "Aldeído": "aldeido.png",
    "Dióxido de Enxofre": "dioxidoEnxofre.png",
    "Trióxido de Enxofre": "trioxidoEnxofre.png",
    "Ácido Sulfúrico": "AcidoSulfurico.png",
}

def _criar_icone_padrao(tamanho):
    #cria icone simples para itens que ainda não possuem imagem cadastrada
    superficie = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    pygame.draw.rect(superficie, (150,150,150), (0,0, tamanho, tamanho), border_radius=6)
    return superficie

def _padronizar_icone(original, tamanho):
    mascara = pygame.mask.from_surface(original)
    area = mascara.get_bounding_rects()

    if not area:
        return _criar_icone_padrao(tamanho)

    area = area[0]

    icone = original.subsurface(area).copy()
    tamanho_desenho = int(tamanho * 0.50)
    largura, altura = icone.get_size()
    escala = min(tamanho_desenho / largura, tamanho_desenho / altura)
    nova_largura = max(1, int(largura * escala))
    nova_altura = max(1, int(altura * escala))
    icone = pygame.transform.smoothscale(icone, (nova_largura, nova_altura))
    superficie = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
    x = (tamanho - nova_largura) //2 
    y= (tamanho - nova_altura) // 2
    superficie.blit(icone, (x, y))
    return superficie

def obter_icone(nome, tamanho=40, reduzir=True):
    #retorna icone correspondente ao item
    #se o icone ja tiver sido carregado anteriormente, usa a versao armazenada no cache
    #caso o item não possua imagem cadastrada, retorna um ícone padrão
    chave = (nome, tamanho, reduzir)

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
            if reduzir:
                superficie = _padronizar_icone(original, tamanho)
            else:
                superficie = pygame.transform.smoothscale(original, (tamanho, tamanho))

    _cache_icones[chave] = superficie

    return superficie