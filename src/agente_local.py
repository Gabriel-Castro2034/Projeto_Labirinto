from typing import Tuple
from dataclasses import dataclass
import matplotlib.pyplot as plt

from src.busca_local import (
    simple_hill_climbing,
    random_restart,
    simulated_annealing
)
import random
from dataclasses import dataclass


@dataclass
class EstatisticasLocal:
    algoritmo: str
    melhor_custo: float
    pior_custo: float
    custo_medio: float
    tempo_medio: float
    iteracoes_medias: float
    taxa_sucesso: float
    curva_convergencia: list
    caminho: list[Tuple[int,int]]
    explorados: list[Tuple[int,int]]

class AgenteLocal:

    @staticmethod
    def execucao_multipla(mapa: dict, algoritmo: str, n_vezes: int = 30):
        resultados = []

        for i in range(n_vezes):
            mapa_temp = mapa.copy()
        
            nova_ordem = mapa_temp["coletas"][:]
            random.shuffle(nova_ordem)
            mapa_temp["coletas"] = nova_ordem
            
            if algoritmo == '1':
                resultado = simple_hill_climbing(mapa_temp)
            elif algoritmo == '2':
                resultado = random_restart(mapa_temp)
            elif algoritmo == '3':
                resultado = simulated_annealing(mapa_temp)
            else:
                raise ValueError(f"Opção de algoritmo '{algoritmo}' é inválida.")
            resultados.append(resultado)
        
        custos = [r.custo for r in resultados]
        tempos = [r.tempo for r in resultados]
        iteracoes = [r.iteracoes for r in resultados]

        melhor_resultado = min(resultados, key=lambda r: r.custo)
        melhor_custo=min(custos)

        if melhor_custo == float('inf'):
            taxa_sucesso = 0.0
        else:
            aceitacao = melhor_custo*1.1
            solucoes_aceitas = sum(1 for custo in custos if custo <=aceitacao)
            taxa_sucesso = (solucoes_aceitas / n_vezes) * 100

        return EstatisticasLocal(
            algoritmo=resultados[0].algoritmo,
            melhor_custo = melhor_custo,
            pior_custo=max(custos),
            custo_medio=sum(custos) / len(custos),
            tempo_medio=sum(tempos) / len(tempos),
            iteracoes_medias=sum(iteracoes) / len(iteracoes),
            curva_convergencia=melhor_resultado.curva_convergencia,
            taxa_sucesso= taxa_sucesso,
            caminho = melhor_resultado.caminho,
            explorados = melhor_resultado.explorados
        )
            
    def calcular_desempenho(self, resultado_busca: EstatisticasLocal) -> float:
        p_tempo = resultado_busca.tempo_medio * 10
        p_iteracoes = resultado_busca.iteracoes_medias * 0.01
        P_erros = p_tempo + p_iteracoes
        denominador = resultado_busca.custo_medio + P_erros
        if denominador == 0:
            return 100.0
        return 10000/denominador
        
    
    def print_resultado(self, resultado_busca):
        print(f"Algoritmo: {resultado_busca.algoritmo}")
        print(f"Melhor custo: {resultado_busca.melhor_custo}")
        print(f"Pior custo: {resultado_busca.pior_custo}")
        print(f"Custo médio: {resultado_busca.custo_medio:.2f}")
        print(f"Tempo médio: {resultado_busca.tempo_medio:.4f} segundos")
        print(f"Média de iterações: {resultado_busca.iteracoes_medias}")
        print(f"Taxa de sucesso: {resultado_busca.taxa_sucesso:.2f}%")
        
        y = resultado_busca.curva_convergencia
        x = range(1, len(y)+1)
        plt.figure(figsize=(10, 6))
        plt.title(f'Curva de Convergência do Melhor Resultado - {resultado_busca.algoritmo}', fontsize=16, fontweight='bold')
        plt.plot(x, y, color='red', label='Melhor custo atual')
        plt.xlabel('Iterações', fontsize=12)
        plt.ylabel('Custo da Solução', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

