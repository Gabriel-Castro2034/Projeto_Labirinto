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
    """Gera a vizinhança trocando de posição dois pontos de coleta."""
    vizinhos = []
    n = len(ordem_coleta)
    for i in range(n):
        for j in range(i+1,n):
            vizinho = list(ordem_coleta)
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
    return vizinhos

def calcula_custo(ordem_coleta: List[Coordenada], inicio: Coordenada, objetivo: Coordenada, mapa: dict) -> float:
    """Calcula o custo total do caminho passando por todos os pontos de coleta."""
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

#def genetico(mapa: dict, max_geracoes: int = 100, tam_populacao: int = 10, prob_mutacao: float = 0.1) -> ResultadoBuscaLocal:
#    t1 = time.perf_counter()
#    inicio_coord = mapa["inicio"]
#    objetivo_coord = mapa["objetivo"]
