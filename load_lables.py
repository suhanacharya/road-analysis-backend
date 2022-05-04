d = {}

label = {
    "4-7": ["horn"],
    "15-23": ["Gearchange"],
    "7-25": ["noise"]
}

for i in range(0, 100, 2):
    i_1 = i+1
    d[f"{i}-{i_1}"] = []

for k,v in label.items():
    start_k, end_k = list(map(int, k.split("-")))
    lk = list(range(start_k, end_k+1))
    # print("startk", start_k,"endk", end_k)
    for kd in d.keys():
        dstart_k, dend_k = list(map(int,kd.split("-")))
        dlk = list(range(dstart_k, dend_k+1))
        # print("dstartk", dstart_k,"dendk", dend_k)
        intersect = list(set(lk) & set(dlk))
        if len(intersect) > 0:
            d[kd].append(v)
        
         
print(d)        



