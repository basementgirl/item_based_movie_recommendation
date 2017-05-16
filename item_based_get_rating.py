from load_movielens import loadMovieLensTrain
from load_movielens import loadMovieLensTest
from math import sqrt
import time
start_time=time.time()


#得到物品之间的相似度。W是用来项目之间相似度的矩阵。
def itemSimilarity(train):
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
    return C,N,W


def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count


#获取当前要预测的项目的最近邻居项目。
def topKMatches(train, w,userid, itemid, k=30):
    #item_set是该用户评价过的所有商品。
    item_set=[]
    #items才是当前待评价商品的最近邻居商品。
    items=[]

    for item in train[userid]:
        item_set.append(item)

    scores = [(w[itemid][item], item) for item in item_set if itemid != item and item in w[itemid]]

    scores.sort()
    scores.reverse()
    if len(scores) <= k:
        for item in scores:
            items.append(item)
    else:
        kscore = scores[0:k]
        for item in kscore:
            items.append(item)
        #items表示最近邻项目。及这些最近邻居项目与待预测项目的相似度。它是由元组构成的列表。每一个元组都由相似度和邻居id组成。
    return items


#获取测试集中每个用户对每个商品的预测评分
def getRating(train,w, userid, itemid):
    if itemid not in w.keys():
        s=getAverage(train, userid)
        return s
    else:
        items = topKMatches(train,w, userid, itemid)
        s=0
        wight_count=0
        for i in items:
            s=s+i[0]*train[userid][i[1]]
            wight_count+=i[0]
        return s/wight_count


#通过调用getRating函数来获取预测评分。
def getAllRating(trainFilename, testFilename, fileResult):
    print("start load train data :")
    train = loadMovieLensTrain(trainFilename)

    print("start load test data :")
    test = loadMovieLensTest(testFilename)

    print("start caculate C,N,W :")
    C,N,W = itemSimilarity(train)
    print("end caculate C,N,W")

    inAllnum = 0
    file = open(fileResult, 'w')
    for userid in test:
        for itemid in test[userid]:
            rating = getRating(train,W, userid, itemid)
            file.write('%s,%s,%s\n'%(userid, itemid, rating))
            inAllnum = inAllnum +1
            print("complete : %d"%inAllnum)
    file.close()
    print("-------------Completed!!-----------",inAllnum)



if __name__ == "__main__":
    print("\n--------------The program is running, please wait!... -----------\n")
    for i in range(1,6):
        getAllRating('u%d.base'%i, 'u%d.test'%i, 'u%dresult.csv'%i)
        print('The %d st is done,please wait!'%i)
        print(time.time()-start_time)







