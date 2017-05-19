from math import sqrt

#定义余弦相似度函数
def sim_cos(train,item1,item2):
    #common_user用来找同时评价过这两个商品的共同用户。
    common_user=[]
    for (user, items) in train.items():
        if item1 in items and item2 in items:
            common_user.append(user)
    if len(common_user)==0:
        return 0.3

    #numerator代表分子。denominator代表分母。
    numerator = sum([(train[user][item1] * train[user][item2]) for user in common_user])
    sq1 = sqrt(sum([pow(train[user][item1], 2) for user in common_user]))
    sq2 = sqrt(sum([pow(train[user][item2], 2) for user in common_user]))
    denominator = sq1 * sq2

    return numerator/denominator


#定义修正余弦相似度函数
def sim_adcos(train,item1,item2):
    common_user=[]
    for (user, items) in train.items():
        if item1 in items and item2 in items:
            common_user.append(user)
    if len(common_user)==0:
        return 0.3

    # numerator代表分子。denominator代表分母。
    numerator = 0
    #item1_sum代表sq1的和。
    item1_sum=0
    item2_sum=0
    for user in common_user:
        sum1=sum([train[user][item] for item in train[user]])
        n1=len(train[user])
        avg1=sum1/n1
        #avg1代表用户的平均评分。
        numerator+=(train[user][item1]-avg1)*(train[user][item2]-avg1)
        #sq1代表共同用户集中的用户u对item1的评分减去u的平均评分。然后再平方。
        sq1=pow((train[user][item1]-avg1),2)
        item1_sum+=sq1
        sq2=pow((train[user][item2]-avg1),2)
        item2_sum += sq2
    denominator=sqrt(item1_sum)*sqrt(item2_sum)
    if denominator==0:#这种情况之前没想到。意思是假如共同用户只评价过这一个。则其均值和该评价相同。则出现0.
        return 0.3
    return numerator/denominator


def sim_pearson(train,item1,item2):
    common_user = []
    for (user, items) in train.items():
        if item1 in items and item2 in items:
            common_user.append(user)

    #没有共同用户的i情况。则默认相似度为0.3。
    if len(common_user) == 0:
        return 0.3

    #存放item1的所有评分值
    all_scores_for_item1=[]
    # 存放item2的所有评分值
    all_scores_for_item2 = []

    for (user, items) in train.items():
        if item1 in items:
            all_scores_for_item1.append(train[user][item1])

    #此书既然有了具有共同评价过这两个商品的用户，则说明这个用户一定被评价过。不是冷启动项目。所以len(all_scores_for_item1)>0。
    avg_item1=sum(all_scores_for_item1)/len(all_scores_for_item1)

    for (user, items) in train.items():
        if item2 in items:
            all_scores_for_item2.append(train[user][item2])
    avg_item2=sum(all_scores_for_item2)/len(all_scores_for_item2)

    numerator = sum([(train[user][item1] - avg_item1) * (train[user][item2] - avg_item2) for user in common_user])
    denominator=sqrt(sum([pow((train[user][item1]-avg_item1),2) for user in common_user]))*sqrt(sum([pow((train[user][item2]-avg_item2),2) for user in common_user]))

    return numerator/denominator

