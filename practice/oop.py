
import numpy as np
import pandas as pd
# complete code to return output

class MaxVal:
    def __init__(self, array_1):
        self.A = array_1
    def MaximumValue(self):
        """Returns the maximum
        value of an array."""
        return max(self.A)

op_obj = MaxVal(np.array([8, 9, 8]))
print(op_obj.MaximumValue())


# create dataframe, write to csv
# then read from csv, back to dataframe

datacamp_data = {
    'chapter': [1, 2, 3],
    'course': ["Data Science", "Data Visualization", "Databases"],
    'technology': ['Python', 'R', 'SQL']
}
datacamp_df = pd.DataFrame(datacamp_data)
index = pd.Index(['P', 'R', 'S'])
datacamp_df = datacamp_df.set_index([index])

# read to csv
#datacamp_df.to_csv("datacamp.csv")
#print("Read datacamp df to csv.-------")


class DataShell:
    def __init__(self, inputFile):
        self.file = inputFile
    def df_from_csv(self):
        self.df = pd.read_csv(self.file)
        return self.df

data_shell = DataShell('datacamp.csv')
data_shell.df_from_csv().head

