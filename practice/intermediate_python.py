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

# Complete the code to return the output

practice = {'python': 100, "r": 30, "sql": 10}

for key, value in practice.items():
    print(key + " practice has " + str(value) + " items")


# Select code to return the out

datacamp_data = {
    'chapter': [1, 2, 3],
    'course': ["Data Science", "Data Visualization", "Databases"],
    'technology': ['Python', 'R', 'SQL']
}

datacamp_df = pd.DataFrame(datacamp_data)
index = pd.Index(['P', 'R', 'S'])
datacamp_df = datacamp_df.set_index([index])

for lab, row in datacamp_df.iterrows():
    print(lab)
    print(row)

# ----- What is the out put of this Numpy Array code 

x = np.array([9, 5])
y = np.array([16, 12])

print(np.logical_or(x < 5, y > 15))

# ------ Complete code output 

numpy1 = np.array([17.2, 20.2, 8.25, 9.50])
numpy2 = np.array([13.0, 24.0, 8.25, 9.0])

# list slicing
print(numpy1[::len(numpy1)-1])


# ----- What is the output?
datacamp_data = {
    'chapter': [1, 2, 3],
    'course': ["Data Science", "Data Visualization", "Databases"],
    'technology': ['Python', 'R', 'SQL']
}

datacamp_df = pd.DataFrame(datacamp_data)
index = pd.Index(['P', 'R', 'S'])
datacamp_df = datacamp_df.set_index([index])

print(datacamp_df.iloc[[1,2], [2]])