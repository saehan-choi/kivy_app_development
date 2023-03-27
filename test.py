import timm

# print(timm.list_models())



f = open('haha.txt', 'a')

for idx, i in enumerate(timm.list_models()):

    f.write(i+'  ')
    
    if idx%100==0:
        f.write('\n')
    
f.close()