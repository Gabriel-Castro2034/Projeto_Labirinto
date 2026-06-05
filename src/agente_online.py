from src.busca_online import (
    ResultadoBuscaOnline,
    busca_profundidade_online
)
from src.busca_classica import busca_weighted_astar

class AgenteOnline:
    def resolver(self, mapa: dict):
        return busca_profundidade_online(mapa)
    
    def compara_offline(self, mapa: dict, resultado_online: ResultadoBuscaOnline):
        resultado_offline = busca_weighted_astar(mapa)
        comp = resultado_online.custo_percorrido / resultado_offline.custo
        print(f"Comparação com offline: {comp:.2f} vezes o custo do offline (Busca A*)")

    def calcular_desempenho(self, resultado: ResultadoBuscaOnline):
        if not resultado.encontrado:
            return 0.0
        p_movimentos = resultado.n_movimentos * 0.01
        p_custo = resultado.custo_percorrido * 0.01
        p_tempo = resultado.tempo * 10
        p_revisita = resultado.n_celulas_revisitadas * 0.02
        denominador = p_movimentos + p_custo + p_tempo + p_revisita
        if denominador == 0:
            return 100.0
        return 10000 / denominador

    def printResultado(self, resultado: ResultadoBuscaOnline):
        print(f"Encontrado: {resultado.encontrado}")
        print(f"Tempo gasto: {resultado.tempo:.4f} segundos")
        print(f"Custo percorrido: {resultado.custo_percorrido:.2f}")
        print(f"Número de movimentos: {resultado.n_movimentos}")
        print(f"Número de células reveladas: {resultado.n_celulas_reveladas}")
        print(f"Número de células revisitadas: {resultado.n_celulas_revisitadas}")
