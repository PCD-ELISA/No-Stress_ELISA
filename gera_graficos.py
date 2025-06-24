import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so
import io
from PIL import Image

def plot_absorbancia(dados_df, tipo_grafico="barra"):
    """
    Gera um gráfico de absorbância para diferentes amostras e comprimentos de onda.

    Parâmetros:
        dados_df (DataFrame): DataFrame com tuplas (média, incerteza) como valores e 
                              comprimentos de onda como índices.

        tipo_grafico (str): Tipo de gráfico a ser gerado. Pode ser de barra ou linha.

    Retorno:
        PIL.Image: Imagem gerada do gráfico.
    """

    dados = []
    for absorbancia in dados_df.index:
        for amostra in dados_df.columns:
            media, incerteza = dados_df.loc[absorbancia, amostra]
            dados.append({
                "Amostra": amostra,
                "Absorbância": absorbancia,
                "Média": media,
                "Incerteza": incerteza
            })

    df_plot = pd.DataFrame(dados)
    df_plot["Absorbância"] = df_plot["Absorbância"].astype(str)

    plotagem = so.Plot(df_plot, x="Amostra", y="Média", color="Absorbância")

    plt.figure(figsize=(10, 6))
    
    if tipo_grafico == "barra":
        sns.barplot(data=df_plot, x="Amostra", y="Média", hue="Absorbância")
    elif tipo_grafico == "linha":
        sns.lineplot(data=df_plot, x="Amostra", y="Média", hue="Absorbância", marker="o")
    
    plt.xlabel("Amostras")
    plt.ylabel("Absorbância (u.a.)")
    plt.legend(title="Comprimento de onda", bbox_to_anchor=(1.05, 0.5), loc='center left')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close()
    return Image.open(buffer)
