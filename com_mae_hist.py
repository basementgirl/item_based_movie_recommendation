import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


lst_user_with_cos=[]
lst_user_with_adcos=[]
lst_user_with_pearson=[]
lst_item=[]
lst_item_with_cos=[]
lst_item_with_adcos=[]
lst_item_with_pearson=[]


for i in range(1,6):
    str1 = './movielens/'
    df_real = pd.read_table(str1 + 'u%d.test' % i, names=['userid', 'itemid', 'real_rating', 'timestamp'])

    user_based_with_cos_predict=pd.read_csv('user_based_with_sim_cos/u%dpredict.csv'%i,
                                            names=['userid','itemid','predict_rating'])
    user_based_with_cos=pd.merge(user_based_with_cos_predict,df_real,on=['userid','itemid'])
    user_based_with_cos=user_based_with_cos.drop('timestamp',axis=1)
    user_based_with_cos['mae']=abs(user_based_with_cos['predict_rating']-user_based_with_cos['real_rating'])
    lst_user_with_cos.append(user_based_with_cos['mae'].mean())


    user_based_with_adcos_predict = pd.read_csv('user_based_with_sim_adcos/u%dpredict.csv' % i,
                                              names=['userid', 'itemid', 'predict_rating'])
    user_based_with_adcos = pd.merge(user_based_with_adcos_predict, df_real, on=['userid', 'itemid'])
    user_based_with_adcos = user_based_with_adcos.drop('timestamp', axis=1)
    user_based_with_adcos['mae'] = abs(user_based_with_adcos['predict_rating'] - user_based_with_adcos['real_rating'])
    lst_user_with_adcos.append(user_based_with_adcos['mae'].mean())



    user_based_with_pearson_predict = pd.read_csv('user_based_with_sim_pearson/u%dpredict.csv' % i,
                                              names=['userid', 'itemid', 'predict_rating'])
    user_based_with_pearson = pd.merge(user_based_with_pearson_predict, df_real, on=['userid', 'itemid'])
    user_based_with_pearson = user_based_with_pearson.drop('timestamp', axis=1)
    user_based_with_pearson['mae'] = abs(user_based_with_pearson['predict_rating'] - user_based_with_pearson['real_rating'])
    lst_user_with_pearson.append(user_based_with_pearson['mae'].mean())

    '''
    item_based_predict = pd.read_csv('item_based/item_based_u%dresult.csv' % i,
                                                  names=['userid', 'itemid', 'predict_rating'])
    item_based_merge = pd.merge(item_based_predict, df_real, on=['userid', 'itemid'])
    item_based_merge = item_based_merge.drop('timestamp', axis=1)
    item_based_merge['mae'] = abs(item_based_merge['predict_rating'] - item_based_merge['real_rating'])
    lst_item.append(item_based_merge['mae'].mean())'''


    item_based_with_cos_predict = pd.read_csv('item_based_with_sim_cos/u%dpredict.csv' % i,
                                     names=['userid', 'itemid', 'predict_rating'])
    item_based_with_cos = pd.merge(item_based_with_cos_predict, df_real, on=['userid', 'itemid'])
    item_based_with_cos = item_based_with_cos.drop('timestamp', axis=1)
    item_based_with_cos['mae'] = abs(item_based_with_cos['predict_rating'] - item_based_with_cos['real_rating'])
    lst_item_with_cos.append(item_based_with_cos['mae'].mean())


    item_based_with_adcos_predict = pd.read_csv('item_based_with_sim_adcos/u%dpredict.csv' % i,
                                     names=['userid', 'itemid', 'predict_rating'])
    item_based_with_adcos = pd.merge(item_based_with_adcos_predict, df_real, on=['userid', 'itemid'])
    item_based_with_adcos = item_based_with_adcos.drop('timestamp', axis=1)
    item_based_with_adcos['mae'] = abs(item_based_with_adcos['predict_rating'] - item_based_with_adcos['real_rating'])
    lst_item_with_adcos.append(item_based_with_adcos['mae'].mean())


    item_based_with_pearson_predict = pd.read_csv('item_based_with_sim_pearson/u%dpredict.csv' % i,
                                     names=['userid', 'itemid', 'predict_rating'])
    item_based_with_pearson = pd.merge(item_based_with_pearson_predict, df_real, on=['userid', 'itemid'])
    item_based_with_pearson = item_based_with_pearson.drop('timestamp', axis=1)
    item_based_with_pearson['mae'] = abs(item_based_with_pearson['predict_rating'] - item_based_with_pearson['real_rating'])
    lst_item_with_pearson.append(item_based_with_pearson['mae'].mean())


cos_com=[sum(lst_user_with_cos)/len(lst_user_with_cos),sum(lst_item_with_cos)/len(lst_item_with_cos)]
adcos_com=[sum(lst_user_with_adcos)/len(lst_user_with_adcos),sum(lst_item_with_adcos)/len(lst_item_with_adcos)]
pearson_com=[sum(lst_user_with_pearson)/len(lst_user_with_pearson),sum(lst_item_with_pearson)/len(lst_item_with_pearson)]


nda=[cos_com,adcos_com,pearson_com]
nda=np.array(nda)
df=pd.DataFrame(nda,columns=['user_based','item_based'],index=['cos','adcos','pearson'])
print(df)

df.plot(kind='bar')


plt.legend(loc=0)
plt.grid()

plt.ylim(0.7,0.78)
plt.xlabel('Similarity')
plt.ylabel('MAE')
plt.savefig('userItemCompare')
plt.show()


