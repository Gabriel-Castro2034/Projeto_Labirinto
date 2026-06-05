from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Set
import time

Estado = Tuple[int, int]

@dataclass
class No:
    estado: Estado
    pai: Optional['No'] = None
    acao: Optional[str] = None
    g: float = 0.0

@dataclass
class ResultadoBuscaOnline:
    encontrado: bool
    tempo: float
    n_movimentos: int
    custo_percorrido: float
    n_celulas_reveladas: int
    n_celulas_revisitadas: int
    historico: list

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
    for _, (l, c) in candidatos:
        if 0 <= l < altura and 0 <= c < largura and not paredes[l][c]:
            resultado.append(((l, c), 1.0))
    return resultado

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

def busca_profundidade_online(mapa: dict) -> ResultadoBuscaOnline:
    t1 = time.perf_counter()
    inicio = mapa["inicio"]
    objetivo = mapa["objetivo"]
    estado_atual = inicio
    caminho_retorno = []
    explorados = set()
    vistos = {inicio}
    historico = []

    custo_percorrido = 0.0
    n_celulas_revisitadas = 0
    n_movimentos = 0
    encontrado = False

    while True:
        if estado_atual == objetivo:
            encontrado = True
            break

        explorados.add(estado_atual)

        l, c = estado_atual
        for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nl, nc = l + dl, c + dc
            if 0 <= nl < mapa["altura"] and 0 <= nc < mapa["largura"]:
                vistos.add((nl, nc))

        
        historico.append((estado_atual, vistos.copy(), explorados.copy()))
        vizinhos_atuais = vizinhos(estado_atual, mapa)

        vizinho_escolhido = None
        custo_vizinho = 0
        
        for vizinho, custo in vizinhos_atuais:
            if vizinho not in explorados:
                vizinho_escolhido = vizinho
                custo_vizinho = custo
                break
        
        if vizinho_escolhido is not None:
            caminho_retorno.append((estado_atual, custo_vizinho))
            estado_atual = vizinho_escolhido
            custo_percorrido += custo_vizinho
            n_movimentos += 1
        else:
            if len(caminho_retorno) == 0:
                break
            estado_atual, custo_revisitado = caminho_retorno.pop()
            n_movimentos += 1
            n_celulas_revisitadas += 1
            custo_percorrido += custo_revisitado
    t2 = time.perf_counter()
    return ResultadoBuscaOnline(
        encontrado = encontrado,
        tempo = t2 - t1,
        n_movimentos = n_movimentos,
        custo_percorrido = custo_percorrido,
        n_celulas_reveladas = len(vistos),
        n_celulas_revisitadas = n_celulas_revisitadas,
        historico = historico
    )