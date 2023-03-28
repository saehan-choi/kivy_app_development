# import timm

# # print(timm.list_models())



# f = open('haha.txt', 'a')

# for idx, i in enumerate(timm.list_models()):

#     f.write(i+'  ')
    
#     if idx%100==0:
#         f.write('\n')
    
# f.close()

import torch

a = torch.tensor([0,0,0,0,0,        0,0,0,0,0], dtype=torch.float)
b = torch.tensor([True,True,True,True,True,           False,True,True,True,True], dtype=torch.bool)
a[b] = torch.tensor([5.6, 5.3, 5.2, 5.4, 5.1,  1.2, 1.5, 1.8, 1.9], dtype=torch.float)
print(a)