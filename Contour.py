import os
import io
import pandas as pd
import matplotlib.pyplot as plt
import glob
from PIL import Image

path = os.path.dirname(__file__)

AllValues = []
dataPoints = len(glob.glob(f"{path}/rawData/*.tas"))

# load all data
for idx in range(dataPoints):
    df = pd.read_csv(
        f"{path}/rawData/FRD " + str(idx) + ".tas", delimiter="\t", header=None
    )
    AllValues.append(df.values.tolist())

# format data
X = df.columns.values
Y = list(range(dataPoints))
Z = []

for coloumn, val in enumerate(X):
    ProperList = []

    for idx in range(dataPoints):
        FinalizedList = AllValues[idx][coloumn]
        ProperList.append(FinalizedList)

    Z.append(ProperList)

# store plots
frames = []

for idx, val in enumerate(Z):
    fig = plt.figure()
    plt.contourf(X, Y, Z[idx])
    plt.colorbar()
    plt.axis("auto")

    # save figure in memory
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    new_frame = Image.open(buf)
    frames.append(new_frame)

    plt.close(fig)

duration = round(len(frames) / 30)

# export GIF
frames[0].save(
    f"{path}/gr.gif",
    format="GIF",
    append_images=frames[1:],
    save_all=True,
    duration=duration,
    loop=0,
)
