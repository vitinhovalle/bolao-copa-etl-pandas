# %%
# importando bibliotecas
import pandas as pd
import glob
import os

# %%
# declarando a lista de tabelas
tabelas_separadas = []

# buscando os palpites
palpites = glob.glob("palpites/*.xlsx")

# abrindo a contagem de participantes
cont_participantes = 0

# separando o nome de participantes
participantes = []

# adicionando a lista de campeoes dos participantes
campeoes_palpites = {}

# adicionando a lista de terceiros colocados dos participantes
terceiro_palpites = {}

# percorrendo todos arquivos dos participantes
for arquivo in palpites:

    # lendo a tabela
    tabela = pd.read_excel(arquivo)

    # declarando a lista de blocos
    blocos_separados = []

    # aumentando a contagem de participantes
    cont_participantes = cont_participantes + 1

    # percorrendo as fases (grupos e mata-mata)
    for linha_inicial in [1, 52]:
        # percorrendo as colunas dos jogos
        for coluna_inicial in [0,9,18]:
            # selecionando os jogos
            bloco = tabela.iloc[linha_inicial:linha_inicial + 47, 
                                coluna_inicial:coluna_inicial + 8]

            # selecionando os placares dos jogos (que possuem um X)
            jogos = bloco[bloco.iloc[:, 2] == "X"]

            # renomeando as colunas dos jogos
            jogos.columns = ["mandante", "golsMandante", 
                             "X", "golsVisitante", 
                             "visitante", "horario", 
                             "pontosMandante", "pontosVisitante"]

            # adicionando apenas as colunas que me interessam
            blocos_separados.append(
                jogos[["mandante", "golsMandante", 
                       "golsVisitante", "visitante", 
                       "pontosMandante", "pontosVisitante"]])

    # unindo os blocos de jogos de cada palpite
    tabela_limpa = pd.concat(blocos_separados)

    # escrevendo o nome do participante em todas as linhas do arquivo, para identificação
    nome_com_extensao = os.path.basename(arquivo)
    nome_participante = nome_com_extensao.replace("palpite","").replace(".xlsx", "")
    tabela_limpa["participante"] = nome_participante
    
    # adicionando participante na lista
    participantes.append(nome_participante)

    # identificando as fases
    tabela_limpa.loc[tabela_limpa.index < 52, "fase"] = "grupo"

    # agrupando as tabelas em uma unica lista
    tabelas_separadas.append(tabela_limpa)

    # adicionando campeoes
    campeoes_palpites[nome_participante] = tabela.iat[97,27]

    # adicionando terceiros
    if (tabela.iat[91,19] > tabela.iat[91,21]):
        terceiro_palpites[nome_participante] = tabela.iat[91,18]
    elif (tabela.iat[91,19] < tabela.iat[91,21]):
        terceiro_palpites[nome_participante] = tabela.iat[91,22]
    elif (tabela.iat[92,19] > tabela.iat[92,21]):
        terceiro_palpites[nome_participante] = tabela.iat[91,18]
    elif (tabela.iat[92,19] < tabela.iat[92,21]):
        terceiro_palpites[nome_participante] = tabela.iat[91,22]
    else:
        terceiro_palpites[nome_participante] = tabela.iat[91,18]

# unindo as tabelas em uma só
todos_palpites = pd.concat(tabelas_separadas)

# adicionando a coluna idJogo
todos_palpites.insert(0, "idJogo", 0)

# classificando as fases do mata-mata
for a in range(cont_participantes):
    todos_palpites.iloc[(72 + (104*a)):
                      (88 + (104*a)),
                      8] = "16 avos"
    
    todos_palpites.iloc[(88 + (104*a)):
                      (96 + (104*a)),
                      8] = "oitavas"
    
    todos_palpites.iloc[(96 + (104*a)):
                      (100 + (104*a)),
                      8] = "quartas"
    
    todos_palpites.iloc[(100 + (104*a)):
                      (102 + (104*a)),
                      8] = "semifinal"
    
    todos_palpites.iloc[(102 + (104*a)):
                      (103 + (104*a)),
                      8] = "3º lugar"
    
    todos_palpites.iloc[(103 + (104*a)):
                      (104 + (104*a)),
                      8] = "final"

    # identificando os jogos
    todos_palpites.iloc[(104*a):(104*(a+1)), 0] = range(1,105)

# %%
# lendo o gabarito
gabarito = pd.read_excel("gabarito.xlsx")

# declarando a lista de resultados
resultados_oficiais = []

# percorrendo as fases (grupos e mata-mata)
for linha_inicial in [1, 52]:

    # percorrendo as colunas dos jogos
    for coluna_inicial in [0,9,18]:

        # selecionando os jogos
        bloco = gabarito.iloc[linha_inicial:linha_inicial + 47, 
                            coluna_inicial:coluna_inicial + 8]

        # selecionando os placares dos jogos (que possuem um X)
        jogos = bloco[bloco.iloc[:, 2] == "X"]

        # renomeando as colunas dos jogos
        jogos.columns = ["mandante", "golsMandante", 
                         "X", "golsVisitante", 
                         "visitante", "horario", 
                         "pontosMandante", "pontosVisitante"]

        # adicionando apenas as colunas que me interessam
        resultados_oficiais.append(
            jogos[["mandante", "golsMandante", 
                   "golsVisitante", "visitante", 
                   "pontosMandante", "pontosVisitante"]])

