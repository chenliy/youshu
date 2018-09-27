import pandas as pd
import numpy as np

date = pd.date_range(start='20180601',end='20180701',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=date,columns=list('ABCD'))
print(df)

print(df.iloc[1,2])
print(df.mean(1))
print(df.mean(1)[1])

print(len(df))
print(len(df.T))

for i in range(len(df)):
    a = df.mean(1)[i]
    print(a)
    for j in range(len(df.T)):
        print(df.iloc[i,j])
        if df.iloc[i,j] < a :
            print('第{}行，第{}列，比第{}的均值小'.format(i,j,i))
        elif df.iloc[i,j] == a:
            print('第{}行，第{}列，与第{}的均值相等'.format(i, j, i))
        else:
            print('第{}行，第{}列，比第{}的均值大'.format(i, j, i))
