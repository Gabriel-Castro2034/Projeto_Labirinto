from dataclasses import dataclass
from typing import Tuple, List
import math
import time
import random
from src.busca_classica import busca_weighted_astar 

Coordenada = Tuple[int, int]


@dataclass
class ResultadoBuscaLocal:
    algoritmo: str
    ordem: List[Tuple[int,int]]
    custo: float
    tempo: float
    iteracoes: int
    curva_convergencia: List[float]
    caminho: List[Tuple[int,int]]
    explorados: List[Tuple[int,int]]


def gerar_vizinhos(ordem_coleta: List[Coordenada]) -> List[List[Coordenada]]:
    '''
    Retorna todas as combinações possíveis obtidas ao trocar a posição de dois 
    pontos de coleta na permutação atual.
    '''
    vizinhos = []
    n = len(ordem_coleta)
    for i in range(n):
        for j in range(i+1,n):
            vizinho = list(ordem_coleta)
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
    return vizinhos

def calcula_custo(ordem_coleta: List[Coordenada], inicio: Coordenada, objetivo: Coordenada, mapa: dict) -> float:
    '''
    Utiliza o algoritmo A* Clássico de forma subjacente para calcular a distância
    entre a origem, a sequência de pontos de coleta e o destino final no labirinto.
    '''
    custo_total = 0.0
    ponto_atual = inicio
    caminho = []
    explorados = []

    for prox_ponto in ordem_coleta:
        mapa_temp = mapa.copy()
        mapa_temp["inicio"] = ponto_atual
        mapa_temp["objetivo"] = prox_ponto
        res_temp = busca_weighted_astar(mapa_temp, peso = 1.0)
        custo_total += res_temp.custo
        caminho.extend(res_temp.caminho)
        explorados.extend(res_temp.estados_explorados)
        ponto_atual = prox_ponto

    mapa_temp = mapa.copy()
    mapa_temp["inicio"] = ponto_atual
    mapa_temp["objetivo"] = objetivo
    res_temp = busca_weighted_astar(mapa_temp, peso = 1.0)
    custo_total += res_temp.custo
    caminho.extend(res_temp.caminho)
    explorados.extend(res_temp.estados_explorados)

    return custo_total, caminho, explorados


def simple_hill_climbing(mapa:dict, max_iter: int = 1000) -> ResultadoBuscaLocal:
    '''
    Itera sobre o espaço de permutações avaliando todos os vizinhos gerados por
    troca de dois pontos de coleta.
    A cada passo, adota o vizinho que apresenta a maior redução no custo total.
    A execução é interrompida ao atingir um mínimo local, ou 
    seja, quando nenhum vizinho é estritamente melhor que o estado atual.
    '''
    t1 = time.perf_counter()
    inicio_coord = mapa["inicio"]
    objetivo_coord = mapa["objetivo"]
    ordem_atual = mapa["coletas"]
    

    custo_atual, caminho_atual, explorados_atual = calcula_custo(ordem_atual, inicio_coord, objetivo_coord, mapa)

    curva = [custo_atual]
    iteracoes_usadas = 0  
    for _ in range(max_iter):
        iteracoes_usadas += 1
        vizinhos = gerar_vizinhos(ordem_atual)
        melhor_vizinho = None
        melhor_custo_vizinho = math.inf

        for vizinho in vizinhos:
            custo, caminho, explorados = calcula_custo(vizinho,inicio_coord, objetivo_coord, mapa)
            if custo < melhor_custo_vizinho:
                melhor_custo_vizinho = custo
                melhor_vizinho = vizinho

        if melhor_custo_vizinho >= custo_atual:
            break  # Não encontrou vizinho melhor, termina

        ordem_atual = melhor_vizinho
        custo_atual = melhor_custo_vizinho
        caminho_atual = caminho
        explorados_atual = explorados
        curva.append(custo_atual)

    t2 = time.perf_counter()
    return ResultadoBuscaLocal('Simple Hill Climbing', ordem_atual, custo_atual, t2-t1, iteracoes_usadas, curva, caminho_atual, explorados_atual)

