from math import sqrt
from load_movielens import loadMovieLensTest


def sim_cos(train,item1,item2):
    #common_user用来找同时评价过这两个商品的共同用户。
    common_user=[]
    for (user, items) in train.items():
        if item1 in items and item2 in items:
            common_user.append(user)
    if len(common_user)==0:
        return 0
    summulti = sum([(train[user][item1] * train[user][item2]) for user in common_user])
    sq1 = sqrt(sum([pow(train[user][item1], 2) for user in common_user]))
    sq2 = sqrt(sum([pow(train[user][item1], 2) for user in common_user]))
    sq = sq1 * sq2
    if sq==0:
        return 0
    else:
        return summulti/sq


def sim_adcos(train,item1,item2):
    common_user=[]
    for (user, items) in train.items():
        if item1 in items and item2 in items:
            common_user.append(user)
    if len(common_user)==0:
        return 0
    #分子
    numerator = 0
    #分母
    denominator=0
    for user in common_user:
        sum1=sum([train[user][item] for item in train[user]])
        n1=len(train[user])
        avg1=sum1/n1
        numerator+=(train[user][item1]-avg1)*(train[user][item2]-avg1)
        denominator+=sqrt(pow((train[user][item1]-avg1),2))*sqrt(pow((train[user][item2]-avg1),2))
    if denominator==0:
        return 0
    return numerator/denominator


def sim_pearson(train,item1,item2):
    common_user = []
    for (user, items) in train.items():
        if item1 in items and item2 in items:
            common_user.append(user)
    if len(common_user) == 0:
        return 0

    #存放item1的所有评分值
    all_scores_for_item1=[]
    # 存放item1的所有评分值
    all_scores_for_item2 = []

    for (user, items) in train.items():
        if item1 in items:
            all_scores_for_item1.append(train[user][item1])
    avg_item1=sum(all_scores_for_item1)/len(all_scores_for_item1)

    for (user, items) in train.items():
        if item2 in items:
            all_scores_for_item2.append(train[user][item1])
    avg_item2=sum(all_scores_for_item2)/len(all_scores_for_item2)

    numerator = sum([(train[user][item1] - avg_item1) * (train[user][item2] - avg_item2) for user in common_user])
    denominator=sqrt(sum([pow((train[user][item1]-avg_item1),2) for user in common_user]))*sqrt(sum([pow((train[user][item2]-avg_item2),2) for user in common_user]))
    if denominator==0:
        return 0
    return numerator/denominator




'''
testSet=loadMovieLensTest('u1.test')
for presentUserid in testSet:
    for presentItem in testSet[presentUserid]:
        print(sim_cos(testSet,presentUserid,presentItem))'''