import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from PIL import Image

def plot_absorbancia(dados_df, tipo_grafico="barra"):
    """
    Gera um gráfico de absorbância para diferentes amostras e comprimentos de onda.

    Parâmetros:
        dados_df (DataFrame): DataFrame com tuplas (média, incerteza) como valores e 
                              comprimentos de onda como índices.

        tipo_grafico (str): Tipo de gráfico a ser gerado. Pode ser "barra" ou "linha".

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

    sns.set_theme(style="whitegrid")
    palette = sns.color_palette("viridis")

    plt.figure(figsize=(10, 6))

    if tipo_grafico == "barra":
        ax = sns.barplot(
            data=df_plot,
            x="Amostra",
            y="Média",
            hue="Absorbância",
            palette=palette,
            edgecolor="black",
            linewidth=1.2,
            errwidth=1.5,
            capsize=0.1,
            errorbar=None
        )

    elif tipo_grafico == "linha":
        ax = sns.lineplot(
            data=df_plot,
            x="Amostra",
            y="Média",
            hue="Absorbância",
            palette=palette,
            marker="o"
        )

    plt.xlabel("Amostras", fontsize=14)
    plt.ylabel("Absorbância (u.a.)", fontsize=14)
    plt.title("Gráfico de Absorbância", fontsize=16, weight='bold', pad=15)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(title="Comprimento de onda", bbox_to_anchor=(1.05, 0.5), loc='center left')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
    buffer.seek(0)
    plt.close()
    return Image.open(buffer)
