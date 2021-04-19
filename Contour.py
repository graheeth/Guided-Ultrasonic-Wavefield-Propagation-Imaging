import os
import io
import re
import pandas as pd
import matplotlib.pyplot as plt
import glob
from PIL import Image

path = os.path.dirname(__file__)

all_files = glob.glob(f"{path}/rawData/*.tas")
all_files.sort(key=lambda f: int(re.sub("\D", "", f)))

raw_csv = [pd.read_csv(file, delimiter="\t", header=None) for file in all_files]

num_rows = len(raw_csv[0])  # 500
num_files = len(all_files)  # 51

# format data
sorted_csv = []
rows = len(raw_csv[0].index)

for index in range(rows):
    for i, df in enumerate(raw_csv):
        sorted_csv.append(df.iloc[index])


sorted_csv = pd.DataFrame(sorted_csv)
X = sorted_csv.columns.values  # 200
Y = [*range(int(len(sorted_csv.index) / num_rows))]  # 51

# store plots
frames = []
fig = plt.figure()

for i in range(num_rows):
    print(f"Processing contour {str(i + 1)}...")

    plt.contourf(X, Y, sorted_csv.iloc[i * num_files : (i + 1) * num_files])
    plt.colorbar()
    plt.axis("auto")

    # save figure in memory
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    new_frame = Image.open(buf)
    frames.append(new_frame)

    plt.clf()

# export GIF
duration = round(len(frames) / 30)

frames[0].save(
    f"{path}/gr.gif",
    format="GIF",
    append_images=frames[1:],
    save_all=True,
    duration=duration,
    loop=0,
)
