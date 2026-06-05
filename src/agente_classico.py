from src.busca_classica import (
    busca_largura,
    busca_profundidade,
    busca_custo_uniforme,
    busca_gulosa,
    busca_weighted_astar,
    ResultadoBusca
)
from typing import List
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

class AgenteClassico:

    def resolver(self, mapa: dict, algoritmo: str, peso_astar: float = 1.0):

        if algoritmo == '1':
            return busca_largura(mapa)
        elif algoritmo == '2':
            return busca_profundidade(mapa)
        elif algoritmo == '3':
            return busca_custo_uniforme(mapa)
        elif algoritmo == '4':
            return busca_gulosa(mapa)
        elif algoritmo == '5':
            return busca_weighted_astar(mapa, peso=peso_astar)
        else:
            raise ValueError(f"Opção de algoritmo '{algoritmo}' é inválida.")
            
    def calcular_desempenho(self, mapa: dict, resultado_busca):
        
        if not resultado_busca.encontrado:
            return 0.0
        
        r_otimo = busca_weighted_astar(mapa, peso=1.0)
        c_otimo = r_otimo.custo

        custo = resultado_busca.custo
        nos_expandidos = resultado_busca.nos_expandidos * 0.1
        tempo = resultado_busca.tempo * 1000
        nos_revisitados = resultado_busca.nos_revisitados * 0.5
        denominador = custo + nos_expandidos + tempo + nos_revisitados
        if denominador == 0:
            return 100.0
        return 100*(c_otimo/denominador)
    
    def print_resultado(self, resultado_busca):
        print(f"Algoritmo: {resultado_busca.algoritmo}")
        print(f"Encontrado: {resultado_busca.encontrado}")
        print(f"Custo do caminho: {resultado_busca.custo:.2f}")
        print(f"Tamanho do caminho: {len(resultado_busca.caminho)}")
        print(f"Nós explorados: {resultado_busca.nos_explorados}")
        print(f"Nós expandidos: {resultado_busca.nos_expandidos}")
        print(f"Tempo: {resultado_busca.tempo:.4f} segundos")
        print(f"Máximo na fronteira: {resultado_busca.max_fronteira}")
        print(f"Nós revisitados: {resultado_busca.nos_revisitados}")

    def comparar_algoritmos(self, resultados: List[ResultadoBusca], desempenhos: List[float]):
        resultados_df = pd.DataFrame({
            'Algoritmo': [r.algoritmo for r in resultados],
            'Desempenho': desempenhos,
            'Nós Explorados': [r.nos_explorados for r in resultados],
            'Nós Expandidos': [r.nos_expandidos for r in resultados],
            'Tempo (s)': [r.tempo for r in resultados]
        })

        sns.set_style('whitegrid')
        
        fig, eixos = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
        fig.suptitle('Comparação de Algoritmos de Busca Clássica', fontsize=18, fontweight='bold')

        # 1º Gráfico: Desempenho
        sns.barplot(x='Algoritmo', y='Desempenho', data=resultados_df, hue='Algoritmo', ax=eixos[0, 0], legend=False)
        eixos[0, 0].set_title('Desempenho (J) - Quanto maior, melhor')
        
        # 2º Gráfico: Nós Explorados
        sns.barplot(x='Algoritmo', y='Nós Explorados', data=resultados_df, hue='Algoritmo', ax=eixos[0, 1], legend=False)
        eixos[0, 1].set_title('Nós Explorados')

        # 3º Gráfico: Nós Expandidos
        sns.barplot(x='Algoritmo', y='Nós Expandidos', data=resultados_df, hue='Algoritmo', ax=eixos[1, 0], legend=False)
        eixos[1, 0].set_title('Nós Expandidos')

        # 4º Gráfico: Tempo
        sns.barplot(x='Algoritmo', y='Tempo (s)', data=resultados_df, hue='Algoritmo', ax=eixos[1, 1], legend=False)
        eixos[1, 1].set_title('Tempo de Execução (segundos)')

        for linha in eixos:
            for eixo in linha: 
                eixo.set_xlabel('')
                for container in eixo.containers:
                    eixo.bar_label(container, padding=3, fmt='%.3f')

        plt.tight_layout()
        plt.show()
