import subprocess

import json

import requests as requests
import time
nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
from conSql import search_maxid, insert_msg, search
from stegstash import soundlsb

def audio_embed(filename: str, secrest: str):
    cmd = 'ffmpeg -i {} -f wav -ar 16000 {}'
    cmd.format(filename, './audio.wav')
    subprocess.call(cmd, shell=True)

    cmd = 'ffmpeg -i ' + filename + ' -vcodec copy -an video.avi'
    subprocess.call(cmd, shell=True)

    soundlsb.simpleEncode("./audio.wav", "./audio_embed.wav", secrest)

    cmd = 'ffmpeg -i ./video.avi -i ./audio_embed.wav -vcodec copy -acodec copy ./test3_embed.mp4'
    subprocess.call(cmd, shell=True)

    return "./audio_embed.wav"


def remote_fingerprint(source_path: str):

    payload = {"source_path": source_path, "format": 'wav'}
    url = 'http://10.64.71.21:8000/audio/fingerprinting'
    requests.post(url, payload)


def fingerprinting(filename: str, secrest: str):
    embed_name = audio_embed(filename, secrest)
    remote_fingerprint(embed_name)


def remote_embed(path: str, secrets: str) -> str:
    payload = {"video_path": path, "secrets": secrets}
    print("embedStart"+nowTime)
    url = 'http://10.64.71.21:8000/watermark/embed'
    params = json.dumps(payload)
    r = requests.post(url, params)
    data = json.loads(r.text)
    path = data['data']
    print("path ", path)
    print("embedEnd"+nowTime)
    return path


def remote_extract(path: str) -> str:
    url = 'http://10.64.71.21:8000/watermark/extract'
    payload = {"video_path": path}
    r = requests.get(url, params=payload)
    data = json.loads(r.text)
    secrets = data['data']
    print("2222",data)
    return secrets


def embed_msg(filename: str, secrets: str, mtype: str) -> str:
    max_id = search_maxid()
    if max_id == None:
        max_id = '0'
    integer = int(max_id, 2)
    integer = integer + 1
    id = "1101110111"+'{:012b}'.format(integer)+"1101110111"
    # 先调用远程嵌入信息接口
    print(id)
    path = remote_embed('/data/huhailang/frontend/upload/' + filename, id)
    insert_msg(id, secrets, mtype)
    return path, id


def extract_msg(filename: str) -> tuple:
    index = remote_extract('/data/huhailang/frontend/upload/' + filename)
    print("3333",index)
    if(index is None):
        return None
    else:
        return search(index)


n= 6
dt = []
dindex = []
index=[]
dict={'0':0,'1':0}
def vote(str) -> str:
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
    return "".join(index)

if __name__ == '__main__':
    print(vote('00001100001100001110000110000100'))

