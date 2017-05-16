
#将训练集转换为字典
def loadMovieLensTrain(filename):
    str1 = './movielens/'
    train = {}
    for line in open(str1 + filename, 'r'):
        (userid, movieid, rating, ts) = line.split()
        train.setdefault(userid, {})
        train[userid][movieid] = float(rating)
    return train


#将测试集转换为字典
def loadMovieLensTest(filename):
    str1 = './movielens/'
    test = {}
    for line in open(str1 + filename, 'r'):
        (userid, movieid, rating, ts) = line.split()
        test.setdefault(userid, {})
        test[userid][movieid] = float(rating)
    return test
