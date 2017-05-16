import pandas as pd
import matplotlib.pyplot as plt

lst_cos=[]
lst_adcos=[]
lst_pearson=[]
lst_item=[]
for i in range(1,6):
    str1 = './movielens/'
    df_real = pd.read_table(str1 + 'u%d.test' % i, names=['userid', 'itemid', 'real_rating', 'timestamp'])

    user_based_with_cos_predict=pd.read_csv('user_based_with_sim_cos/u%dpredict.csv'%i,
                                            names=['userid','itemid','predict_rating'])
    user_based_with_cos=pd.merge(user_based_with_cos_predict,df_real,on=['userid','itemid'])
    user_based_with_cos=user_based_with_cos.drop('timestamp',axis=1)
    user_based_with_cos['mae']=abs(user_based_with_cos['predict_rating']-user_based_with_cos['real_rating'])
    lst_cos.append(user_based_with_cos['mae'].mean())


    user_based_with_adcos_predict = pd.read_csv('user_based_with_sim_adcos/u%dpredict.csv' % i,
                                              names=['userid', 'itemid', 'predict_rating'])
    user_based_with_adcos = pd.merge(user_based_with_adcos_predict, df_real, on=['userid', 'itemid'])
    user_based_with_adcos = user_based_with_adcos.drop('timestamp', axis=1)
    user_based_with_adcos['mae'] = abs(user_based_with_adcos['predict_rating'] - user_based_with_adcos['real_rating'])
    lst_adcos.append(user_based_with_adcos['mae'].mean())



    user_based_with_pearson_predict = pd.read_csv('user_based_with_sim_pearson/u%dpredict.csv' % i,
                                              names=['userid', 'itemid', 'predict_rating'])
    user_based_with_pearson = pd.merge(user_based_with_pearson_predict, df_real, on=['userid', 'itemid'])
    user_based_with_pearson = user_based_with_pearson.drop('timestamp', axis=1)
    user_based_with_pearson['mae'] = abs(user_based_with_pearson['predict_rating'] - user_based_with_pearson['real_rating'])
    lst_pearson.append(user_based_with_pearson['mae'].mean())


    item_based_predict = pd.read_csv('item_based/item_based_u%dresult.csv' % i,
                                                  names=['userid', 'itemid', 'predict_rating'])
    item_based_merge = pd.merge(item_based_predict, df_real, on=['userid', 'itemid'])
    item_based_merge = item_based_merge.drop('timestamp', axis=1)
    item_based_merge['mae'] = abs(item_based_merge['predict_rating'] - item_based_merge['real_rating'])
    lst_item.append(item_based_merge['mae'].mean())

plt.plot(range(1,6),lst_cos,label='user_based_with_cos')
plt.plot(range(1,6),lst_adcos,label='user_based_with_adcos')
plt.plot(range(1,6),lst_pearson,label='user_based_with_pearson')
plt.plot(range(1,6),lst_item,label='item_based')
plt.legend(loc='upper right')
plt.grid()
plt.savefig('mae')
plt.show()


