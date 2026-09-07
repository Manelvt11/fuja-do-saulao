class Inventario:
    def __init__(self, capacidade=3):
        self.itens = []
        self.capacidade = capacidade

    def adicionar_item(self, item):
        if self.esta_cheio():
            print("Inventário cheio!")
            return False
    
        self.itens.append(item)
        print(f"{item.nome} adicionado ao inventário")
        return True
    
    def remover_item(self, item):
        if item not in self.itens:
            return False

        self.itens.remove(item)
        return True

    def tem_item(self, nome):
        #verifica se o inventário possui um item pelo nome
        return any(item.nome == nome for item in self.itens)

    def quantidade(self):
        #retorna a quantidade atual de itens
        return len(self.itens)

    def esta_cheio(self):
        return len(self.itens) >= self.capacidade

    def tem_espaço(self):
        #verifica se ainda tem espaço no inventário
        return not self.esta_cheio()

    def limpar(self):
        #remove todos os itens do inventário
        self.itens.clear()