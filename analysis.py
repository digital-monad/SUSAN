import numpy as np
import pandas as pd
import json

# This script analyses the data to provide useful figures for normalisation

# Path to database. Use RAW_recipes for now
path = "/Users/Elijah/Sus-Recipes/SR/RAW_recipes.csv"


def reject_outliers(data, m=0.05):
    outlier_matr = np.abs(np.transpose(data) - np.mean(data, 0)[:, None]) - m * np.std(data, 0)[:, None]
    return np.where(outlier_matr < 0)


def clean(nutr):
    nutrs = np.array(list(map(json.loads, nutr)))
    rows, cols = reject_outliers(nutrs)
    inds = np.unique(cols)
    print("Size after outliers: "+str(inds.size))
    return inds


def filter_data():
    df = pd.read_csv(path)
    rec_inds = []
    nutr = df.get("nutrition")
    inds = clean(nutr)
    for i in range(len(nutr)):  # 129,000
        vals = json.loads(nutr.iloc[i])
        cal = vals[0]
        fat = vals[1]
        sug = vals[2]
        sod = vals[3]
        pro = vals[4]
        sat = vals[5]
        carbs = vals[6]
        if cal < 1000 and fat < 100 and sug < 100 and sod < 100 and pro < 100 and sat < 100 and carbs < 100:
            rec_inds.append(i)
    rec_inds = np.array(rec_inds)

    # result = [df.iloc[i] for i in rec_inds]

    """res_df = pd.DataFrame(result)
    nutr2 = res_df.get("nutrition")
    nutr2 = np.array(list(map(json.loads, nutr2)))
    print(max(nutr2[:,0]))"""
    # plt.plot(range(len(nutr2)), nutr2[:,0])
    # plt.show()
    # res_df = pd.DataFrame(recs)
    # res_df.to_csv("/Users/Elijah/Sus-Recipes/SR/database.csv", encoding='utf-8')
    return len(rec_inds)


print("Size before filtering: "+str(231637))
print("Size after filtering: "+str(filter_data()))
