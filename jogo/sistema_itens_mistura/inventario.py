class Inventario:
    def __init__(self):
        self.itens = []
        self.capacidade = 3

    def adicionar_item(self, item):
        if len(self.itens) < self.capacidade:
            self.itens.append(item)
            print(f"{item.nome} adicionado ao inventário")
            return True
        
        print("Inventário cheio!")
        return False
    
    def remover_item(self, item):
        if item in self.itens:
            self.itens.remove(item)

    def esta_cheio(self):
        return len(self.itens) >= self.capacidade