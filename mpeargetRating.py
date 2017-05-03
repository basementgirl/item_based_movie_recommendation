from math import sqrt
from mpearloadMovieLens import loadMovieLensTrain
from mpearloadMovieLens import loadMovieLensTest

def sim_mpearson(prefer, person1, person2):
    sim = {}
    for item in prefer[person1]:
        if item in prefer[person2]:
            sim[item] = 1
    n = len(sim)
    if len(sim)==0:
        return -1
    sum1=sum([prefer[person1][item] for item in prefer[person1]])
    sum2=sum([prefer[person2][item] for item in prefer[person2]])
    n1=len(prefer[person1])
    n2=len(prefer[person2])
    avg1=sum1/n1
    avg2=sum2/n2
    summulti=sum([(prefer[person1][item]-avg1)*(prefer[person2][item]-avg2) for item in sim])
    sq1=sqrt(sum([pow((prefer[person1][item]-avg1),2) for item in sim]))
    sq2=sqrt(sum([pow((prefer[person2][item]-avg2),2) for item in sim]))
    sq=sq1*sq2
    if sq==0:
        return 0
    result=summulti/sq
    return result

def topKMatches(prefer, person, itemId, k=60, sim = sim_mpearson):
    userSet = []
    scores = []
    users = []
    for user in prefer:
        if itemId in prefer[user]:
            userSet.append(user)
    scores = [(sim(prefer, person, other),other) for other in userSet if other!=person]
    scores.sort()
    scores.reverse()
    if len(scores)<=k:       
        for item in scores:
            users.append(item[1])  
        return users
    else:                  
        kscore = scores[0:k]
        for item in kscore:
            users.append(item[1])  
        return users             

def getAverage(prefer, userId):
    count = 0
    sum = 0
    for item in prefer[userId]:
        sum = sum + prefer[userId][item]
        count = count+1
    return sum/count

def getRating(prefer1, userId, itemId, knumber=60,similarity=sim_mpearson):
    sim = 0.0
    averageOther =0.0
    jiaquanAverage = 0.0
    simSums = 0.0

    users = topKMatches(prefer1, userId, itemId, k=knumber, sim = sim_mpearson)
    averageOfUser = getAverage(prefer1, userId)
    for other in users:
        sim = similarity(prefer1, userId, other)    
        averageOther = getAverage(prefer1, other)  
        simSums += abs(sim)    
        jiaquanAverage +=  (prefer1[other][itemId]-averageOther)*sim   

    if simSums==0:
        return averageOfUser
    else:
        return (averageOfUser + jiaquanAverage/simSums)  

def getAllUserRating(fileTrain, fileTest, fileResult, similarity=sim_mpearson):
    prefer1 = loadMovieLensTrain(fileTrain)        
    prefer2 = loadMovieLensTest(fileTest)            
    inAllnum = 0

    file = open(fileResult, 'a')
    for userid in prefer2:            
        for item in prefer2[userid]:   
            rating = getRating(prefer1, userid, item, 60)  
            file.write('%s\t%s\t%s\n'%(userid, item, rating))
            inAllnum = inAllnum +1
    file.close()
    print("-------------Completed!!-----------",inAllnum)

if __name__ == "__main__":
    print("\n--------------The program is running, please wait!... -----------\n")
    getAllUserRating('u5.base', 'u5.test', 'u5result.txt')









