from load_movielens import loadMovieLensTrain
from load_movielens import loadMovieLensTest
from item_based_similarity_function import sim_adcos
from item_based_similarity_function import sim_cos
from item_based_similarity_function import sim_pearson
import time
start_time=time.time()


def topKMatches(trainSet, presentUserid, presentItemid, sim,k=30):
    #假如当前用户不是新用户，有评价过的项目x。但x和当前项目没有共同用户。则默认相似度为0.3。（见相似度函数）
    scores = [(sim(trainSet, presentItemid, other),other) for other in trainSet[presentUserid] if other!=presentItemid]
    scores.sort()
    scores.reverse()

    if len(scores)<=k:
        neighborSimAndItems=scores
        return neighborSimAndItems
    else:
        neighborSimAndItems = scores[0:k]
        return neighborSimAndItems
#neighborSimAndItems此时是以元组为元素的列表。每个元组包括包括邻居项目与当前项目的相似度以及邻居项目id。


def getUserAverage(trainSet, userid):
    count = 0
    sum = 0
    for item in trainSet[userid]:
        sum = sum + trainSet[userid][item]
        count = count+1
    return sum/count


def getItemAverage(trainSet, itemid):
    all_scores_for_item=[] #存放所有用户对这个项目的评分。
    for (user, items) in trainSet.items():
        if itemid in items:
            all_scores_for_item.append(trainSet[user][itemid])
    avg_item=sum(all_scores_for_item)/len(all_scores_for_item)
    return avg_item


#预测评分
def getRating(trainSet, presentUserid, presentItemid,sim):
    all_scores_for_item = []  # 存放所有用户对这个项目的评分。
    for (user, items) in trainSet.items():
        if presentItemid in items:
            all_scores_for_item.append(trainSet[user][presentItemid])
    if presentUserid not in trainSet:
        if len(all_scores_for_item)==0:
            return 3
        #如果当前用户是新用户，当前商品又是新项目。则返回默认评分3.
        else:
            return sum(all_scores_for_item)/len(all_scores_for_item)
        #如果当前用户是新用户，但当前商品不是新项目，则返回当前商品的平均评分。
    else:
        if len(all_scores_for_item)==0:
            return getUserAverage(trainSet, presentUserid)
        #如果当前用户不是新用户，但当前商品是新项目。则返回当前用户的平均评分
        else:
        # 如果当前用户不是新用户。当前商品又不是新商品。则按正常流程来。
            neighborSimAndItems = topKMatches(trainSet, presentUserid, presentItemid, sim)
            s=0  #代表分子。即当前用户对每个近邻物品的评分乘上该近邻物品与当前物品的相似度。然后再求和的结果。
            simSum = 0
            avgOfPresentItem=sum(all_scores_for_item)/len(all_scores_for_item)

            for i in neighborSimAndItems:
                avgOfNeighborItem = getItemAverage(trainSet, i[1])
                s = s + abs(i[0]) * (trainSet[presentUserid][i[1]]-avgOfNeighborItem)
                simSum+=abs(i[0])
            return avgOfPresentItem+s/simSum


def getAllUserRating(fileTrain, fileTest, fileResult,sim):
    trainSet = loadMovieLensTrain(fileTrain)
    testSet = loadMovieLensTest(fileTest)
    inAllnum = 0
    file = open(fileResult, 'w')
    for presentUserid in testSet:
        for presentItem in testSet[presentUserid]:
            rating = getRating(trainSet, presentUserid, presentItem,sim)
            file.write('%s,%s,%.4f\n'%(presentUserid, presentItem, rating))
            inAllnum = inAllnum +1
    file.close()
    print("a train set is done",inAllnum)


if __name__ == "__main__":
    print("The program is running, please wait!")
    for i in ('sim_pearson','sim_adcos'):
        if i=='sim_cos':
            sim=sim_cos
        elif i=='sim_adcos':
            sim=sim_adcos
        else:
            sim=sim_pearson
        print('item based with %s is running ,please wait!'%i)
        for j in range(1,6):
            getAllUserRating('u%d.base'%j, 'u%d.test'%j, 'item_based_with_%s/u%dpredict.csv'%(i,j),sim)
            print('The %d st train set is done,please wait!'%j)
        print('item based with %s is finished!'%i)
        print(time.time() - start_time)
    print("Report, master,the program is finished!")
    print('Total running time is :',time.time() - start_time)