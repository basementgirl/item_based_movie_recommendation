import math

dic={}
dic.setdefault('1',{})
print(dic)
dic['1']['1']=5
print(dic)

#setdefault函数，如果字典中存在这个key，则吧它打印出来。如果没有，则给赋值。
dic.setdefault('1',{})
print(dic)
dic['1']['2']=3
print(dic)


dic.setdefault('2',{})
print(dic)
dic['2']['1']=4
print(dic)

dic.setdefault('5',{})
print(dic)
dic['5']['7']=4
print(dic)

dic.setdefault('5',{})
print(dic)
dic['5']['9']=5
print(dic)

dic.setdefault('10',{})
print(dic)
dic['10']['8']=3
print(dic)

C = dict()  # 物品-物品的共现矩阵
N = dict()  # 物品被多少个不同用户购买


for user, items in dic.items():
    for i in items.keys():

        N.setdefault(i, 0)
        N[i] += 1
        C.setdefault(i, {})
        #print(C)
        for j in items.keys():

            if i == j: continue
            C[i].setdefault(j, 0)
            C[i][j] += 1
        print(C)
            #continue在此，是若满足条件。则后两句不执行。继续j.


W = dict()
for i, related_items in C.items():
    W.setdefault(i, {})
    for j, cij in related_items.items():
        W[i][j] = cij / (math.sqrt(N[i] * N[j]))
print(W)
print(W['2']['1'])



