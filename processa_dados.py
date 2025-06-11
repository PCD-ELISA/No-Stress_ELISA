import pandas as pd
import numpy as np
from math import sqrt, pow

def retira_branco(df, incerteza_equipamento=0):
    '''Retira o branco das medidas e propaga o erro por essa operação
    
    Retorna o dataframe sem o branco e retorna a incerteza associada a cada medida
    '''

    # Define uma incerteza de equipamento
    branco = df['Água'].mean()
    incerteza_branco = df['Água'].sem() 
    df_sem_branco = df.drop('Água', axis=1)
    df_sem_branco -= branco 
    # Propagar o erro
    incerteza_saida = sqrt(pow(incerteza_equipamento) + pow(incerteza_branco))

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

def layout_para_dataframe(layout_provisorio):
    colunas, pocos = separa_layout(layout_provisorio)
    pocos = normaliza_lista(pocos)
    pocos_transposto = np.transpose(pocos)
    dados_organizados = pd.DataFrame(pocos_transposto, columns=colunas)
    return dados_organizados

def separa_amostras2(layout, dados_amostrais={}):
    '''Separa em um dataframe (layout) apenas as absorbâncias de poços que contém uma determinada amostra'''

    abs = str(dados_amostrais.columns.tolist()[2])
    #layout é uma tabela com colunas de composto químico e poços em que o composto está
    layout_copy = layout.copy()
    for i in layout_copy:
        for j in layout_copy[i]:
            # Encontra o índice na tabela de dados amostrais correspondente ao poço em que há uma amostra
            indice = dados_amostrais.index[dados_amostrais['Well'] == j].tolist()[0]
            # Substitui na cópia do layout o valor das absorbâncias associadas aos poços
            layout_copy[i] = layout_copy[i].replace(j, (dados_amostrais[abs][indice]))

    return layout_copy

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


layout = pd.read_excel('layout.xlsx')

layout = [["Água", "A1", "B1"], ["HCl", "A2", "B2"]]

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


print(layout_para_dataframe(layout_caso_teste))
