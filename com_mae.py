import pandas as pd
import matplotlib.pyplot as plt

lst=[]
for i in range(1,6):
    str1 = './movielens/'
    df_real = pd.read_table(str1 + 'u%d.test' % i, names=['userid', 'itemid', 'real_rating', 'timestamp'])

    user_based_with_cos_predict=pd.read_csv('user_based_with_sim_cos/u%dpredict.csv'%i,names=['userid','itemid','predict_rating'])

    mae_of_user_based_with_cos=pd.merge(user_based_with_cos_predict,df_real,on=['userid','itemid'])
    mae_of_user_based_with_cos=mae_of_user_based_with_cos.drop('timestamp',axis=1)
    mae_of_user_based_with_cos['mae']=abs(mae_of_user_based_with_cos['predict_rating']-mae_of_user_based_with_cos['real_rating'])

    print(mae_of_user_based_with_cos.head())
    print(mae_of_user_based_with_cos['mae'].mean())
    lst.append(mae_of_user_based_with_cos['mae'].mean())
    
plt.plot(range(1,6),lst)
plt.show()

