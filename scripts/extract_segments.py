# -*- coding: utf-8 -*-
"""按镜头段抽取每个案例的代表帧（段中间帧），全分辨率 JPEG。"""
import cv2
import numpy as np
import os
import json

SRC = r'D:\edge默认下载\47b602a7f4c1687294ad243b193f977e.mp4'
OUT = r'D:\绘图绘表skills\frames'
os.makedirs(OUT, exist_ok=True)

diffs = np.load(os.path.join(OUT, 'diffs.npy'))
N = len(diffs)

THR = 5
cuts = [i for i in range(1, N) if diffs[i] > THR]
segs = []
start = 0
for c in cuts + [N]:
    if c - start >= 2:
        segs.append((start, c))
    start = c

print('segments =', len(segs))

cap = cv2.VideoCapture(SRC)
meta = []
for k, (a, b) in enumerate(segs, 1):
    mid = (a + b) // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ok, frame = cap.read()
    if not ok:
        print('READ FAIL seg', k, 'frame', mid)
        continue
    # 裁掉顶部可能的黑边无意义区，保留原样
    name = 'seg_%03d.jpg' % k
    okenc, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
    with open(os.path.join(OUT, name), 'wb') as f:
        f.write(buf.tobytes())
    meta.append({'seg': k, 'frames': [a, b], 'mid': mid, 'file': name})
cap.release()

with open(os.path.join(OUT, 'segments.json'), 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)
print('saved', len(meta), 'frames to', OUT)
