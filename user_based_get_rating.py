from load_movielens import loadMovieLensTrain
from load_movielens import loadMovieLensTest
from user_based_similarity_function import sim_adcos
from user_based_similarity_function import sim_cos
from user_based_similarity_function import sim_pearson


import time
start_time=time.time()


def topKMatches(trainSet, presentUserid, presentItemid, sim,k=30):
    userSet = []#userSet表示评价过当前商品的所有用户

    for user in trainSet:
        if presentItemid in trainSet[user]:
            userSet.append(user)
    scores = [(sim(trainSet, presentUserid, other),other) for other in userSet if other!=presentUserid]
    scores.sort()
    scores.reverse()
    # neighborSimAndUsers最近邻居用户。
    if len(scores)<=k:
        neighborSimAndUsers=scores
        return neighborSimAndUsers
    else:                  
        kscore = scores[0:k]
        neighborSimAndUsers = kscore
        return neighborSimAndUsers


def getUserAverage(trainSet, userid):
    count = 0
    sum = 0
    for item in trainSet[userid]:
        sum = sum + trainSet[userid][item]
        count = count+1
    return sum/count



def getRating(trainSet, presentUserid, presentItemid,sim):
    all_scores_for_item = []  # 存放所有用户对这个项目的评分。
    for (user, items) in trainSet.items():
        if presentItemid in items:
            all_scores_for_item.append(trainSet[user][presentItemid])
    if presentUserid not in trainSet:
        if len(all_scores_for_item) == 0:
            return 3
        # 如果当前用户是新用户，当前商品又是新项目。则返回默认评分3.
        else:
            return sum(all_scores_for_item) / len(all_scores_for_item)
            # 如果当前用户是新用户，但当前商品不是新项目，则返回当前商品的平均评分。
    else:
        if len(all_scores_for_item) == 0:
            return getUserAverage(trainSet, presentUserid)
        # 如果当前用户不是新用户，但当前商品是新项目。则返回当前用户的平均评分
        else:
            neighborSimAndUsers = topKMatches(trainSet, presentUserid, presentItemid, sim)
            averageOfUser = getUserAverage(trainSet, presentUserid)
            s=0
            simSum = 0
            for i in neighborSimAndUsers:
                averageOfneighborUser = getUserAverage(trainSet, i[1])
                s = s + abs(i[0]) * (trainSet[i[1]][presentItemid]-averageOfneighborUser)
                simSum+=abs(i[0])
            if simSum==0:
                return averageOfUser

            return (averageOfUser + s/simSum)


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
        print('user based with %s is running ,please wait!'%i)
        for j in range(1,6):
            getAllUserRating('u%d.base'%j, 'u%d.test'%j, 'user_based_with_%s/u%dpredict.csv'%(i,j),sim)
            print('The %d st train set is done,please wait!'%j)
        print('user based with %s is finished!'%i)
        print(time.time() - start_time)
    print("Report, master,the program is finished!")
    print(time.time() - start_time)







