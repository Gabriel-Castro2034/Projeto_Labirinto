```markdown
# Agente Inteligente em Labirinto: Busca Clássica, Local e Online

Este repositório contém o desenvolvimento completo do Trabalho Prático da disciplina de **Inteligência Artificial (CSI457 / CS1701)** da **Universidade Federal de Ouro Preto (UFOP)**. O projeto consiste na modelagem, implementação e análise experimental de agentes inteligentes operando em ambientes labirínticos sob três paradigmas distintos de resolução de problemas: Busca Clássica (offline), Busca Local (otimização combinatória) e Busca Online (exploração sob observabilidade parcial).

---

## 🚀 Contexto do Projeto

O objetivo do agente é navegar eficientemente por uma matriz de estados discretos contendo paredes (`█`), espaços livres (` `), uma coordenada inicial de origem (`A`), um objetivo final de destino (`B`) e, opcionalmente, múltiplos pontos de coleta obrigatórios (`C`).

O sistema divide-se em três partes principais:
1. **Parte I - Busca Clássica (Ambiente Conhecido):** Planejamento *offline* completo com caminhos ótimos e subótimos.
2. **Parte II - Busca Local (Pontos de Coleta):** Resolução do problema do caixeiro-viajante aplicado ao labirinto, otimizando a sequência de visitação das coletas obrigatórias.
3. **Parte III - Busca Online (Ambiente Desconhecido):** Exploração em tempo real sob névoa de guerra, onde o agente intercala percepção local, atualização de modelo interno e movimentação física.

---

## 🛠️ Arquitetura do Repositório

O projeto adota uma arquitetura modular orientada a objetos de alta coesão e baixo acoplamento, estruturada da seguinte forma:

```text
├── data/                       # Arquivos de entrada de labirintos (.txt)
│   ├── easy.txt                # Labirinto de controle de escala reduzida
│   ├── big.txt                 # Teste de estresse com alta densidade de estados
│   ├── multiple.txt            # Labirinto aberto com múltiplos caminhos viáveis
│   └── hard.txt                # Cenário complexo projetado em espiral para busca local
├── src/                        # Código-fonte do sistema
│   ├── busca_classica.py       # Algoritmos de busca clássica e fila de prioridades (Min-Heap)
│   ├── busca_local.py          # Meta-heurísticas de busca local (operador Swap)
│   ├── busca_online.py         # Algoritmo DFS Online e retração física (Backtracking)
│   ├── agente_classico.py      # Orquestrador, cálculo de desempenho e exportação de dados
│   ├── agente_local.py         # Módulo de simulação local, estatísticas e convergência
│   ├── agente_online.py        # Controlador de ciclo percepção-ação online e interface
│   └── map.py                  # Parser de arquivos, buffers de terminal e janelas visuais
├── main.py                     # Ponto de entrada central (CLI interativo)
├── CSV_classico.csv            # Tabela de métricas gerada para a Busca Clássica
├── CSV_Local.csv               # Tabela de métricas gerada para a Busca Local
└── CSV_Online.csv              # Tabela de métricas gerada para a Busca Online

