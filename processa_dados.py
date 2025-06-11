import pandas as pd
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
    # TODO:
    # Remover celulas NaN individuais 
    # e manter a estrutura de maneira que seja fácil iterar e manipular os dados

    ''' 
    Essa função recebe uma tupla de dataframes e remove celulas vazias

    Retorna uma tupla de dataframes com metadados e dados amostrais
    '''

    # Inicialmente deletaremos a primeira coluna, pois assumimos que ela sempre será vazia (toda NaN),
    # porém devemos tratar melhor depois para outros casos
    dataframes_processados = []
    for data in dataframes:
        data = data.drop('Unnamed: 0', axis=1)
        dataframes_processados.append(data)
    return dataframes_processados


def separa_amostras_jjj(layout, dados_amostrais={}):
    # TODO:
    # Receber o arquivo da interface
    dados_organizados = []
    colunas = []
    for dado in layout:
        colunas.append(dado[0])
    print(colunas)
    return dados_organizados


def separa_amostras2(layout, dados_amostrais={}):
    '''Separa em um dataframe apenas as absorbâncias de poços que contém uma determinada amostra'''

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





#Vou supor essa arquitetura para o layout:

layout = [["Água", "A1", "B1"], ["HCl", "A2", "B2"]]
df = pd.read_excel('layout.xlsx')
print(df)

# print(df.where(df == 'A1').stack().index.tolist())
a = separa_amostras2(df, remove_celulas_vazias(recebe_arquivo('Teste.xlsx'))[1])
print(a)
