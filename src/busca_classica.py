from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Set
from collections import deque
import heapq
import itertools
import math
import time

Estado = Tuple[int, int]

@dataclass
class No:
    estado: Estado
    pai: Optional['No'] = None
    acao: Optional[str] = None
    g: float = 0.0

@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    estados_explorados: List[Estado]
    tempo: float
    custo: float
    max_fronteira: int
    nos_revisitados: int = 0


def vizinhos(estado: Estado, mapa: dict) -> List[Tuple[str, Estado, float]]:
    linha, coluna = estado
    altura = mapa["altura"]
    largura = mapa["largura"]
    paredes = mapa["paredes"]
    
    candidatos = [
        ('up',    (linha - 1, coluna)),
        ('down',  (linha + 1, coluna)),
        ('left',  (linha, coluna - 1)),
        ('right', (linha, coluna + 1)),
    ]
    resultado = []
    for acao, (l, c) in candidatos:
        if 0 <= l < altura and 0 <= c < largura and not paredes[l][c]:
            resultado.append((acao, (l, c), 1.0))
    return resultado

def h(estado: Estado, objetivo: Estado) -> float:
    """Heurística de Manhattan."""
    return abs(estado[0] - objetivo[0]) + abs(estado[1] - objetivo[1])

def reconstruir(no: No):
    estados = []
    acoes = []
    atual = no
    while atual.pai is not None:
        estados.append(atual.estado)
        acoes.append(atual.acao)
        atual = atual.pai
    estados.reverse()
    acoes.reverse()
    return estados, acoes

def busca_largura(mapa: dict) -> ResultadoBusca:
    t1 = time.perf_counter()
    inicio_coord = mapa["inicio"]
    objetivo_coord = mapa["objetivo"]
    
    inicio = No(inicio_coord)
    fronteira = deque([inicio])
    em_fronteira = {inicio_coord}
    explorados: Set[Estado] = set()
    ordem_explorados: List[Estado] = []
    nos_explorados = 0
    nos_expandidos = 0
    max_fronteira = 1
    nos_revisitados = 0

    while fronteira:
        no = fronteira.popleft()
        em_fronteira.remove(no.estado)
        nos_explorados += 1
        ordem_explorados.append(no.estado)

        if no.estado == objetivo_coord:
            caminho, acoes = reconstruir(no)
            t2 = time.perf_counter()
            return ResultadoBusca('BFS', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, t2-t1, no.g, max_fronteira, nos_revisitados)

        explorados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in vizinhos(no.estado, mapa):
            if estado not in explorados and estado not in em_fronteira:
                filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                fronteira.append(filho)
                em_fronteira.add(estado)
            else:
                nos_revisitados += 1
        
        if len(fronteira) > max_fronteira:
            max_fronteira = len(fronteira)

    t2 = time.perf_counter()

    return ResultadoBusca('BFS', False, [], [], nos_explorados, nos_expandidos, ordem_explorados, t2-t1, no.g, max_fronteira, nos_revisitados)

def busca_profundidade(mapa: dict) -> ResultadoBusca:
    t1 = time.perf_counter()
    inicio = No(mapa["inicio"])
    fronteira = [inicio]
    em_fronteira = {mapa["inicio"]}
    explorados: Set[Estado] = set()
    ordem_explorados: List[Estado] = []
    nos_explorados = 0
    nos_expandidos = 0
    max_fronteira = 1
    nos_revisitados = 0

    while fronteira:
        no = fronteira.pop()
        em_fronteira.remove(no.estado)
        nos_explorados += 1
        ordem_explorados.append(no.estado)

        if no.estado == mapa["objetivo"]:
            caminho, acoes = reconstruir(no)
            t2 = time.perf_counter()
            return ResultadoBusca('DFS', True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, t2-t1, no.g, max_fronteira, nos_revisitados)

        explorados.add(no.estado)
        nos_expandidos += 1

        for acao, estado, custo in vizinhos(no.estado, mapa):
            if estado not in explorados and estado not in em_fronteira:
                filho = No(estado=estado, pai=no, acao=acao, g=no.g + custo)
                fronteira.append(filho)
                em_fronteira.add(estado)
            else:
                nos_revisitados += 1
        
        if len(fronteira) > max_fronteira:
            max_fronteira = len(fronteira)

    t2 = time.perf_counter()
    return ResultadoBusca('DFS', False, [], [], nos_explorados, nos_expandidos, ordem_explorados, t2-t1, no.g, max_fronteira, nos_revisitados)

def busca_prioridade(nome: str, mapa: dict, funcao_prioridade) -> ResultadoBusca:
    t1 = time.perf_counter()
    inicio_coord = mapa["inicio"]
    objetivo_coord = mapa["objetivo"]
    
    contador = itertools.count()
    inicio = No(inicio_coord, g=0.0)
    fronteira = []
    
    # Note que agora passamos inicio_coord para a funcao_prioridade, se ela precisar
    heapq.heappush(fronteira, (funcao_prioridade(inicio, objetivo_coord), next(contador), inicio))
    
    melhor_g: Dict[Estado, float] = {inicio_coord: 0.0}
    fechados: Set[Estado] = set()
    ordem_explorados: List[Estado] = []
    nos_explorados = 0
    nos_expandidos = 0
    max_fronteira = 1
    nos_revisitados = 0

    while fronteira:
        _, _, no = heapq.heappop(fronteira)

        if no.estado in fechados:
            continue

        nos_explorados += 1
        ordem_explorados.append(no.estado)

        if no.estado == objetivo_coord:
            caminho, acoes = reconstruir(no)
            t2 = time.perf_counter()
            return ResultadoBusca(nome, True, caminho, acoes, nos_explorados, nos_expandidos, ordem_explorados, t2-t1, no.g, max_fronteira, nos_revisitados)

        fechados.add(no.estado)
        nos_expandidos += 1

        # Novamente, passando o 'mapa'
        for acao, estado, custo in vizinhos(no.estado, mapa):
            novo_g = no.g + custo
            if estado in fechados:
                nos_revisitados+=1
                continue
            if novo_g < melhor_g.get(estado, math.inf):
                filho = No(estado=estado, pai=no, acao=acao, g=novo_g)
                melhor_g[estado] = novo_g
                heapq.heappush(fronteira, (funcao_prioridade(filho, objetivo_coord), next(contador), filho))
            else:
                nos_revisitados += 1

        if len(fronteira) > max_fronteira:
            max_fronteira = len(fronteira)

    t2 = time.perf_counter()
    return ResultadoBusca(nome, False, [], [], nos_explorados, nos_expandidos, ordem_explorados, t2-t1, no.g, max_fronteira, nos_revisitados)

def busca_custo_uniforme(mapa: dict) -> ResultadoBusca:
    return busca_prioridade(
        'UCS',
        mapa,
        lambda no, objetivo: no.g
    )

def busca_gulosa(mapa: dict) -> ResultadoBusca:
        return busca_prioridade(
            'Greedy BFS',
            mapa,
            lambda no, objetivo: h(no.estado, objetivo)
        )

def busca_weighted_astar(mapa: dict, peso: float = 1.0) -> ResultadoBusca:
    if peso <= 0:
        raise ValueError('O peso deve ser positivo.')
    return busca_prioridade(
        f'A* (w={peso})',
        mapa,
        lambda no, objetivo: no.g + peso * h(no.estado, objetivo)
    )