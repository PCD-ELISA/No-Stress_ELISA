import pandas as pd

def recebe_arquivo(nome_do_arquivo):
    # TODO:
    # Receber o arquivo da interface
    # Botar nomes mais significativos nas variáveis

    ''' 
    Essa função recebe um arquivo xlsx e transforma ele em um dataframe do Pandas.
    Por simplicidade, nesse protótipo inicial receberemos ele diretamente, sem intermédio
    da interface
    '''

    planilha = pd.read_excel(nome_do_arquivo, sheet_name=None)
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
    '''

    # Inicialmente deletaremos a primeira coluna, pois assumimos que ela sempre será vazia (toda NaN),
    # porém devemos tratar melhor depois para outros casos
    dataframes_processados = []
    for data in dataframes:
        data = data.drop('Unnamed: 0', axis=1)
        dataframes_processados.append(data)
    return dataframes_processados

def separa_amostras(dados_amostrais, layout):
    # TODO:
    # Receber o arquivo da interface
    print("Oi!")

print(remove_celulas_vazias(recebe_arquivo("Teste.xlsx")))

#Vou supor essa arquitetura para o layout:

layout = [["Água", "A1", "B1"], ["HCl", "A2", "B2"]]
layout_pandas = pd.DataFrame(layout)
print(layout_pandas)
