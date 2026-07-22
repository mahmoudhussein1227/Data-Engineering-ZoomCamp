import sys as s
import pandas as pd 

month = s.argv[1]

print(s.argv)

print(f"hello in pipline and the month parameter is {month}")

df = pd.DataFrame({"day" : [1,2,3] 
                   ,"no_passangers" : [5,7,8]})







df['Month'] = month








print(df.head())

