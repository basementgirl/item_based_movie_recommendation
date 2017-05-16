import pandas as pd
import matplotlib.pyplot as plt

lst=[]
for i in range(1,6):
    df_predict=pd.read_csv('u%dresult.csv'%i,names=['userid','itemid','predict_rating'])

    str1 = './movielens/'
    df_real=pd.read_table(str1+'u%d.test'%i,names=['userid','itemid','real_rating','timestamp'])
    
    df=pd.merge(df_predict,df_real,on=['userid','itemid'])
    df=df.drop('timestamp',axis=1)
    
    df['mae']=abs(df['predict_rating']-df['real_rating'])
    print(df.head())
    
    print(df['mae'].mean())
    lst.append(df['mae'].mean())
    
plt.plot(range(1,6),lst)
plt.show()

