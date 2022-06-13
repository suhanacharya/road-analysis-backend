import csv
import os
import shutil
import argparse

# read data from csv to a dictionary
# if csv is like this:
# "1-2", "a"
# dictionary will be like this:
# {"1-2": "a"}

parser = argparse.ArgumentParser()  
parser.add_argument("-f", help="file name")

args = parser.parse_args()
file_name = args.f

with open("data/labels/labels.csv", "r") as f:
    reader = csv.reader(f)
    label = dict(reader)
    # print(label)

d = {}

for i in range(0, 974, 2):
    i_1 = float(i)+2
    i_f = float(i)
    d[f"{i_f}-{i_1}"] = ""

for k,v in label.items():
    print(k)
    start_k, end_k = k.split("-")
    start_k = start_k.split(":")
    start_k = float(start_k[0])*60 + float(start_k[1])
    end_k = end_k.split(":")
    end_k = float(end_k[0])*60 + float(end_k[1])
    
    dir_name = f"{file_name}/"+str(v)
    new_dir = f"./data/spectrogram/segments/{dir_name}"
    # print(new_dir)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    
    for kd in d.keys():
        dstart_k, dend_k = list(map(float,kd.split("-")))
        if start_k < dstart_k <= end_k or start_k <= dend_k <= end_k:
            if d[kd] == "":
                d[kd] = v
            else:
                d[kd] = d[kd]+";"+str(v)
                
for k,v in d.items():
    if v == "":
        d[k] = "regular"
        labels = "regular"
        dir_name = f"{file_name}/"+"regular"
        new_dir = f"./data/spectrogram/segments/{dir_name}"
        # print(new_dir)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
    else:
        labels = v

    fname = f"{file_name}_"+k+".png"
    print(fname, v)
    labels = labels.split(";")
    for l in labels:
        shutil.copyfile(f"./data/spectrogram/segments/{file_name}/{fname}", f"./data/spectrogram/segments/{file_name}/{l}/{fname}")
    
                
# write data to csv
with open("data/labels/complete_labels.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for k,v in d.items():
        writer.writerow([k,v])

# print(d)