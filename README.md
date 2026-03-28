# Fuja do Saulão

Jogo desenvolvido em Python utilizando a biblioteca Pygame para a disciplina de Programação Orientada a Objetos.

---

## Integrantes

* Manoel Vitor Nascimento
* Adaylton

---

## 1. Descrição Geral

"Fuja do Saulão" é um jogo do tipo aventura com visão de cima (top-down). O jogador está preso dentro de um laboratório e precisa encontrar uma forma de escapar.

O cenário é um laboratório com mesas, prateleiras e itens espalhados. A ideia principal do jogo é coletar itens corretos, realizar uma mistura e fugir enquanto é perseguido por um inimigo.

---

## 2. Objetivo do Jogo

O objetivo do jogador é coletar três itens corretos, realizar a mistura na mesa de laboratório, criar uma solução corrosiva e usá-la para abrir a porta e escapar antes de ser alcançado pelo inimigo.

---

## 3. Personagem Principal

O jogador controla um estudante preso no laboratório.

Movimentação:

* Pode se mover em quatro direções (cima, baixo, esquerda e direita)

Atributos:

* Vida: 3 pontos
* Inventário: até 3 itens
* Velocidade: fixa

---

## 4. Inimigos e Obstáculos

Inimigo principal: Saulão

* Se move automaticamente pelo mapa
* Persegue o jogador
* Ao encostar no jogador, retira 1 ponto de vida

Obstáculos:

* Mesas
* Prateleiras
* Paredes

Função dos obstáculos:

* Impedir passagem
* Dificultar movimentação

---

## 5. Cenário (Mapa)

O jogo acontece dentro de um laboratório fechado.

Elementos do mapa:

* Mesas com itens
* Prateleiras com objetos
* Porta de saída (objetivo final)
* Paredes que limitam o mapa

Distribuição:

* Itens principais ficam nas mesas
* Itens de apoio ficam nas prateleiras
* A porta fica na parte inferior do mapa

---

## 6. Sistema de Pontuação

A pontuação é baseada no tempo que o jogador leva para escapar:

| Tempo para fugir | Pontos      |
| ---------------- | ----------- |
| 0 – 1 min        | 1000 pontos |
| 1 – 2 min        | 900 pontos  |
| 2 – 3 min        | 800 pontos  |
| 3 – 4 min        | 650 pontos  |
| 4 – 5 min        | 500 pontos  |
| 5 – 6 min        | 300 pontos  |
| 6 – 7 min        | 150 pontos  |
| Não fugiu        | 0 pontos    |

---

## 7. Sistema de Vida

O jogador começa com 3 vidas.

Perde vida ao encostar no inimigo.
Quando a vida chega a zero, o jogo termina.

---

## 8. Controles

| Tecla                  | Função                                |
| ---------------------- | ------------------------------------- |
| W / seta para cima     | mover para cima                       |
| S / seta para baixo    | mover para baixo                      |
| A / seta para esquerda | mover para esquerda                   |
| D / seta para direita  | mover para direita                    |
| E                      | interagir (coletar itens e usar mesa) |
| C                      | misturar itens                        |
| ESC                    | sair do jogo                          |

---

## 9. Fluxo do Jogo

O jogo começa com o personagem no centro do laboratório.
O jogador precisa explorar o mapa, coletar itens e evitar o inimigo.

Depois de coletar os itens necessários, deve ir até a mesa de mistura e tentar criar a solução correta.

Se conseguir, pode abrir a porta e vencer o jogo.
Se perder todas as vidas, o jogo termina.

---

## 10. Regras do Jogo

* O jogador não pode atravessar paredes
* Pode carregar no máximo 3 itens
* A mistura só funciona com os itens corretos
* Encostar no inimigo causa dano
* É necessário criar a solução antes de sair

---

## 11. Estrutura do Projeto

```
/jogo
  main.py
  game.py
  player.py
  enemy.py
  item.py
  map.py
```

Responsabilidades:

* main.py: inicia o jogo
* game.py: controla o funcionamento geral
* player.py: define o jogador
* enemy.py: define o inimigo
* item.py: define os itens
* map.py: define o cenário

---

## 12. Funcionalidades Mínimas

* Movimento do jogador
* Colisão com paredes
* Coleta de itens
* Inventário simples
* Sistema de mistura
* Inimigo seguindo o jogador
* Sistema de vida
* Condição de vitória e derrota

---

## 13. Melhorias Futuras

* Adicionar mais tipos de itens
* Melhorar efeitos visuais
* Adicionar sons
* Melhorar comportamento do inimigo
* Criar mapas diferentes
* Adicionar novos desafios

---

## Nome da Solução Final

Solução Corrosiva Experimental

Item necessário para abrir a porta e finalizar o jogo.

---

## Conclusão

O jogo trabalha conceitos de programação orientada a objetos de forma prática, organizando o código em classes e dividindo responsabilidades entre os elementos do jogo.
