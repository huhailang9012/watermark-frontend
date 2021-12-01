import json

import requests

n= 6
dt = []
dindex = []
index=[]
dict={'0':0,'1':0}
def str2index(str):
    x, y, k = 0, 0, 0
    for k in str:
        dt.append(k)
    for i in range(6):
        dindex=dt[i:30:6]
        for key in dindex:
            dict[key]+=1
        if(dict['0']>dict['1']):
            index.append('0')
        else:
            index.append('1')
        dict['0'] = 0
        dict['1'] = 0
    print("得到索引串："+"".join(index))
    return "".join(index)

# 识别是否存在相似水印
def recognize(filename: str):
    url = 'http://10.64.71.21:8000/audio/recognize'
    payload = {'filename': filename}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    bool = data['data']
    return bool
