import pandas as pd
import matplotlib.pyplot as plt

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



plt.plot(range(1,6),lst_user_with_cos,label='user_based_with_cos')
plt.plot(range(1,6),lst_user_with_adcos,label='user_based_with_adcos')
plt.plot(range(1,6),lst_user_with_pearson,label='user_based_with_pearson')
#plt.plot(range(1,6),lst_item,label='item_based')
plt.plot(range(1,6),lst_item_with_cos,label='item_based_with_cos')
plt.plot(range(1,6),lst_item_with_adcos,label='item_based_with_adcos')
plt.plot(range(1,6),lst_item_with_pearson,label='item_based_with_pearson')

plt.legend(loc=0)
plt.grid()
plt.xlabel('train set')
plt.ylabel('MAE')
plt.savefig('similarityCompare')
plt.show()


