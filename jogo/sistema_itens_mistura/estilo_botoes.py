import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_BOTOES = os.path.join(BASE_DIR, "assets", "ui", "botoes")

_cache = {}

def _carregar(nome_arquivo, tamanho):
    chave = (nome_arquivo, tamanho)
    if chave in _cache:
        return _cache[chave]

    caminho = os.path.join(PASTA_BOTOES, nome_arquivo)
    original = pygame.image.load(caminho).convert_alpha()
    escalada = pygame.transform.smoothscale(original, tamanho)

    _cache[chave] = escalada
    return escalada

def imagem_normal(tamanho):
    return _carregar("botao_normal.png", tamanho)

def imagem_hover(tamanho):
    return _carregar("botao_hover.png", tamanho)

def imagem_selecionado(tamanho):
    return _carregar("botao_selecionado.png", tamanho)

def imagem_desabilitado(tamanho):
    return _carregar("botao_desabilitado.png", tamanho)