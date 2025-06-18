import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

def plot_absorbancia(dados_df, tipo_grafico="barra"):
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

    print(dados)
    df_plot = pd.DataFrame(dados)
    print(df_plot)

    p = so.Plot(df_plot, x="Amostra", y="Média", color="Absorbância")

    if tipo_grafico == "barra":
        p = p.add(so.Bar(), so.Dodge())
    elif tipo_grafico == "linha":
        p = p.add(so.Line(marker="o"))
    else:
        raise ValueError("tipo_grafico deve ser 'barra' ou 'linha'.")

    p = p.label(x="Amostras", y="Absorbância (u.a.)")
    p.show()

df_exemplo = pd.DataFrame({
    "Amostra1": [(0.52, 0.03), (0.68, 0.05), (0.75, 0.04)],
    "Amostra2": [(0.49, 0.02), (0.65, 0.06), (0.78, 0.05)],
    "Amostra3": [(0.55, 0.04), (0.63, 0.05), (0.80, 0.03)],
}, index=["Abs1", "Abs2", "Abs3"])

print(df_exemplo)

plot_absorbancia(df_exemplo)