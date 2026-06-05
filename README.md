# Fuja do Saulão

Jogo desenvolvido em Python utilizando a biblioteca Pygame para a disciplina de Programação Orientada a Objetos.

---

## Integrantes

* Manoel Vitor Nascimento
* Adaylton

---

## 1. Descrição Geral

"Fuja do Saulão" é um jogo de aventura com visão superior (top-down) desenvolvido em Python utilizando Pygame.

O jogador controla um estudante preso dentro de um laboratório e precisa encontrar uma forma de escapar enquanto é perseguido por Saulão.

Para vencer, o jogador deverá explorar o laboratório, coletar os elementos químicos corretos, produzir Ácido Sulfúrico (H₂SO₄) e utilizá-lo para derreter a porta de saída.

---

## 2. Objetivo do Jogo

O objetivo do jogador é encontrar os elementos químicos necessários para produzir Ácido Sulfúrico (H₂SO₄), realizar a mistura corretamente e utilizar a substância para abrir a saída do laboratório antes de ser alcançado por Saulão.

---

## 3. Personagem Principal

O jogador controla um estudante preso no laboratório.

### Movimentação

* Movimento em quatro direções
* Suporte às teclas WASD
* Suporte às setas direcionais
* Movimentação diagonal

### Atributos

* Vida: 3 pontos
* Inventário: até 3 itens
* Velocidade fixa

---

## 4. Inimigos e Obstáculos

### Inimigo Principal: Saulão

* Persegue o jogador pelo laboratório
* Utiliza sistema de inteligência artificial para encontrar caminhos livres
* Desvia de obstáculos presentes no mapa
* Ao encostar no jogador, remove 1 ponto de vida

### Obstáculos

* Mesas
* Bancadas
* Prateleiras
* Paredes

### Função dos Obstáculos

* Impedir passagem
* Dificultar movimentação
* Influenciar o trajeto percorrido pelo inimigo

---

## 5. Cenário (Mapa)

O jogo acontece dentro de um laboratório fechado.

### Elementos do Mapa

* Bancadas de laboratório
* Prateleiras
* Itens químicos coletáveis
* Mesa de mistura
* Porta de saída
* Paredes e obstáculos

### Desenvolvimento do Cenário

O cenário foi criado utilizando o software Tiled Map Editor.

As informações do mapa e das colisões são carregadas através da biblioteca PyTMX.

---

## 6. Sistema de Mistura

O jogador deverá coletar elementos químicos espalhados pelo laboratório.

### Elementos Corretos

* Hidrogênio (H)
* Enxofre (S)
* Oxigênio (O)

### Elementos Incorretos

* Cloro (Cl)
* Carbono (C)
* Sódio (Na)

### Ordem Correta da Mistura

H → S → O

### Resultado da Mistura

Se a mistura estiver correta:

* Produz Ácido Sulfúrico (H₂SO₄)
* Permite derreter a porta do laboratório
* Possibilita a vitória do jogador

Se a mistura estiver incorreta:

* Ocorre uma explosão
* O jogador perde vida
* Os itens utilizados são descartados

---

## 7. Sistema de Pontuação

A pontuação será baseada no tempo necessário para escapar do laboratório.

O jogo foi planejado para ter duração mínima de 5 minutos e máxima de 7 minutos.

| Tempo para fugir          | Pontos      |
| ------------------------- | ----------- |
| Até 5 min                 | 1000 pontos |
| Até 5 min e 30 s          | 900 pontos  |
| Até 6 min                 | 800 pontos  |
| Até 6 min e 30 s          | 600 pontos  |
| Até 7 min                 | 400 pontos  |
| Acima de 7 min ou derrota | 0 pontos    |

---

## 8. Sistema de Vida

O jogador inicia a partida com 3 vidas.

Perde vida quando:

* É atingido por Saulão
* Realiza uma mistura incorreta

Quando a vida chega a zero, o jogo termina.

