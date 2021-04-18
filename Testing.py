import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from PIL import Image

path = os.path.dirname(__file__)

i = 0
coloumn = 0
FRD = 0

AList = []
VList = []
ProperList = []

abc = []
xyz = []

while i < len(glob.glob(f'{path}\\Hole\\*')) :

    df = pd.read_csv(f'{path}\\Hole\\FRD ' + str(i) +'.tas', delimiter = '\t', header=None)
   
    Horizontal = df.columns.values
    Vertical = [*range(len(glob.glob(f'{path}\\Hole\\*.tas')))]
    
    HList = df.columns.values.tolist()
    TList = df.index.values.tolist()
    AList.append(df.values.tolist())
    VList.append(i)

    i += 1

while coloumn < len(Horizontal) :
    FRD = 0


    while FRD < len(glob.glob(f'{path}\\Hole\\*.tas')) :

        FinalizedList = AList[FRD][coloumn]
        ProperList.append(FinalizedList)

        if len(ProperList) == len(glob.glob(f'{path}\\Hole\\*.tas')) :
            abc.append(ProperList)
            ProperList = []
        FRD += 1

    coloumn += 1

if not os.path.exists(f'{path}/images'):
    os.makedirs(f'{path}/images')

PicNum = 0

while PicNum < len(abc) :
        
    fig = plt.figure()

    plt.contourf(Horizontal,Vertical,abc[PicNum])
    plt.colorbar()
    plt.axis('auto')

    fig.savefig(f'{path}\\images\\image {str(PicNum)}.png')
    
    PicNum += 1

frames = []
imgs = glob.glob(f'{path}\\images\\*.png')

imgs.sort(key=lambda y: int(y.split(" ")[-1][0:-4]))

print(imgs)
for a in imgs:
    new_frame = Image.open(a)
    frames.append(new_frame)

DurationCalc = round(len(glob.glob(f'{path}\\images\\*.png')) / 30)

frames[0].save(f'{path}\\images\\gr.gif', format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=DurationCalc, loop=0)