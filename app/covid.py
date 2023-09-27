import torch
from torch import nn
import torch.nn.functional as F
import numpy as np

torch.manual_seed(123)
# Contrução do Modelo
class classificador(nn.Module):
  def __init__(self):
      super().__init__()

      self.conv1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3,3)) 
      self.conv2 = nn.Conv2d(64, 64, (3,3))
      self.activation = nn.ReLU()
      self.bnorm = nn.BatchNorm2d(num_features=64)
      self.pool = nn.MaxPool2d(kernel_size=(2,2))
      self.flatten = nn.Flatten()

      # output = (input - filter + 1) / stride
      # Convolução 1 -> (64 - 3 + 1) / 1 = 62x62
      # Pooling 1 -> Só dividir pelo kernel_size = 31x31
      # Convolução 2 -> (31 - 3 + 1)/ 1 = 29x29
      # Pooling 2 -> Só dividir pelo kernel_size = 14x14
      # 14 * 14 * 64
      # 33907200 valores -> 256 neurônios da camada oculta
      self.linear1 = nn.Linear(in_features=14*14*64, out_features=256)
      self.linear2 = nn.Linear(256, 128)
      self.output = nn.Linear(128, 3)

  def forward(self, X):
      X = self.pool(self.bnorm(self.activation(self.conv1(X))))
      X = self.pool(self.bnorm(self.activation(self.conv2(X))))
      X = self.flatten(X)

      # Camadas densas
      X = self.activation(self.linear1(X))
      X = self.activation(self.linear2(X))
      
      # Saída
      X = self.output(X)

      return X

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device

classificadorLoaded = classificador()
state_dict = torch.load('app/checkpoint.pth')
classificadorLoaded.load_state_dict(state_dict)
def transform_imagem(imagem_teste):
    from PIL import Image
    imagem = Image.open(imagem_teste)
    imagem = imagem.resize((64, 64))
    imagem = imagem.convert('RGB') 
    imagem = np.array(imagem.getdata()).reshape(*imagem.size, -1)
    imagem = imagem / 255
    imagem = imagem.transpose(2, 0, 1)
    imagem = torch.tensor(imagem, dtype=torch.float).view(-1, *imagem.shape)
    return imagem

def classificar_imagem(file):
    imagem = transform_imagem(file)
    classificadorLoaded.eval()
    imagem = imagem.to(device)
    output = classificadorLoaded.forward(imagem)
    output = F.softmax(output, dim=1)
    top_p, top_class = output.topk(k = 1, dim = 1)
    output = output.detach().numpy()
    resultado = np.argmax(output)
    return resultado
