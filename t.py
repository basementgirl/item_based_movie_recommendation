dic={'1': {'1': 5, '2': 3}, '2': {'1': 4}}
for user, items in dic.items():
    for i in items.keys():
        print(i,'a')
        for j in items.keys():
            print(j, 'bb')