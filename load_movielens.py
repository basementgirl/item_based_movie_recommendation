
#将训练集转换为字典
def loadMovieLensToDict(filename):
    str1 = './movielens/'
    dataSet = {}
    for line in open(str1 + filename, 'r'):
        (userid, movieid, rating, ts) = line.split(',')
        dataSet.setdefault(userid, {})
        dataSet[userid][movieid] = float(rating)
    return dataSet