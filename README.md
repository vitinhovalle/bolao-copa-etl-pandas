**🏆 Sistema de Processamento e Pontuação - Bolão da Copa**

Este projeto automatiza a gestão de um bolão de futebol, realizando todo o processo de ETL (Extract, Transform, Load) para converter palpites individuais em arquivos Excel em um ranking consolidado de participantes.

O sistema foi desenvolvido para lidar com as complexidades de um torneio real, incluindo fase de grupos, mata-mata, disputa de terceiro lugar e a pontuação do grande campeão.


**🛠️ Tecnologias Utilizadas**

Python 3.x

Pandas: Biblioteca principal para manipulação e análise de dados.

Glob: Para leitura dinâmica de múltiplos arquivos no sistema.

Openpyxl: Engine para suporte e formatação de arquivos Excel.

OS: Manipulação de caminhos e nomes de arquivos.


**🏗️ Arquitetura do Projeto (Pipeline de Dados)**

O script segue o modelo de pipeline ETL:

Extração (Extract): O sistema varre a pasta /palpites utilizando glob, identifica cada participante pelo nome do arquivo e lê as planilhas individuais. Também extrai os dados oficiais do arquivo gabarito.xlsx.

Transformação (Transform):

Limpeza e fatiamento dos dados utilizando .iloc.

Identificação dinâmica das fases (Grupos, 16-avos, Oitavas, Quartas, Semi, 3º lugar e Final).

Cruzamento de dados (Merge) entre palpites e resultados reais via idJogo.

Aplicação de regras de negócio complexas para pontuação (filtros booleanos com .loc e .isin).

Tratamento de dados ausentes (NaN) para evitar pontuação em jogos não realizados.

Carga (Load): Geração de um novo arquivo Excel (Resultado_Bolao_Copa.xlsx) contendo duas abas: o Ranking Geral e os Dados Detalhados de cada aposta.


**📈 Regras de Pontuação**

O algoritmo processa diferentes pesos para cada fase do torneio:

| Categoria | Descrição | Pontos |
| :--- | :--- | :--- |
| **Fase de Grupos** | Acerto de placar exato | 5 pts |
| **Fase de Grupos** | Acerto de vencedor e saldo de gols | 3 pts |
| **Fase de Grupos** | Acerto apenas do vencedor/empate | 2 pts |
| **Mata-Mata** | Acerto de time classificado (por fase) | Progressivo (1 a 16) |
| **3º Lugar** | Acerto do vencedor (incluindo pênaltis) | 16 pts |
| **Final** | Acerto de um finalista + Campeão | 48 pts |
| **Final** | Acerto dos dois finalistas + Campeão | 64 pts |


**🚀 Como Executar**

Clone o repositório:
git clone https://github.com/SeuUsuario/bolao-copa-etl-pandas.git

Instale as dependências:
pip install pandas openpyxl

Coloque as planilhas dos participantes na pasta /palpites.

Atualize o gabarito.xlsx com os resultados reais.

Execute o script:
python bolao_copa.py


**🧠 Desafios Superados**

Idempotência: O script foi desenvolvido para ser executado múltiplas vezes sem duplicar a pontuação, garantindo a integridade dos dados rodada após rodada.

Tratamento de "Pontos Fantasmas": Implementação de máscaras booleanas para impedir que células vazias no gabarito gerassem pontuações indevidas por coincidência de valores nulos.

Lógica de Desempate: Implementação de busca em profundidade nos dados para identificar vencedores de partidas que foram para a decisão por pênaltis.
