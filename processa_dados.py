import pandas as pd

print("Aqui a gente processa os dados!!!")
print("WIP!!!")



def retira_branco(df, incerteza_equipamento=0):
    '''Retira o branco das medidas e propaga o eror por essa operação
    
    Retorna o data frame sem o branco e retorna a incerteza associada a cada medida
    '''

    from math import sqrt, pow

    # Defini uma incerteza de equipamento
    branco = df['Água'].mean()
    incerteza_branco = df['Água'].sem() # Importante
    df_sem_branco = df.drop('Água', axis=1)
    df_sem_branco -= branco # Importante
    # Propagar o erro
    incerteza_saida = sqrt(pow(incerteza_equipamento) + pow(incerteza_branco))

    return df_sem_branco, incerteza_saida

df_total = pd.read_excel('Teste.xlsx', 'Results')
print(df_total)