```

---

## 🧠 Algoritmos Implementados

### 1. Busca Clássica (Best-First Search centralizada)

Implementados através de uma estrutura genérica de fila de prioridades baseada em um *Min-Heap*, diferenciando-se estritamente pela injeção matemática da função de avaliação $f(n)$:

* **Busca em Largura (BFS):** Exploração em camadas orientada por fila FIFO. Garante a otimalidade em caminhos de custo unificado.
* **Busca em Profundidade (DFS):** Exploração linear profunda orientada por pilha (LIFO). Comportamento subótimo com baixo consumo de memória imediata.
* **Busca de Custo Uniforme (UCS):** Minimização baseada estritamente no custo real acumulado do trajeto:
$$f(n) = g(n)$$


* **Busca Gulosa (Greedy BFS):** Direcionamento focado exclusivamente na estimativa heurística até o objetivo (míope):
$$f(n) = h(n)$$


* **Busca $A^*$ e $A^*$ Ponderado (Weighted $A^*$):** Equilíbrio entre custo real e estimativa, parametrizado com um peso ajustável ($w \ge 1.0$) para aceleração de convergência:
$$f(n) = g(n) + w \cdot h(n)$$


* *Heurística Adotada:* **Distância de Manhattan**, provada matematicamente como admissível e consistente para este domínio ortogonal.



### 2. Busca Local (Otimização Espacial)

Focada na ordenação ótima de uma lista de tamanho $N$ de pontos de coleta obrigatórios (`C`). O espaço de estados é definido por permutações combinatórias, avaliadas pelo custo físico real de locomoção calculado de forma subjacente pelo motor do $A^*$:

* **Simple Hill Climbing (Steepest-Ascent):** Avaliação exaustiva de toda a vizinhança gerada pelo operador de *Swap* ($O(N^2)$). Migra obrigatoriamente para o melhor vizinho. Altamente suscetível a travamentos em mínimos locais.
* **Random Restart Hill Climbing:** Introdução de diversificação estocástica. Instancia $k$ execuções independentes do Hill Climbing a partir de sementes embaralhadas (*shuffles*), mantendo um registro elitista do melhor resultado histórico global.
* **Simulated Annealing (Têmpera Simulada):** Meta-heurística inspirada na termodinâmica. Sorteia um único vizinho aleatório por iteração e aceita transições para estados piores de acordo com a distribuição probabilística de Boltzmann:
$$P = e^{-\frac{\Delta E}{T}}$$



Apresenta decaimento geométrico da temperatura ($T$) para transicionar de uma exploração ampla (*exploration*) para uma explotação refinada (*exploitation*).

### 3. Busca Online (Observabilidade Parcial)

* **DFS Online:** O agente navega sem conhecimento prévio do mapa. O planejamento ocorre de forma intercalada com a execução física (*interleaving planning and execution*). O agente mapeia dinamicamente os arredores através de sensores locais (`vistos`) e marca células consolidadas (`explorados`). Ao atingir um beco sem saída, realiza o *backtracking* de forma física (caminhando em marcha ré através da pilha `caminho_retorno`), sofrendo penalizações diretas em movimentos e custo real de combustível.

---

## 📊 Engenharia de Dados e Estatísticas

O repositório utiliza a biblioteca **Pandas** para consolidar os resultados experimentais. O sistema isola as variáveis pesadas de renderização (listas de coordenadas de caminhos e estados) e exporta estritamente as métricas analíticas em arquivos `.csv` formatados para leitura imediata em sistemas Microsoft Excel em português brasileiro (separador de colunas por ponto-e-vírgula `;` e decimais por vírgula `,` com codificação `utf-8-sig` para proteção de acentos).

### Métricas Capturadas por Linha de Teste:

* **Busca Clássica:** Custo total da rota, quantidade de nós explorados, quantidade de nós expandidos na árvore, tamanho máximo atingido pela fronteira de memória e tempo de CPU de alta resolução (`perf_counter`).
* **Busca Local:** Melhor custo do grupo, pior custo, custo médio amostral, iterações gastas até a convergência estática, taxa de sucesso e o array vetorial da curva de convergência.
* **Busca Online:** Status de sucesso, tempo total de navegação, movimentos físicos executados, custo total consumido, contagem de células inéditas reveladas e volume de células revisitadas devido a retrações.

---

## 📺 Recursos de Visualização

O repositório possui duas interfaces de renderização para o monitoramento passo a passo do agente inteligente:

1. **Terminal Animado (CLI):** Utiliza sequências de escape ANSI (`\033[H`) para reescrever dinamicamente o quadro do labirinto diretamente no console do VS Code, permitindo assistir ao agente avançando às cegas e revelando os caracteres escondidos sob os pontos de interrogação (`?`).
2. **Interface Gráfica Nativa (Tkinter):** Uma janela independente do Windows que renderiza graficamente o labirinto usando loops de atualização temporal assíncronos (`root.after`), evitando travamentos da interface e permitindo o ajuste de força de quadros por segundo (FPS).

---

## ⚙️ Pré-requisitos e Execução

### Instalação

O projeto utiliza apenas a biblioteca padrão do Python para execução e o ecossistema Pandas/Matplotlib para Ciência de Dados. Certifique-se de possuir o ambiente configurado:

```bash
# Clone o repositório
git clone [https://github.com/gabriel-castro2034/projeto_labirinto.git](https://github.com/gabriel-castro2034/projeto_labirinto.git)
cd projeto_labirinto

# Instale as dependências de análise de dados
pip install pandas matplotlib seaborn

```

### Execução Centralizada

O sistema possui um menu interativo por console executável pelo arquivo principal:

```bash
python main.py

```

Siga as instruções na tela para:

1. Escolher o arquivo de mapa do labirinto (armazenados em `data/`).
2. Selecionar o Modo de Operação (1 - Clássico, 2 - Local, 3 - Online).
3. Visualizar as estatísticas completas, tabelas e disparar a animação visual da jornada do agente.

---

## 👤 Autor

* **Gabriel Henrique Fonseca Castro** - Aluno de Graduação - Universidade Federal de Ouro Preto (UFOP).
* Trabalho Prático desenvolvido para a disciplina de **Inteligência Artificial (CSI457)**.
* Data de Conclusão e Consolidação: 8 de Junho de 2026.

```

``````markdown
# Agente Inteligente em Labirinto: Busca Clássica, Local e Online

Este repositório contém o desenvolvimento completo do Trabalho Prático da disciplina de **Inteligência Artificial (CSI457 / CS1701)** da **Universidade Federal de Ouro Preto (UFOP)**. O projeto consiste na modelagem, implementação e análise experimental de agentes inteligentes operando em ambientes labirínticos sob três paradigmas distintos de resolução de problemas: Busca Clássica (offline), Busca Local (otimização combinatória) e Busca Online (exploração sob observabilidade parcial).

---

## 🚀 Contexto do Projeto

O objetivo do agente é navegar eficientemente por uma matriz de estados discretos contendo paredes (`█`), espaços livres (` `), uma coordenada inicial de origem (`A`), um objetivo final de destino (`B`) e, opcionalmente, múltiplos pontos de coleta obrigatórios (`C`).

O sistema divide-se em três partes principais:
1. **Parte I - Busca Clássica (Ambiente Conhecido):** Planejamento *offline* completo com caminhos ótimos e subótimos.
2. **Parte II - Busca Local (Pontos de Coleta):** Resolução do problema do caixeiro-viajante aplicado ao labirinto, otimizando a sequência de visitação das coletas obrigatórias.
3. **Parte III - Busca Online (Ambiente Desconhecido):** Exploração em tempo real sob névoa de guerra, onde o agente intercala percepção local, atualização de modelo interno e movimentação física.

---

## 🛠️ Arquitetura do Repositório

O projeto adota uma arquitetura modular orientada a objetos de alta coesão e baixo acoplamento, estruturada da seguinte forma:

```text
├── data/                       # Arquivos de entrada de labirintos (.txt)
│   ├── easy.txt                # Labirinto de controle de escala reduzida
│   ├── big.txt                 # Teste de estresse com alta densidade de estados
│   ├── multiple.txt            # Labirinto aberto com múltiplos caminhos viáveis
│   └── hard.txt                # Cenário complexo projetado em espiral para busca local
├── src/                        # Código-fonte do sistema
│   ├── busca_classica.py       # Algoritmos de busca clássica e fila de prioridades (Min-Heap)
│   ├── busca_local.py          # Meta-heurísticas de busca local (operador Swap)
│   ├── busca_online.py         # Algoritmo DFS Online e retração física (Backtracking)
│   ├── agente_classico.py      # Orquestrador, cálculo de desempenho e exportação de dados
│   ├── agente_local.py         # Módulo de simulação local, estatísticas e convergência
│   ├── agente_online.py        # Controlador de ciclo percepção-ação online e interface
│   └── map.py                  # Parser de arquivos, buffers de terminal e janelas visuais
├── main.py                     # Ponto de entrada central (CLI interativo)
├── CSV_classico.csv            # Tabela de métricas gerada para a Busca Clássica
├── CSV_Local.csv               # Tabela de métricas gerada para a Busca Local
└── CSV_Online.csv              # Tabela de métricas gerada para a Busca Online

```

---

## 🧠 Algoritmos Implementados

### 1. Busca Clássica (Best-First Search centralizada)

Implementados através de uma estrutura genérica de fila de prioridades baseada em um *Min-Heap*, diferenciando-se estritamente pela injeção matemática da função de avaliação $f(n)$:

* **Busca em Largura (BFS):** Exploração em camadas orientada por fila FIFO. Garante a otimalidade em caminhos de custo unificado.
* **Busca em Profundidade (DFS):** Exploração linear profunda orientada por pilha (LIFO). Comportamento subótimo com baixo consumo de memória imediata.
* **Busca de Custo Uniforme (UCS):** Minimização baseada estritamente no custo real acumulado do trajeto:
$$f(n) = g(n)$$


* **Busca Gulosa (Greedy BFS):** Direcionamento focado exclusivamente na estimativa heurística até o objetivo (míope):
$$f(n) = h(n)$$


* **Busca $A^*$ e $A^*$ Ponderado (Weighted $A^*$):** Equilíbrio entre custo real e estimativa, parametrizado com um peso ajustável ($w \ge 1.0$) para aceleração de convergência:
$$f(n) = g(n) + w \cdot h(n)$$


* *Heurística Adotada:* **Distância de Manhattan**, provada matematicamente como admissível e consistente para este domínio ortogonal.



### 2. Busca Local (Otimização Espacial)

Focada na ordenação ótima de uma lista de tamanho $N$ de pontos de coleta obrigatórios (`C`). O espaço de estados é definido por permutações combinatórias, avaliadas pelo custo físico real de locomoção calculado de forma subjacente pelo motor do $A^*$:

* **Simple Hill Climbing (Steepest-Ascent):** Avaliação exaustiva de toda a vizinhança gerada pelo operador de *Swap* ($O(N^2)$). Migra obrigatoriamente para o melhor vizinho. Altamente suscetível a travamentos em mínimos locais.
* **Random Restart Hill Climbing:** Introdução de diversificação estocástica. Instancia $k$ execuções independentes do Hill Climbing a partir de sementes embaralhadas (*shuffles*), mantendo um registro elitista do melhor resultado histórico global.
* **Simulated Annealing (Têmpera Simulada):** Meta-heurística inspirada na termodinâmica. Sorteia um único vizinho aleatório por iteração e aceita transições para estados piores de acordo com a distribuição probabilística de Boltzmann:
$$P = e^{-\frac{\Delta E}{T}}$$



Apresenta decaimento geométrico da temperatura ($T$) para transicionar de uma exploração ampla (*exploration*) para uma explotação refinada (*exploitation*).

### 3. Busca Online (Observabilidade Parcial)

* **DFS Online:** O agente navega sem conhecimento prévio do mapa. O planejamento ocorre de forma intercalada com a execução física (*interleaving planning and execution*). O agente mapeia dinamicamente os arredores através de sensores locais (`vistos`) e marca células consolidadas (`explorados`). Ao atingir um beco sem saída, realiza o *backtracking* de forma física (caminhando em marcha ré através da pilha `caminho_retorno`), sofrendo penalizações diretas em movimentos e custo real de combustível.

---

## 📊 Engenharia de Dados e Estatísticas

O repositório utiliza a biblioteca **Pandas** para consolidar os resultados experimentais. O sistema isola as variáveis pesadas de renderização (listas de coordenadas de caminhos e estados) e exporta estritamente as métricas analíticas em arquivos `.csv` formatados para leitura imediata em sistemas Microsoft Excel em português brasileiro (separador de colunas por ponto-e-vírgula `;` e decimais por vírgula `,` com codificação `utf-8-sig` para proteção de acentos).

### Métricas Capturadas por Linha de Teste:

* **Busca Clássica:** Custo total da rota, quantidade de nós explorados, quantidade de nós expandidos na árvore, tamanho máximo atingido pela fronteira de memória e tempo de CPU de alta resolução (`perf_counter`).
* **Busca Local:** Melhor custo do grupo, pior custo, custo médio amostral, iterações gastas até a convergência estática, taxa de sucesso e o array vetorial da curva de convergência.
* **Busca Online:** Status de sucesso, tempo total de navegação, movimentos físicos executados, custo total consumido, contagem de células inéditas reveladas e volume de células revisitadas devido a retrações.

---

## 📺 Recursos de Visualização

O repositório possui duas interfaces de renderização para o monitoramento passo a passo do agente inteligente:

1. **Terminal Animado (CLI):** Utiliza sequências de escape ANSI (`\033[H`) para reescrever dinamicamente o quadro do labirinto diretamente no console do VS Code, permitindo assistir ao agente avançando às cegas e revelando os caracteres escondidos sob os pontos de interrogação (`?`).
2. **Interface Gráfica Nativa (Tkinter):** Uma janela independente do Windows que renderiza graficamente o labirinto usando loops de atualização temporal assíncronos (`root.after`), evitando travamentos da interface e permitindo o ajuste de força de quadros por segundo (FPS).

---

## ⚙️ Pré-requisitos e Execução

### Instalação

O projeto utiliza apenas a biblioteca padrão do Python para execução e o ecossistema Pandas/Matplotlib para Ciência de Dados. Certifique-se de possuir o ambiente configurado:

```bash
# Clone o repositório
git clone [https://github.com/gabriel-castro2034/projeto_labirinto.git](https://github.com/gabriel-castro2034/projeto_labirinto.git)
cd projeto_labirinto

# Instale as dependências de análise de dados
pip install pandas matplotlib seaborn

```

### Execução Centralizada

O sistema possui um menu interativo por console executável pelo arquivo principal:

```bash
python main.py

```

Siga as instruções na tela para:

1. Escolher o arquivo de mapa do labirinto (armazenados em `data/`).
2. Selecionar o Modo de Operação (1 - Clássico, 2 - Local, 3 - Online).
3. Visualizar as estatísticas completas, tabelas e disparar a animação visual da jornada do agente.

---

## 👤 Autor

* **Gabriel Henrique Fonseca Castro** - Aluno de Graduação - Universidade Federal de Ouro Preto (UFOP).
* Trabalho Prático desenvolvido para a disciplina de **Inteligência Artificial (CSI457)**.
* Data de Conclusão e Consolidação: 8 de Junho de 2026.

```

```
