import pandas as pd

df = pd.DataFrame({'Name': ['John', 'Emma', 'Peter', 'Maria'],
                   'Age' : [ 25, 30, 20, 35],
                   'Gender': ['Male', 'Female', 'Male', 'Female']})

print(df)




grouped_df = df.groupby('Age').mean()


print(grouped_df)