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

    plotagem = so.Plot(df_plot, x="Amostra", y="Média", color="Amostra")

    if tipo_grafico == "barra":
        plotagem = plotagem.add(so.Bar(), so.Dodge())
    elif tipo_grafico == "linha":
        plotagem = plotagem.add(so.Line(marker="o"))
    else:
        raise ValueError("tipo_grafico deve ser 'barra' ou 'linha'.")

    plotagem = plotagem.label(x="Amostras", y="Absorbância (u.a.)")

    buffer = io.BytesIO()
    plotagem.save(buffer, format="png")
    buffer.seek(0)
    return Image.open(buffer)