def random_restart(mapa: dict, k: int = 5, max_iter: int = 1000) -> ResultadoBuscaLocal:
    t1 = time.perf_counter()
    inicio_coord = mapa["inicio"]
    objetivo_coord = mapa["objetivo"]
    ordem_inicial = mapa["coletas"]
    
    solucoes_iniciais = [ordem_inicial]
    for _ in range(k-1):
        nova_ordem = ordem_inicial[:]
        random.shuffle(nova_ordem)
        solucoes_iniciais.append(nova_ordem)
    
    melhor_ordem_global = None
    melhor_custo_global = math.inf
    curva = []
    iteracoes_usadas = 0
    
    for solucao in solucoes_iniciais:
        ordem_atual = solucao
        custo_atual, caminho_atual, explorados_atual = calcula_custo(solucao, inicio_coord, objetivo_coord, mapa)

        if custo_atual < melhor_custo_global:
            melhor_custo_global = custo_atual
            melhor_ordem_global = ordem_atual

        curva.append(melhor_custo_global)

        for _ in range(max_iter):
            iteracoes_usadas += 1
            vizinhos = gerar_vizinhos(ordem_atual)
            melhor_vizinho = None
            melhor_custo_vizinho = math.inf

            for vizinho in vizinhos:
                custo, caminho, explorados = calcula_custo(vizinho,inicio_coord, objetivo_coord, mapa)
                if custo < melhor_custo_vizinho:
                    melhor_custo_vizinho = custo
                    melhor_vizinho = vizinho

            if melhor_custo_vizinho >= custo_atual:
                break  # Não encontrou vizinho melhor, termina

            ordem_atual = melhor_vizinho
            custo_atual = melhor_custo_vizinho
            caminho_atual = caminho
            explorados_atual = explorados

            if custo_atual < melhor_custo_global:
                melhor_custo_global = custo_atual
                melhor_ordem_global = ordem_atual
            
            curva.append(melhor_custo_global)
        


    t2 = time.perf_counter()
    return ResultadoBuscaLocal(f'Random Restart Hill Climbing (k={k})', melhor_ordem_global, melhor_custo_global, t2 - t1, iteracoes_usadas, curva, caminho_atual, explorados_atual)


def simulated_annealing(mapa: dict, max_iter: int = 1000, t_inicial: float = 100.0, resfriamento: float = 0.95) -> ResultadoBuscaLocal:
    '''
    O algoritmo escapa de mínimos locais ao permitir transições para rotas piores.
    A probabilidade de aceitar um passo ruim é calculada pela função de Boltzmann (e^(-delta/T))
    e diminui ao longo do tempo de acordo com a temperatura e a taxa de resfriamento.
    Avalia apenas um vizinho aleatório por iteração.
    '''
    t1 = time.perf_counter()
    inicio_coord = mapa["inicio"]
    objetivo_coord = mapa["objetivo"]
    ordem_atual = mapa["coletas"]
    
    custo_atual, caminho_atual, explorados_atual = calcula_custo(ordem_atual, inicio_coord, objetivo_coord, mapa)

    melhor_ordem_global = ordem_atual
    melhor_custo_global = custo_atual

    curva = [custo_atual]
    iteracoes_usadas = 0 
    t = t_inicial

    for _ in range(max_iter):
        iteracoes_usadas += 1
        vizinhos = gerar_vizinhos(ordem_atual)
        vizinho = random.choice(vizinhos)
        custo_vizinho, caminho_vizinho, explorados_vizinho = calcula_custo(vizinho, inicio_coord, objetivo_coord, mapa)
        delta = custo_vizinho - custo_atual
        
        if t < 0.0001:
            break

        if delta<0 or random.random() < math.exp(-delta/t):
            ordem_atual = vizinho
            custo_atual = custo_vizinho
            caminho_atual = caminho_vizinho
            explorados_atual = explorados_vizinho
            if custo_atual < melhor_custo_global:
                melhor_custo_global = custo_atual
                melhor_ordem_global = ordem_atual

        curva.append(melhor_custo_global)

        t *= resfriamento
            

    t2 = time.perf_counter()
    return ResultadoBuscaLocal('Simulated Annealing', melhor_ordem_global, melhor_custo_global, t2-t1, iteracoes_usadas, curva, caminho_atual, explorados_atual)