# unindo os blocos de jogos de cada palpite
gabarito_limpo = pd.concat(resultados_oficiais)

# adicionando a coluna idJogo
gabarito_limpo.insert(0,"idJogo", 0)

# identificando os jogos
gabarito_limpo.iloc[0:104, 0] = range(1,105)

# juntando os palpites com o gabarito
tabela_final = pd.merge(todos_palpites, gabarito_limpo, 
                        on=["idJogo"], how="left", 
                        suffixes=["Palpite", "Real"])

# colocando os id's do jogo como índice da tabela
tabela_final = tabela_final.set_index("idJogo")

# %%
# identificando fases do mata-mata
filtro = tabela_final["fase"] == "16 avos"
times_16avos = pd.concat([tabela_final[filtro].iloc[0:16, 8], 
                          tabela_final[filtro].iloc[0:16, 11]])

filtro = tabela_final["fase"] == "oitavas"
times_oitavas = pd.concat([tabela_final[filtro].iloc[0:8, 8], 
                          tabela_final[filtro].iloc[0:8, 11]])

filtro = tabela_final["fase"] == "quartas"
times_quartas = pd.concat([tabela_final[filtro].iloc[0:4, 8], 
                          tabela_final[filtro].iloc[0:4, 11]])

filtro = tabela_final["fase"] == "semifinal"
times_semifinal = pd.concat([tabela_final[filtro].iloc[0:2, 8], 
                          tabela_final[filtro].iloc[0:2, 11]])

filtro = tabela_final["fase"] == "3º lugar"
times_3lugar = pd.concat([tabela_final[filtro].iloc[0:1, 8], 
                          tabela_final[filtro].iloc[0:1, 11]])

filtro = tabela_final["fase"] == "final"
times_final = pd.concat([tabela_final[filtro].iloc[0:1, 8], 
                          tabela_final[filtro].iloc[0:1, 11]])


# %%
# conferindo se o jogo já ocorreu
jogo_ocorreu = tabela_final["golsMandanteReal"].notna()

# acrescentando coluna de pontuação
tabela_final["pontos"] = 0

# aplicando lógicas de pontuação da fase de grupos
tabela_final.loc[(
    ((tabela_final["golsMandantePalpite"] 
      == tabela_final["golsMandanteReal"]) 
    | 
    (tabela_final["golsVisitantePalpite"] 
     == tabela_final["golsVisitanteReal"])
    )
    &
    (tabela_final["fase"] == "grupo")
    & 
    jogo_ocorreu
    ), "pontos"
] = 1

tabela_final.loc[(
    (tabela_final["pontosMandantePalpite"] 
     == tabela_final["pontosMandanteReal"])
    &
    (tabela_final["fase"] == "grupo")
    & 
    jogo_ocorreu
    ), "pontos"
] = 2

tabela_final.loc[(
    ((tabela_final["golsMandantePalpite"] 
      - tabela_final["golsMandanteReal"]) 
    == 
    (tabela_final["golsVisitantePalpite"] 
     - tabela_final["golsVisitanteReal"])
    )
    &
    (tabela_final["fase"] == "grupo")
    & 
    jogo_ocorreu
    ), "pontos"
] = 3

tabela_final.loc[(
    ((tabela_final["golsMandantePalpite"] 
      == tabela_final["golsMandanteReal"]) 
    & 
    (tabela_final["golsVisitantePalpite"] 
     == tabela_final["golsVisitanteReal"])
    )
    &
    (tabela_final["fase"] == "grupo")
    & 
    jogo_ocorreu
    ), "pontos" 
] = 5

# %%
# aplicando lógicas de pontuação do mata-mata
tabela_final.loc[(
    (((tabela_final["mandantePalpite"].isin(times_16avos))
    &
    (~tabela_final["visitantePalpite"].isin(times_16avos)))
    |
    ((~tabela_final["mandantePalpite"].isin(times_16avos))
    &
    (tabela_final["visitantePalpite"].isin(times_16avos))))
    &
    (tabela_final["fase"] == "16 avos")
    ), "pontos"
] = 1

tabela_final.loc[(
    (tabela_final["mandantePalpite"].isin(times_16avos))
    &
    (tabela_final["visitantePalpite"].isin(times_16avos))
    &              
    (tabela_final["fase"] == "16 avos")
    ), "pontos"
] = 2

tabela_final.loc[(
    (((tabela_final["mandantePalpite"].isin(times_oitavas))
    &
    (~tabela_final["visitantePalpite"].isin(times_oitavas)))
    |
    ((~tabela_final["mandantePalpite"].isin(times_oitavas))
    &
    (tabela_final["visitantePalpite"].isin(times_oitavas))))
    &
    (tabela_final["fase"] == "oitavas")
    ), "pontos"
] = 2

