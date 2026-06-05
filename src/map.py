import os
import sys

from src.busca_classica import ResultadoBusca
from src.agente_local import EstatisticasLocal
from src.busca_online import ResultadoBuscaOnline
from typing import Optional
import time


def carregar_labirinto(filename: str):
    with open(filename, encoding='utf-8') as f:
        linhas = f.read().splitlines()

    altura = len(linhas)
    largura = max(len(linha) for linha in linhas)

    paredes = []
    inicio = None
    objetivo = None
    coletas = []

    for i in range(altura):
        row = []
        for j in range(largura):
            char = linhas[i][j] if j < len(linhas[i]) else ' '
            if char == 'A':
                inicio = (i, j)
                row.append(False)
            elif char == 'B':
                objetivo = (i, j)
                row.append(False)
            elif char == 'C':
                coletas.append((i, j))
                row.append(False)
            elif char == ' ':
                row.append(False)
            else:
                row.append(True)
        paredes.append(row)

    if inicio is None or objetivo is None:
        raise ValueError('O labirinto deve ter pontos A e B.')

    return {
        "altura": altura,
        "largura": largura,
        "paredes": paredes,
        "inicio": inicio,
        "objetivo": objetivo,
        "coletas": coletas
    }

def imprimir_labirinto(mapa: dict,
                                resultado_classico: Optional[ResultadoBusca] = None,
                                resultado_local: Optional[EstatisticasLocal] = None):
    caminho = set()
    explorados = set()

    if resultado_classico:
        if resultado_classico.encontrado:
            caminho = set(resultado_classico.caminho) 
        explorados = set(resultado_classico.estados_explorados)

    if resultado_local:
        caminho = set(resultado_local.caminho)
        explorados = set(resultado_local.explorados)

    print()
    for i in range(mapa["altura"]):
        for j in range(mapa["largura"]):
            estado = (i, j)
            if mapa["paredes"][i][j]:
                print('█', end='')
            elif estado == mapa["inicio"]:
                print('A', end='')
            elif estado == mapa["objetivo"]:
                print('B', end='')
            elif estado in caminho and estado in mapa["coletas"]:
                print('C', end='')
            elif estado in caminho and not estado in mapa["coletas"]:
                print('*', end='')
            elif estado in explorados:
                print('.', end='')
            else:
                print(' ', end='')
        print()
    print()


def animar_busca_online(mapa: dict, resultado_online: ResultadoBuscaOnline, fps: int = 10):
    """
    Reproduz o passo a passo do agente online no terminal.
    Mostra '?' para o que o agente ainda não viu.
    """
    if not resultado_online.historico:
        print("Nenhum histórico encontrado para animar.")
        return

    delay = 1.0 / fps

    # 1. Limpamos a tela de verdade APENAS UMA VEZ antes da animação começar
    print("\033[H\033[J", end='')
    # 2. Oculta o cursor piscando do terminal (Deixa a animação mais limpa)
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()
    try:
            
        for passo, (estado_agente, vistos_no_momento, explorados_no_momento) in enumerate(resultado_online.historico):
            sys.stdout.write("\033[H")

            buffer_tela = []
            

            buffer_tela.append(f"--- Busca Online: Passo {passo + 1} ---\n")
            buffer_tela.append(f"Posição do Agente: {estado_agente}\n\n")

            for i in range(mapa["altura"]):
                for j in range(mapa["largura"]):
                    estado = (i, j)
                    
                    # 1. Desenha o Agente
                    if estado == estado_agente:
                        print('@', end='')
                        
                    # 2. Desenha o que o Agente já descobriu
                    elif estado in vistos_no_momento:
                        if mapa["paredes"][i][j]:
                            print('█', end='')
                        elif estado == mapa["inicio"]:
                            print('A', end='')
                        elif estado == mapa["objetivo"]:
                            print('B', end='')
                        elif estado in mapa["coletas"]:
                            print('C', end='')
                        elif estado in explorados_no_momento:
                            print('.', end='')
                        else:
                            print(' ', end='')
                            
                    # 3. Névoa de Guerra (O que ele não conhece)
                    else:
                        print('?', end='')
                print() # Quebra de linha da matriz
                
            time.sleep(delay)

        print("\nFim da simulação online!")
    finally:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()