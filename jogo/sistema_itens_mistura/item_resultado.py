class ItemResultado:
    #item criado através de uma mistura
    #diferente de Item, esse objeto não aparece diretamente no mapa, ele é criado já dentro do inventário
    def __init__(self, nome):
        self.nome = nome
        self.coletado = True