# -*- coding: utf-8 -*-
"""从蒙太奇视频中按镜头分段抽取每个案例的代表帧。"""
import cv2
import numpy as np
import os
import json

SRC = r'D:\edge默认下载\47b602a7f4c1687294ad243b193f977e.mp4'
OUT = r'D:\绘图绘表skills\frames'
os.makedirs(OUT, exist_ok=True)

cap = cv2.VideoCapture(SRC)
grays = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    small = cv2.resize(f, (135, 180))
    grays.append(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY).astype(np.float32))
cap.release()

N = len(grays)
diffs = np.zeros(N)
for i in range(1, N):
    diffs[i] = float(np.abs(grays[i] - grays[i - 1]).mean())

print('N frames =', N)
print('diff stats: median=%.2f p75=%.2f p90=%.2f p99=%.2f max=%.2f' % (
    np.median(diffs[1:]), np.percentile(diffs[1:], 75),
    np.percentile(diffs[1:], 90), np.percentile(diffs[1:], 99), diffs[1:].max()))

for thr in (3, 5, 8, 12, 18):
    cuts = [i for i in range(1, N) if diffs[i] > thr]
    # 合并相邻切点（间隔<=2帧视为一次切换）
    merged = []
    for c in cuts:
        if merged and c - merged[-1] <= 2:
            continue
        merged.append(c)
    segs = []
    start = 0
    for c in merged + [N]:
        if c - start >= 2:
            segs.append((start, c))
        start = c
    lens = [b - a for a, b in segs]
    print('thr=%2d cuts=%3d merged=%3d segments=%3d lens(min/med/max)=%d/%d/%d' % (
        thr, len(cuts), len(merged), len(segs),
        min(lens), int(np.median(lens)), max(lens)))

np.save(os.path.join(OUT, 'diffs.npy'), diffs)
