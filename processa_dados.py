import pandas as pd
import numpy as np
from math import sqrt, pow

def recebe_arquivo(nome_do_arquivo):
    """
    Recebe um arquivo .xlxs de um leitor de placas ELISA e separa seus metadados e os dados amostrais.

    Entrada:
        nome_do_arquivo: Caminho para o arquivo .xlxs.

    Retornos (Tupla):
        metadados (Dataframe): Primeira página da planilha, contém os metadados do equpamento.
        dados_amostrais (Dataframe): Os dados amostrais medidos pelo equipamento.
    """

    planilha = pd.read_excel(nome_do_arquivo, sheet_name=None, header=1)
    sheet_names = list(planilha.keys())
    metadados = planilha[sheet_names[0]]
    dados_amostrais = planilha[sheet_names[1]]

    return metadados, dados_amostrais
    
def remove_celulas_vazias(dataframes):
    """
    Remove as células e colunas vazias de um dataframe com duas pa´ginas.

    Entrada:
        dataframes (Dataframe): Um dataframe proveninente de recebe_arquivo.

    Retorno:
        dataframes_processados (Dataframe): O mesmo dataframe, porém sem células vazias.
    """
    dataframes_processados = []
    for data in dataframes:
        data = data.drop('Unnamed: 0', axis=1)
        data = data.dropna()
        dataframes_processados.append(data)
    return dataframes_processados


def separa_layout(lista_amostras):
    """
    Separa os nomes das amostras e os poços associados a elas.

    Entrada:
        lista_amostras (list): Lista de listas, onde o primeiro elemento de cada sublista 
                               é o nome da amostra e os demais são os poços onde ela está.

    Retorno (Tupla):
        colunas (list): Lista com os nomes das amostras.
        pocos (list): Lista com listas de poços correspondentes a cada amostra.
    """

    colunas = []
    pocos = []
    for dado in lista_amostras:
        colunas.append(dado[0])
        dado.pop(0)
        pocos.append(dado)
    return colunas, pocos

def normaliza_lista(lista_amostras):
    """
    Normaliza listas internas para que todas tenham o mesmo comprimento (preenche com NaN). 
    (Função gerada pelo ChatGPT)

    Entrada:
        lista_amostras (list): Lista de listas de poços, com tamanhos variáveis.

    Retorno:
        normalizado (list): Lista de listas com comprimento uniforme.
    """

    maior_num_de_amostras = max(len(amostras) for amostras in lista_amostras) 
    normalizado = [amostras + [np.nan] * (maior_num_de_amostras - len(amostras)) for amostras in lista_amostras]
    return normalizado

def layout_para_dataframe(layout_provisorio):
    """
    Converte um layout de amostras em formato de lista para um DataFrame estruturado.

    Entrada:
        layout_provisorio (list): Lista de listas contendo nomes das amostras e seus poços.

    Retorno:
        layout_organizado (DataFrame): DataFrame com colunas nomeadas por amostra e valores como poços.
    """

    colunas, pocos = separa_layout(layout_provisorio)
    pocos = normaliza_lista(pocos)
    pocos_transposto = np.transpose(pocos)
    layout_organizado = pd.DataFrame(pocos_transposto, columns=colunas)
    return layout_organizado


def substitui(layout, dados_amostrais={}, abs=2):
    """
    Substitui os nomes dos poços no layout pelos valores de absorbância medidos 
    para um determinado comprimento de onda.

    Entradas:
        layout (DataFrame): Layout contendo os nomes dos poços por amostra.
        dados_amostrais (DataFrame): Dados contendo absorbâncias e poços.
        abs (int): Índice da coluna de absorbância a ser utilizada (deve ser >= 2).

    Retorno:
        layout_copy (DataFrame): Layout com valores de absorbância substituindo os poços.
    """

    abs = str(dados_amostrais.columns.tolist()[abs])

    layout_copy = layout.copy()
    for i in layout_copy:
        for j in layout_copy[i]:
            if j == 'nan':
                continue

            indice = dados_amostrais.index[dados_amostrais['Well'] == j].tolist()[0]

            layout_copy[i] = layout_copy[i].replace(j, (dados_amostrais[abs][indice]))

    return layout_copy

def retira_branco(df, incerteza_equipamento=0):
    """
    Retira o branco das medidas e propaga o erro por essa operação. 
    As incertezas concideradas são o erro do equipamento e a incerteza padrão
    
    Entradas:
        df (Dataframe): Dados amostrais.
        incerteza_equipamento (float): Incerteza do equipamento.

    Retornos (Tupla):
        df_sem_branco: Dataframe contendo os dados amostrais com o branco subtraido.
        incerteza_saida: Incerteza final.
    """

    for coluna in df:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    branco = df['Água'].mean()
    incerteza_branco = df['Água'].sem()
    df_sem_branco = df.drop('Água', axis=1)

    for i in df_sem_branco:
        for j in df_sem_branco[i]:
            if j == 'nan':
                continue
            df_sem_branco[i] = df_sem_branco[i].replace(j, j-branco)

    incerteza_saida = sqrt(pow(incerteza_equipamento, 2) + pow(incerteza_branco, 2))

    return df_sem_branco, incerteza_saida

def separa_namostra(layout, dados_amostrais={}):
    """
    Calcula a média e a incerteza combinada das absorbâncias por amostra e comprimento de onda.

    Entradas:
        layout (DataFrame): DataFrame com amostras e os poços onde estão alocadas.
        dados_amostrais (DataFrame): Dados brutos contendo absorbâncias em diferentes comprimentos de onda.

    Retorno:
        df (DataFrame): Tabela final contendo a média e a incerteza da absorbância 
        para cada amostra e comprimento de onda.
    """

    colunas = layout.columns.tolist()
    colunas.pop(0)
    indice = [i for i in dados_amostrais if i.startswith('A')]
    
    lista_dados = []
    dados = []
    for i in range(len(indice)):

        dataframe_interno, incerteza = retira_branco(substitui(layout, dados_amostrais, abs=i+2))
        print(i)
        print('\n dataframe', dataframe_interno, '\n')    
        
        for coluna in dataframe_interno:
            dataframe_interno[coluna] = pd.to_numeric(dataframe_interno[coluna], errors='coerce')

        for coluna in dataframe_interno:
            media = dataframe_interno[coluna].mean()
            sigma = dataframe_interno[coluna].sem()
            incerteza_saida = sqrt(pow(sigma, 2) + pow(incerteza, 2))
            dados.append((media, incerteza_saida))

        lista_dados.append(dados)
        dados = []
        
    df = pd.DataFrame(lista_dados, index=indice, columns=colunas)
    print(df)
    
    return df
