from math import sqrt

from item_based_load import loadMovieLensTest


def ItemSimilarity(train):

    # 建立物品-物品的共现矩阵
    C = dict()  # 物品-物品的共现矩阵
    N = dict()  # 物品被多少个不同用户购买
    for user, items in train.items():
        for i in items.keys():
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j in items.keys():
                if i == j: continue
                C[i].setdefault(j, 0)
                C[i][j] += 1
                # 计算相似度矩阵

    # w指相似度。
    W = dict()
    for i, related_items in C.items():
        W.setdefault(i, {})
        for j, cij in related_items.items():
            W[i][j] = cij / (sqrt(N[i] * N[j]))
    return W

trainFilename='u1.base'
train = loadMovieLensTest(trainFilename)
print(ItemSimilarity(train))