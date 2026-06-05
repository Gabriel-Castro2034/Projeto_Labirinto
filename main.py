from src.map import (
    carregar_labirinto,
    imprimir_labirinto,
    animar_busca_online
)
from src.agente_classico import AgenteClassico
from src.agente_local import AgenteLocal
from src.agente_online import AgenteOnline

def main():
    print("=== Simulador de Agente Inteligente ===")
    mapa = input("Qual mapa você deseja usar? (1: coleta.txt, 2: lab2.txt, 3: hard.txt): ")
    if mapa == "1":
        caminho_mapa = "data/coleta.txt"
    elif mapa == "2":
        caminho_mapa = "data/site_diferente.txt"
    elif mapa == "3":
        caminho_mapa  = "data/hard.txt"
    else:
        raise ValueError("Mapa inválido. Escolha 1, 2 ou 3.")
    
    mapa = carregar_labirinto(caminho_mapa)
    
    modo = input("Qual modo executar? (1: Clássico, 2: Coletas, 3: Online): ")    

    if modo == "1":
        imprimir_labirinto(mapa)
        agente = AgenteClassico()
        
        print('1 - Busca em Largura (BFS)')
        rbfs = agente.resolver(mapa, algoritmo="1")
        imprimir_labirinto(mapa, rbfs)
        agente.print_resultado(rbfs)
        bfs_desempenho = agente.calcular_desempenho(mapa, rbfs)
        print(f"Desempenho: {bfs_desempenho:.2f}")

        print('\n2 - Busca em Profundidade (DFS)')
        rdfs = agente.resolver(mapa, algoritmo="2")
        imprimir_labirinto(mapa, rdfs)
        agente.print_resultado(rdfs)
        dfs_desempenho = agente.calcular_desempenho(mapa, rdfs)
        print(f"Desempenho: {dfs_desempenho:.2f}")

        print('\n3 - Busca de Custo Uniforme (UCS)')
        rucs = agente.resolver(mapa, algoritmo="3")
        imprimir_labirinto(mapa, rucs)
        agente.print_resultado(rucs)
        ucs_desempenho = agente.calcular_desempenho(mapa, rucs)
        print(f"Desempenho: {ucs_desempenho:.2f}")

        print('\n4 - Greedy Best-First Search')
        rgreedy = agente.resolver(mapa, algoritmo="4")
        imprimir_labirinto(mapa, rgreedy)
        agente.print_resultado(rgreedy)
        greedy_desempenho = agente.calcular_desempenho(mapa, rgreedy)
        print(f"Desempenho: {greedy_desempenho:.2f}")

        print('\n5 - Weighted A*')
        rastar = agente.resolver(mapa, algoritmo="5", peso_astar=2.0)
        imprimir_labirinto(mapa, rastar)
        agente.print_resultado(rastar)
        rastar_desempenho = agente.calcular_desempenho(mapa, rastar)
        print(f"Desempenho: {rastar_desempenho:.2f}")

        resultados_df = [rbfs,rdfs,rucs,rgreedy,rastar]
        desempenhos = [bfs_desempenho, dfs_desempenho, ucs_desempenho, greedy_desempenho, rastar_desempenho]
        agente.comparar_algoritmos(resultados_df,desempenhos)
    
    elif modo == "2":
        imprimir_labirinto(mapa)
        agente = AgenteLocal()

        print('1 - Hill Climbing')
        hc = agente.execucao_multipla(mapa, algoritmo="1")
        imprimir_labirinto(mapa, None, hc)
        agente.print_resultado(hc)
        hc_desempenho = agente.calcular_desempenho(hc)
        print(f"Desempenho: {hc_desempenho:.2f}")

        print('\n2 - Random Restart')
        rr = agente.execucao_multipla(mapa, algoritmo="2")
        imprimir_labirinto(mapa, None, rr)
        agente.print_resultado(rr)
        rr_desempenho = agente.calcular_desempenho(rr)
        print(f"Desempenho: {rr_desempenho:.2f}")

        print('\n3 - Simulated Annealing')
        sa = agente.execucao_multipla(mapa, algoritmo="3")
        imprimir_labirinto(mapa, None, sa)
        agente.print_resultado(sa)
        sa_desempenho = agente.calcular_desempenho(sa)
        print(f"Desempenho: {sa_desempenho:.2f}")

        print('\n4 - Genético')
        ag = agente.execucao_multipla(mapa, algoritmo="4")
        imprimir_labirinto(mapa, None, ag)
        agente.print_resultado(ag)
        ag_desempenho = agente.calcular_desempenho(ag)
        print(f"Desempenho: {ag_desempenho:.2f}")
        

    elif modo == "3":
        agente = AgenteOnline()
        res = agente.resolver(mapa)
        print("Aperte Enter para animar a busca online...")
        input()
        animar_busca_online(mapa, res,60)
        agente.calcular_desempenho(res)
        agente.printResultado(res)
        agente.compara_offline(mapa, res)
        desempenho = agente.calcular_desempenho(res)
        print(f"Desempenho: {desempenho:.2f}")
    else:
        raise ValueError("Modo inválido. Escolha 1, 2 ou 3.")

if __name__ == "__main__":
    main()