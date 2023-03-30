import heapq
import random
import time

class Node:
    def __init__(self, nivel, valor, peso, items):
        self.nivel = nivel
        self.valor = valor
        self.peso = peso
        self.items = items
    
    def __lt__(self, other):
        return self.valor > other.valor

def bound(node, items, capacidade):
    if node.peso >= capacidade:
        return 0
    else:
        bound_valor = node.valor
        bound_peso = node.peso
        cap_restante = capacidade - bound_peso
        next_item = node.nivel
        while next_item < len(items) and bound_peso + items[next_item][2] <= capacidade:
            bound_valor += items[next_item][1]
            bound_peso += items[next_item][2]
            next_item += 1
        if next_item < len(items):
            bound_valor += (cap_restante / items[next_item][2]) * items[next_item][1]
        return bound_valor

def mochila_bnb(items, capacidade):
    n = len(items)
    raiz = Node(0, 0, 0, [])
    heap = []
    valor_max = 0
    num_subproblemas = 0
    heapq.heappush(heap, raiz)
    while heap:
        node = heapq.heappop(heap)
        num_subproblemas += 1
        if node.nivel == n:
            if node.valor > valor_max:
                valor_max = node.valor
                selecionados = node.items
        else:
            next_item = items[node.nivel]
            if node.peso + next_item[2] <= capacidade:
                filho = Node(node.nivel + 1, node.valor + next_item[1], node.peso + next_item[2], node.items + [next_item[0]])
                if filho.valor > valor_max:
                    valor_max = filho.valor
                    selecionados = filho.items
                if bound(filho, items, capacidade) > valor_max:
                    heapq.heappush(heap, filho)
                    num_subproblemas += 1
            filho = Node(node.nivel + 1, node.valor, node.peso, node.items)
            if bound(filho, items, capacidade) > valor_max:
                heapq.heappush(heap, filho)
                num_subproblemas += 1
    return selecionados, valor_max, num_subproblemas

def mochila_gerador(num_items):
    capacidade = 100
    valores = [random.randint(1, 10) for _ in range(num_items)]
    pesos = [random.randint(1, 10) for _ in range(num_items)]
    items = [(i+1, valores[i], pesos[i]) for i in range(num_items)]
    return items, capacidade

def mochila_display(items, capacidade):
    print(f"Capacidade: {capacidade}")
    print("Item\tValor\tPeso")
    for item in items:
        print(f"{item[0]}\t{item[1]}\t{item[2]}")

num_items = 30
items, capacidade = mochila_gerador(num_items)

mochila_display(items, capacidade)
inicio = time.time_ns()
selecionados, valor_max, num_subproblemas = mochila_bnb(items, capacidade)
decorrido = time.time_ns() - inicio

print(f"\nItens: {selecionados}")
print(f"Z: {valor_max}")
print(f"Subproblemas: {num_subproblemas}")
print(f"Tempo decorrido: {decorrido:.2f} segundos")