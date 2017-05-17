from load_movielens import loadMovieLensTrain
from load_movielens import loadMovieLensTest
from user_based_similarity_function import sim_adcos
from user_based_similarity_function import sim_cos
from user_based_similarity_function import sim_pearson


import time
start_time=time.time()


def topKMatches(trainSet, presentUserid, presentItemid, sim,k=30):
    userSet = []#userSet表示评价过当前商品的所有用户
    neighborUsers = []#neighborUsers最近邻居用户。
    for user in trainSet:
        if presentItemid in trainSet[user]:
            userSet.append(user)
    scores = [(sim(trainSet, presentUserid, other),other) for other in userSet if other!=presentUserid]
    scores.sort()
    scores.reverse()
    if len(scores)<=k:       
        for item in scores:
            neighborUsers.append(item[1])
        return neighborUsers
    else:                  
        kscore = scores[0:k]
        for item in kscore:
            neighborUsers.append(item[1])
        return neighborUsers


def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count


def getRating(trainSet, presentUserid, presentItemid,sim):
    jiaquanAverage = 0.0
    simSums = 0.0
    neighborUsers = topKMatches(trainSet, presentUserid, presentItemid, sim)
    averageOfUser = getAverage(trainSet, presentUserid)
    for other in neighborUsers:
        similarity = sim(trainSet, presentUserid, other)
        averageOther = getAverage(trainSet, other)
        simSums += abs(similarity )
        jiaquanAverage +=  (trainSet[other][presentItemid]-averageOther)*similarity
    if simSums==0:
        return averageOfUser
    else:
        return (averageOfUser + jiaquanAverage/simSums)  


def getAllUserRating(fileTrain, fileTest, fileResult,i):
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







