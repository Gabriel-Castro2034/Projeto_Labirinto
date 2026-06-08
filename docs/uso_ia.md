1. ##### **Ferramentas utilizadas**
* **Gemini versão 3.1 Pro**
* **GitHub Copilot Chat 0.48.1**

2. ##### **principais prompts utilizados**
• Aperfeiçoamento de código ou explicação no relatório técnico: "Verifique, corrija e aperfeiçoe [trecho de
código/explicação sobre algoritmo] : [código/texto]";
• Duvidas sobre a implementação dos algoritmos de busca ainda não implementados em aula;
• Aperfeiçoamento de trechos de código que podem ser substituídos por funções nativas;
• Debugging e ajuda na correção de erros: "O que tem de errado na função X?";
• Tentativa de fabricação de labirintos por meio da IA;
• Exportação de dados: "Como faço para concatenar esses objetos e gerar uma tabela CSV?";
• Dúvida de de conceitos teóricos: "Resuma o funcionamento do algoritmo de busca Simulated Annealing";
• Resolução de problemas de formatação no LaTeX: "Como faço para colocar uma imagem/tabela no LaTeX?";
• Funcionamento de bibliotecas: "Como funciona a biblioteca X? Quais os parâmetros do comando Y?"

3. ##### **trechos de código sugeridos por IA**
• Exportação via Pandas: Como já havia utilizado pandas e não sabia como exportar os resultados para
.CSV a IA sugeriu a conversão direta pelo pandas que foi bem fácil de utilizar;
• Renderização do Labirinto (Animação): Ao indagar com a IA sobre como fazer uma animação para Busca
Online ela retornou com sugestões de código que foram adotadas na função animar_busca_online no que
antes eram chamadas diretas de print;
• Adaptação do código de aulas anteriores: O código de aulas anteriores continha as funções de busca
clássicas já implementadas e junto com a ajuda da IA adaptamos essas funções para o trabalho atual;
• Arquitetura de código: Indaguei com a IA qual seria a melhor arquitetura para rodar o código e chegamos
na atual onde o main utiliza os agente para executar as funções de busca.

4. ##### **sugestões rejeitadas**
• Geração de Labirinto: A IA fez um labirinto de caracteres ASCII para testes do algoritmo de busca porém
a exportação ou escrita dele estava quebrada e não consegui utilizá-lo;
• Animação em janela ao invés de terminal: Na função animar_busca_online a IA sugeriu o uso de uma
janela a parte para executar a animação porém devido à sua complexidade e já estar avançado no projeto
optei por não mudar a função.
5. ##### **erros cometidos pela IA**
• Geração de Labirinto quebrada;
• Mudança de nome de variáveis ao corrigir ou gerar códigos;
• Excesso de complexidade na execução de algoritmos de busca afim de economizar memória.

6. ##### **como o grupo validou a solução**
• Execução: Funções sugeridas foram executadas e os relatórios de erro foram analisados e devolvidos
iterativamente até a obtenção de um código funcional.
• Validação Teórica: As explicações algorítmicas geradas pela IA para o código ou relatório foram cruzadas
com as exigências do trabalho e com o material disponibilizado pelo professor para garantir que os conceitos
estavam sendo seguidos.

7. ##### **modificações feitas pelo grupo**
• Correção de atributos trocados no código sugerido (ex: as variáveis custo_percorrido e n_movimentos
que a IA havia invertido nos resultados das buscas).
• Arredondamento de strings de ponto flutuante no relatório em LaTeX para evitar que os resultados das
tabelas extrapolassem as margens do documento no PDF final.
• Modificação dos nomes dos atributos das partes de código geradas por IA para condizer com o restante
do trabalho.

