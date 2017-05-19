from load_movielens import loadMovieLensTrain
from load_movielens import loadMovieLensTest
from item_based_similarity_function import sim_adcos
from item_based_similarity_function import sim_cos
from item_based_similarity_function import sim_pearson
import time
start_time=time.time()


def topKMatches(trainSet, presentUserid, presentItemid, sim,k=30):
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


#预测评分
def getRating(trainSet, presentUserid, presentItemid,sim):
    neighborSimAndItems = topKMatches(trainSet, presentUserid, presentItemid, sim)
    s=0  #代表分子。即当前用户对每个近邻物品的评分乘上该近邻物品与当前物品的相似度。然后再求和的结果。
    simSum = 0
    for i in neighborSimAndItems:
        s = s + i[0] * trainSet[presentUserid][i[1]]
        simSum+=i[0]

    if simSum==0:
        return sum([trainSet[presentUserid][item] for item in trainSet[presentUserid]])/len(trainSet[presentUserid])
    return s/simSum


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
    for i in ('sim_cos','sim_adcos','sim_pearson'):
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