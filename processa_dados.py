import pandas as pd
import numpy as np
from math import sqrt, pow

def retira_branco(df, incerteza_equipamento=0):
    '''Retira o branco das medidas e propaga o erro por essa operação. O erro é a raiz quadrada
    da soma dos quadrados das incertezas.
    As incertezas concideradas sõa o erro do equipamento e a incerteza padrão
    
    Retorna o dataframe sem o branco e retorna a incerteza associada a cada medida
    '''

    # Define uma incerteza de equipamento
    branco = df['Água'].mean()
    incerteza_branco = df['Água'].sem()
    df_sem_branco = df.drop('Água', axis=1)
    for i in df_sem_branco:
        for j in df_sem_branco[i]:
            if j == 'nan':
                continue
            df_sem_branco[i] = df_sem_branco[i].replace(j, j-branco)
    # df_sem_branco -= branco 
    # Propagar o erro
    incerteza_saida = sqrt(pow(incerteza_equipamento, 2) + pow(incerteza_branco, 2))

    return df_sem_branco, incerteza_saida

def recebe_arquivo(nome_do_arquivo):
    # TODO:
    # Receber o arquivo da interface
    # Botar nomes mais significativos nas variáveis

    ''' 
    Essa função recebe um arquivo xlsx e transforma ele em um dataframe do Pandas.
    Por simplicidade, nesse protótipo inicial receberemos ele diretamente, sem intermédio
    da interface
    '''

    planilha = pd.read_excel(nome_do_arquivo, sheet_name=None, header=1)
    sheet_names = list(planilha.keys())
    metadados = planilha[sheet_names[0]]
    dados_amostrais = planilha[sheet_names[1]]

    return metadados, dados_amostrais
    
def remove_celulas_vazias(dataframes):
    ''' 
    Essa função recebe uma tupla de dataframes e remove celulas vazias

    Retorna uma tupla de dataframes com metadados e dados amostrais
    '''
    dataframes_processados = []
    for data in dataframes:
        data = data.drop('Unnamed: 0', axis=1)
        data = data.dropna()
        dataframes_processados.append(data)
    return dataframes_processados


def separa_layout(lista_amostras):
    colunas = []
    pocos = []
    for dado in lista_amostras:
        colunas.append(dado[0])
        dado.pop(0)
        pocos.append(dado)
    return colunas, pocos

def normaliza_lista(lista_amostras):
    # Gerado pelo ChatGPT
    maior_num_de_amostras = max(len(amostras) for amostras in lista_amostras) 
    normalizado = [amostras + [np.nan] * (maior_num_de_amostras - len(amostras)) for amostras in lista_amostras]
    return normalizado

def layout_para_dataframe(layout_provisorio):
    colunas, pocos = separa_layout(layout_provisorio)
    pocos = normaliza_lista(pocos)
    pocos_transposto = np.transpose(pocos)
    layout_organizado = pd.DataFrame(pocos_transposto, columns=colunas)
    return layout_organizado


def substitui(layout, dados_amostrais={}, abs=2):
    '''Separa em um dataframe (layout) apenas as absorbâncias de poços que contém uma determinada amostra
    
    Faz isso substituindo os poços (A1, A2, ...,) pelas absorbâncias medidas nesses poços.
    O parâmetro "abs" indica em qual comprimento de onda a medida de absorbancia foi realizada.
    "abs" >= 2

    Essa função lê apenas um comprimento de onda por vez
    '''

    abs = str(dados_amostrais.columns.tolist()[abs])
    #layout é uma tabela com colunas de composto químico e poços em que o composto está
    layout_copy = layout.copy()
    for i in layout_copy:
        for j in layout_copy[i]:
            if j == 'nan':
                continue
            # Encontra o índice na tabela de dados amostrais correspondente ao poço em que há uma amostra
            indice = dados_amostrais.index[dados_amostrais['Well'] == j].tolist()[0]
            # Substitui na cópia do layout o valor das absorbâncias associadas aos poços
            layout_copy[i] = layout_copy[i].replace(j, (dados_amostrais[abs][indice]))

    return layout_copy

def separa_namostra(layout, dados_amostrais={}):
    # Pega as colunas e os índices para formar uma tabela com os comprimentos de onda
    colunas = layout.columns.tolist()
    # Retira a coluna de Água pois essa sumirá na função retira branco
    colunas.pop(0)
    indice = [i for i in dados_amostrais if i.startswith('A')]
    
    # Anexar o valor de absorbância à coordenada Amostra; Comprimento (média, incerteza)
    lista_dados = []
    dados = []
    for i in range(len(indice)):

        dataframe_interno, incerteza = retira_branco(substitui(layout, dados_amostrais, abs=i+2))
        print(i)
        print('\n dataframe', dataframe_interno, '\n')    
        
        # Faz o dataframe ficar "numérico"
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


    #     for coluna in dataframe_interno:

    #         # Calcula a média; Pandas não queria fazer o serviço
    #         soma = 0
    #         contador = 0
    #         for valor in dataframe_interno[coluna]:
    #             if valor == 'nan':
    #                 continue
    #             soma += valor
    #             contador += 1
    #         media = soma / contador

    #         dados.append((media, incerteza))
    #     lista_dados.append(dados)
    #     dados = []

    # df = pd.DataFrame(lista_dados, index=indice, columns=colunas)
    # print(df)
    
    # return df

layout_caso_teste = [["Água", "A10", "A11", "A12", "B10", "B11", "B12", "C10", "C11", "C12"],
                    ["Controle_1_ph2", "A1", "B1", "C1"],
                    ["Controle_1_ph8", "A5", "B5", "C5"],
                    ["Controle_2_ph2", "F1", "G1", "H1"],
                    ["Controle_2_ph8", "F5", "G5", "H5"],
                    ["CaCl2_1_ph2", "A2", "B2", "C2"],
                    ["CaCl2_1_ph8", "A6", "B6", "C6"],
                    ["CaCl2_2_ph2", "F2", "G2", "H2"],
                    ["CaCl2_2_ph8", "F6", "G6", "H6"],
                    ["FeSO4_1_ph2", "A3", "B3", "C3"],
                    ["FeSO4_1_ph8", "A7", "B7", "C7"],
                    ["FeSO4_2_ph2", "F3", "G3", "H3"],
                    ["FeSO4_2_ph8", "F7", "G7", "H7"]]


layout = layout_para_dataframe(layout_caso_teste)
dados_amostrais = remove_celulas_vazias(recebe_arquivo('Teste.xlsx'))[1]
print('Layout\n', layout)
print('Dados amostrais\n', dados_amostrais)
print('----------##########----------##########----------##########')

separa_namostra(layout, dados_amostrais)
