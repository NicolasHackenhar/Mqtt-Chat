class Fila:
    def __init__(self):
        self.items = []

    def esta_vazia(self):
        return len(self.items) == 0

    def enfileirar(self, item):
        self.items.append(item)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.items.pop(0)
        else:
            raise IndexError("A fila está vazia")

    def tamanho(self):
        return len(self.items)
