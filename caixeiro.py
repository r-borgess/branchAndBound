import heapq
import itertools
import random
import time

class Node:
    def __init__(self, nivel, rota, custo, cidades):
        self.nivel = nivel
        self.rota = rota
        self.custo = custo
        self.cidades = cidades
    
    def __lt__(self, other):
        return self.custo < other.custo

def bound(node, dist):
    n = len(node.cidades)
    cidade_atual = node.rota[-1]
    nao_visitadas = [c for c in node.cidades if c != cidade_atual]
    if not nao_visitadas:
        return node.custo + dist[cidade_atual][0]
    else:
        distancias = [(dist[cidade_atual][c], cidade_atual, c) for c in nao_visitadas]
        heapq.heapify(distancias)
        nodes = list(range(n))
        if cidade_atual in nodes:
            nodes.remove(cidade_atual)
        arestas = []
        node_set = {cidade_atual}
        while len(node_set) < n:
            _, u, v = heapq.heappop(distancias)
            if u in node_set and v in node_set:
                continue
            if u not in node_set:
                u, v = v, u
            node_set.add(v)
            if v in nodes:
                nodes.remove(v)
            arestas.append((u, v))
        custo_arvore_min = sum(dist[u][v] for u, v in arestas)
        custo_1 = 0
        for u, v in arestas:
            distancia_min = float('inf')
            for i in nodes:
                if dist[u][i] + dist[i][v] < distancia_min:
                    distancia_min = dist[u][i] + dist[i][v]
            custo_1 += distancia_min
        return node.custo + custo_arvore_min + custo_1

def caixeiro_bnb(dist):
    n = len(dist)
    raiz = Node(0, [0], 0, list(range(1, n)))
    heap = []
    custo_min = float('inf')
    num_subproblemas = 0
    heapq.heappush(heap, raiz)
    while heap:
        node = heapq.heappop(heap)
        num_subproblemas += 1
        if node.nivel == n-1:
            custo = node.custo + dist[node.rota[-1]][0]
            if custo < custo_min:
                custo_min = custo
                melhor_rota = node.rota
        else:
            cidade_atual = node.rota[-1]
            for proxima_cidade in node.cidades:
                filho_custo = node.custo + dist[cidade_atual][proxima_cidade]
                if filho_custo < custo_min:
                    filho_rota = node.rota + [proxima_cidade]
                    filho_cidades = [c for c in node.cidades if c != proxima_cidade]
                    filho = Node(node.nivel + 1, filho_rota, filho_custo, filho_cidades)
                    if not filho_cidades:
                        if filho_custo + dist[proxima_cidade][0] < custo_min:
                            custo_min = filho_custo + dist[proxima_cidade][0]
                            melhor_rota = filho_rota + [0]
                    elif bound(filho, dist) < custo_min:
                        heapq.heappush(heap, filho)
                        num_subproblemas += 1
    return melhor_rota, custo_min, num_subproblemas

def caixeiro_gerador(num_cidades, max_distance):
    dist = [[0]*num_cidades for _ in range(num_cidades)]
    for i in range(num_cidades):
        for j in range(i+1, num_cidades):
            dist[i][j] = random.randint(1, max_distance)
            dist[j][i] = dist[i][j]
    return dist

def caixeiro_display(dist):
    print("Matriz de distâncias:")
    for l in dist:
        print(l)

dist = caixeiro_gerador(10, 10)
caixeiro_display(dist)

start_time = time.time()
melhor_rota, custo_min, num_subproblemas = caixeiro_bnb(dist)
time_taken = time.time() - start_time

print(f"\nRota: {melhor_rota}")
print(f"Z: {custo_min}")
print(f"Subproblemas: {num_subproblemas}")
print(f"Tempo decorrido: {time_taken:.12f} segundos")