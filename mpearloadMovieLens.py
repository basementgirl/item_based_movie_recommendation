def loadMovieLensTrain(fileName):
    str1 = './movielens/'                         
    
    prefer = {}
    for line in open(str1+fileName,'r'):      
        (userid, movieid, rating,ts) = line.split()
        prefer.setdefault(userid, {})      
        prefer[userid][movieid] = float(rating)    

    return prefer     

def loadMovieLensTest(fileName):
    str1 = './movielens/'    
    prefer = {}
    for line in open(str1+fileName,'r'):    
        (userid, movieid, rating,ts) = line.split()
        prefer.setdefault(userid, {})    
        prefer[userid][movieid] = float(rating)   
    return prefer                   
print(len(loadMovieLensTest('u5.test')))

                        

















