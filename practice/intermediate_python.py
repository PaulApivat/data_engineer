import pandas as pd
import numpy as np

data = {
    's_length': [5.1, 7.0, 6.3],
    's_width': [3.5, 3.2, 3.3],
    'species': ['setosa', 'versicolor', 'virginica']
}

df = pd.DataFrame(data)

print(df)

print(df.iloc[[1], 0])
print(df.loc[[0]])

between = np.logical_and(df['s_width'] > 3.2, df['s_width'] < 3.5)
df[between]