tabela_final.loc[(
    (tabela_final["mandantePalpite"].isin(times_oitavas))
    &
    (tabela_final["visitantePalpite"].isin(times_oitavas))
    &              
    (tabela_final["fase"] == "oitavas")
    ), "pontos"
] = 4

tabela_final.loc[(
    (((tabela_final["mandantePalpite"].isin(times_quartas))
    &
    (~tabela_final["visitantePalpite"].isin(times_quartas)))
    |
    ((~tabela_final["mandantePalpite"].isin(times_quartas))
    &
    (tabela_final["visitantePalpite"].isin(times_quartas))))
    &
    (tabela_final["fase"] == "quartas")
    ), "pontos"
] = 4

tabela_final.loc[(
    (tabela_final["mandantePalpite"].isin(times_quartas))
    &
    (tabela_final["visitantePalpite"].isin(times_quartas))
    &              
    (tabela_final["fase"] == "quartas")
    ), "pontos"
] = 8

tabela_final.loc[(
    (((tabela_final["mandantePalpite"].isin(times_semifinal))
    &
    (~tabela_final["visitantePalpite"].isin(times_semifinal)))
    |
    ((~tabela_final["mandantePalpite"].isin(times_semifinal))
    &
    (tabela_final["visitantePalpite"].isin(times_semifinal))))
    &
    (tabela_final["fase"] == "semifinal")
    ), "pontos"
] = 8

tabela_final.loc[(
    (tabela_final["mandantePalpite"].isin(times_semifinal))
    &
    (tabela_final["visitantePalpite"].isin(times_semifinal))
    &              
    (tabela_final["fase"] == "semifinal")
    ), "pontos"
] = 16

tabela_final.loc[(
    (((tabela_final["mandantePalpite"].isin(times_final))
    &
    (~tabela_final["visitantePalpite"].isin(times_final)))
    |
    ((~tabela_final["mandantePalpite"].isin(times_final))
    &
    (tabela_final["visitantePalpite"].isin(times_final))))
    &
    (tabela_final["fase"] == "final")
    ), "pontos"
] = 16

tabela_final.loc[(
    (tabela_final["mandantePalpite"].isin(times_final))
    &
    (tabela_final["visitantePalpite"].isin(times_final))
    &              
    (tabela_final["fase"] == "final")
    ), "pontos"
] = 32

# %%
# pontos para o acerto do Grande Campeão!
for participante, palpite in campeoes_palpites.items():
    if (palpite == gabarito.iloc[97,27]):
        tabela_final.loc[((
            ((tabela_final["mandantePalpite"].isin(times_final))
            &
            (~tabela_final["visitantePalpite"].isin(times_final)))
            |
            ((~tabela_final["mandantePalpite"].isin(times_final))
            &
            (tabela_final["visitantePalpite"].isin(times_final))))
            &
            (tabela_final["fase"] == "final")
            &
            (tabela_final["participante"] == participante)
            ), "pontos"
        ] = 48

        tabela_final.loc[(
            (tabela_final["mandantePalpite"].isin(times_final))
            &
            (tabela_final["visitantePalpite"].isin(times_final))
            &              
            (tabela_final["fase"] == "final")
            &
            (tabela_final["participante"] == participante)
            ), "pontos"
        ] = 64

# logica para confirmar o terceiro colocado 
if (gabarito.iat[91,19] > gabarito.iat[91,21]):
    gabarito_terceiro = gabarito.iat[91,18]
elif (gabarito.iat[91,19] < gabarito.iat[91,21]):
    gabarito_terceiro = gabarito.iat[91,22]
elif (gabarito.iat[92,19] > gabarito.iat[92,21]):
    gabarito_terceiro = gabarito.iat[91,18]
elif (gabarito.iat[92,19] < gabarito.iat[92,21]):
    gabarito_terceiro = gabarito.iat[91,22]
else:
    gabarito_terceiro = gabarito.iat[91,18]

# logica para a pontuação do terceiro colocado
for participante, palpite in terceiro_palpites.items():
    if (palpite == gabarito_terceiro):
        tabela_final.loc[(
            (tabela_final["fase"] == "3º lugar")
            &
            (tabela_final["participante"] == participante)
            &
            jogo_ocorreu
            ), "pontos"
        ] = 16

# %%
# gerando ranking
ranking = (tabela_final.groupby("participante")["pontos"].sum()
          .sort_values(ascending=False).reset_index())
ranking.insert(0, "posição", range(1, len(ranking) + 1))

# transportando o dataframe para o excel
with pd.ExcelWriter("Resultado_Bolao_Copa.xlsx", engine="openpyxl") as writer:
    ranking.to_excel(writer, sheet_name="Ranking Geral", index=False)
    tabela_final.to_excel(writer, sheet_name="Dados Detalhados", index=False)

# %%
tabela_final
# %%
times_final
# %%
gabarito.iloc[97,27]
# %%
