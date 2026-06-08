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

    print("\033[H\033[J", end='')
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()
    
    try:
        for passo, (estado_agente, vistos_no_momento, explorados_no_momento) in enumerate(resultado_online.historico):
            sys.stdout.write("\033[H")

            buffer_tela = []
            
            buffer_tela.append(f"--- Busca Online: Passo {passo + 1} ---\n")
            buffer_tela.append(f"Posição do Agente: {estado_agente}\n\n")

            for i in range(mapa["altura"]):
                linha_atual = []
                for j in range(mapa["largura"]):
                    estado = (i, j)
                    
                    if estado == estado_agente:
                        linha_atual.append('@')
                        
                    elif estado in vistos_no_momento:
                        if mapa["paredes"][i][j]:
                            linha_atual.append('█')
                        elif estado == mapa["inicio"]:
                            linha_atual.append('A')
                        elif estado == mapa["objetivo"]:
                            linha_atual.append('B')
                        elif estado in mapa["coletas"]:
                            linha_atual.append('C')
                        elif estado in explorados_no_momento:
                            linha_atual.append('.')
                        else:
                            linha_atual.append(' ')                            
                    else:
                        linha_atual.append('?')
                        
                buffer_tela.append("".join(linha_atual) + "\n")
                
            sys.stdout.write("".join(buffer_tela))
            sys.stdout.flush()
            time.sleep(delay)

        print("\nFim da animação.")
    finally:
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()