---

## 9. Controles

| Tecla | Função              |
| ----- | ------------------- |
| W / ↑ | Mover para cima     |
| S / ↓ | Mover para baixo    |
| A / ← | Mover para esquerda |
| D / → | Mover para direita  |
| E     | Interagir           |
| C     | Misturar itens      |
| ESC   | Sair do jogo        |

---

## 10. Fluxo do Jogo

O jogo começa com o personagem dentro do laboratório.

Fluxo principal:

Jogador explora o mapa
↓
Coleta elementos químicos
↓
Evita Saulão
↓
Vai até a mesa de mistura
↓
Seleciona os três elementos
↓
Realiza a mistura
↓
Produz Ácido Sulfúrico
↓
Derrete a porta
↓
Escapa do laboratório

Caso o jogador perca todas as vidas, o jogo termina.

---

## 11. Regras do Jogo

* O jogador não pode atravessar obstáculos
* O inventário possui limite de 3 itens
* Apenas a combinação correta produz Ácido Sulfúrico
* Misturas incorretas causam dano
* Encostar em Saulão causa dano
* É obrigatório produzir o ácido antes de escapar

---

## 12. Estrutura do Projeto

```text
/jogo
│
├── assets
│
├── sistema_itens_mistura
│   ├── __init__.py
│   ├── inventario.py
│   ├── item.py
│   ├── mesa_mistura.py
│   ├── objeto_mapa.py
│   └── porta.py
│
├── sistema_personagens
│   ├── __init__.py
│   ├── inimigo.py
│   ├── personagens.py
│   └── player.py
│
├── __init__.py
├── game.py
├── hud.py
├── main.py
└── map.py
```

### Responsabilidades

* main.py: inicia o jogo
* game.py: controla o funcionamento geral
* map.py: gerencia cenário e colisões
* hud.py: exibe informações ao jogador
* personagens.py: classe base dos personagens
* player.py: controla o jogador
* inimigo.py: controla Saulão
* objeto_mapa.py: classe base para objetos do mapa
* item.py: define os itens coletáveis
* inventario.py: gerencia o inventário do jogador
* mesa_mistura.py: controla o sistema de mistura
* porta.py: controla a porta de saída

---

## 13. Funcionalidades Implementadas

* Movimentação do jogador
* Movimentação diagonal
* Sistema de colisão
* Sistema de vida
* Estrutura orientada a objetos
* Mapa criado no Tiled
* Carregamento de mapa com PyTMX
* Sprites animados do jogador
* Sistema de iluminação dinâmica
* IA de perseguição do Saulão
* Obstáculos carregados do mapa
* Sistema de tela cheia

---

## 14. Funcionalidades em Desenvolvimento

* Sistema de itens
* Sistema de inventário (máximo de 3 itens)
* Coleta de itens
* Interação com objetos
* Mesa de mistura
* Produção do Ácido Sulfúrico
* Sistema de pontuação
* Tela de vitória
* Tela de derrota
* HUD completa
* Abertura da porta utilizando o ácido produzido

---

## 15. Melhorias Futuras

* Adicionar efeitos sonoros
* Implementar música de fundo
* Melhorar animações
* Melhorar a inteligência artificial do Saulão
* Adicionar novos mapas
* Criar novos desafios
* Adicionar diferentes níveis de dificuldade

---

## Solução Final

### Ácido Sulfúrico (H₂SO₄)

Substância necessária para derreter a porta do laboratório e permitir a fuga do jogador.

---

## Conclusão

O projeto aplica conceitos de Programação Orientada a Objetos por meio da divisão do código em módulos independentes, utilização de herança, encapsulamento e separação de responsabilidades.

Além disso, integra sistemas de movimentação, colisão, inteligência artificial, carregamento de mapas, iluminação dinâmica e mecânicas de coleta e mistura de itens para criar uma experiência interativa dentro do ambiente de laboratório.
