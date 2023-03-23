
import timm
import torch
# print(timm.list_models())

model = timm.create_model('efficientnet_b0', pretrained=True)
img = torch.randn((1,3,224,224))
print(model(img).size())

# 여기서 제일 큰거 하나만 
# torch with nograd, torch eval 하고 적용하기.