def mutacao(rota: List[Coordenada], taxa_mutacao: float = 0.1) -> List[Coordenada]:
    """Sorteia um número. Se cair na taxa de mutação, troca dois genes (pontos) de lugar."""
    if random.random() < taxa_mutacao:
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]
    return rota

def cruzamento_ordem(pai1: List[Coordenada], pai2: List[Coordenada]) -> List[Coordenada]:
    """Faz o Order Crossover (OX). Garante que o filho tenha todos os pontos sem repetições."""
    tamanho = len(pai1)
    # 1. Escolhe dois pontos de corte aleatórios
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    
    # 2. Cria o filho vazio e copia o 'miolo' do pai1
    filho = [None] * tamanho
    filho[inicio:fim+1] = pai1[inicio:fim+1]
    
    # 3. Preenche o resto com os genes do pai2 (que já não estejam no filho)
    ponteiro_filho = (fim + 1) % tamanho
    for gene in pai2:
        if gene not in filho:
            filho[ponteiro_filho] = gene
            ponteiro_filho = (ponteiro_filho + 1) % tamanho
            
    return filho

def algoritmo_genetico(mapa: dict, tamanho_populacao: int = 50, max_geracoes: int = 100, taxa_mutacao: float = 0.1) -> ResultadoBuscaLocal:
    t1 = time.perf_counter()
    inicio_coord = mapa["inicio"]
    objetivo_coord = mapa["objetivo"]
    ordem_inicial = mapa["coletas"]

    # 1. Gênesis: Criar a População Inicial (Várias rotas aleatórias)
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = ordem_inicial[:]
        random.shuffle(individuo)
        populacao.append(individuo)

    melhor_ordem_global = None
    melhor_custo_global = math.inf
    curva = []
    iteracoes_usadas = 0

    # 2. O Ciclo da Evolução (Gerações)
    for geracao in range(max_geracoes):
        iteracoes_usadas += 1

        # Avalia a aptidão de todos (Calcula o custo de cada rota)
        custos_populacao = []
        for individuo in populacao:
            custo = calcula_custo(individuo, inicio_coord, objetivo_coord, mapa)
            custos_populacao.append((custo, individuo))

        # Ordena do melhor (menor custo) para o pior
        custos_populacao.sort(key=lambda x: x[0])

        # Atualiza o recorde histórico
        melhor_custo_atual, melhor_individuo_atual = custos_populacao[0]
        if melhor_custo_atual < melhor_custo_global:
            melhor_custo_global = melhor_custo_atual
            melhor_ordem_global = melhor_individuo_atual

        curva.append(melhor_custo_global)

        # 3. Seleção e Reprodução
        # Elitismo: Os 2 melhores pais sobrevivem intactos para a próxima geração
        nova_populacao = [custos_populacao[0][1], custos_populacao[1][1]]

        # Preenche o resto da população cruzando os melhores
        while len(nova_populacao) < tamanho_populacao:
            # Torneio Simples: Pega 3 pessoas aleatórias e o melhor vira pai
            competidores_pai1 = random.sample(custos_populacao, 3)
            pai1 = min(competidores_pai1, key=lambda x: x[0])[1]

            competidores_pai2 = random.sample(custos_populacao, 3)
            pai2 = min(competidores_pai2, key=lambda x: x[0])[1]

            # Reprodução e Mutação
            filho = cruzamento_ordem(pai1, pai2)
            filho = mutacao(filho, taxa_mutacao)

            nova_populacao.append(filho)

        # A nova geração substitui a antiga
        populacao = nova_populacao

    t2 = time.perf_counter()
    return ResultadoBuscaLocal(
        algoritmo=f'Algoritmo Genético (Pop={tamanho_populacao}, Ger={max_geracoes})',
        caminho=melhor_ordem_global,
        custo=melhor_custo_global,
        tempo=t2 - t1,
        iteracoes=iteracoes_usadas,
        curva_convergencia=curva
    )
