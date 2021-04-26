import os
import pandas as pd

from matplotlib import pyplot as plt

pd.set_option('display.max_columns', None)

print(*os.listdir("opinions"), sep="\n")


productId = input("Podaj kod produktu: ")

opinions = pd.read_json(f"./opinions/{productId}.json")

opinions.stars = opinions.stars.apply(lambda x: float(x.split("/")[0].replace(",", ".")))
average_score = opinions.stars.mean()
opinions.rcmd = opinions.rcmd.apply(lambda x: "Nie mam zdania" if x is None else x)



recommendations = opinions.rcmd.value_counts(dropna = False)
recommendations.plot.pie(qlabel="")
plt.show()
