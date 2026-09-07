#receitas disponíveis na mesa de mistura
#o frozenset permite que a ordem dos ingredientes não importe
RECEITAS = {
    frozenset(["Enxofre", "Oxigênio"]): "Dióxido de Enxofre",
    frozenset(["Dióxido de Enxofre", "Oxigênio"]): "Trióxido de Enxofre",
    frozenset(["Hidrogênio", "Oxigênio"]): "Água",
    frozenset(["Trióxido de Enxofre", "Água"]): "Ácido Sulfúrico",
}

ITEM_FINAL = "Ácido Sulfúrico"

def buscar_receita(nomes_selecionados):
    #procura uma receita com base nos nomes dos itens selecionados
    ingredientes = frozenset(nomes_selecionados)
    return RECEITAS.get(ingredientes)

