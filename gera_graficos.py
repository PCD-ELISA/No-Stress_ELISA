import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

sns.set_theme(style="darkgrid")
df = sns.load_dataset("penguins")

g = sns.displot(
    df, x="flipper_length_mm", col="species", row="sex",
    binwidth=3, height=3, facet_kws=dict(margin_titles=True),
)

g.savefig("penguins_flipper_length.png")  
