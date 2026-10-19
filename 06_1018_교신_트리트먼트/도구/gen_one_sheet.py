# -*- coding: utf-8 -*-
"""1호의 모습: 붉은 표시등 한 점의 문법, 정비 카메라, 정비 암, 바깥에서 보는 창.
Usage: python3 -I gen_one_sheet.py out.svg
"""
import sys
from html import escape as esc

OUT = sys.argv[1]
W, H = 1460, 700
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
BG = "#15171b"; BLOCK = "#1c1f25"; EDGE = "#353a43"
WHITE = "#f1f1f1"; GREY = "#9aa0a8"; DIM = "#5f6670"
RED = "#ff4a3c"; GOLD = "#d4a62a"; HULL = "#e9e9e6"

o = []
A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
A('<defs>')
A('<radialGradient id="gR"><stop offset="0" stop-color="#ff5a4a" stop-opacity="0.85"/><stop offset="1" stop-color="#ff5a4a" stop-opacity="0"/></radialGradient>')
A('<radialGradient id="gW"><stop offset="0" stop-color="#ffffff" stop-opacity="0.8"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>')
A('<radialGradient id="gG"><stop offset="0" stop-color="#ffe08a" stop-opacity="0.9"/><stop offset="1" stop-color="#ffe08a" stop-opacity="0"/></radialGradient>')
A('<radialGradient id="halo"><stop offset="0" stop-color="#ff3b2a" stop-opacity="0.8"/><stop offset="1" stop-color="#ff3b2a" stop-opacity="0"/></radialGradient>')
A('</defs>')
A(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
A(f'<text x="30" y="34" fill="{WHITE}" font-size="20" font-weight="bold">1호의 모습 · 점 하나와 눈 하나</text>')
A(f'<text x="30" y="58" fill="{GREY}" font-size="13">1호에게 LED 화면은 없다. 주 제어 패널의 붉은 표시등 한 점이 맥박이고, 레일 위의 정비 카메라가 눈이다. 화면의 흰 글자는 상태 기록이지 표정이 아니다.</text>')


def dot(x, y, r=4.5, col="red"):
    g = {"red": "gR", "white": "gW", "gold": "gG"}[col]
    c = {"red": RED, "white": WHITE, "gold": "#ffe08a"}[col]
    A(f'<circle cx="{x}" cy="{y}" r="{r*3}" fill="url(#{g})"/>')
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')


def block(x, y, w, h, title):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{BLOCK}" stroke="{EDGE}" stroke-width="1.5"/>')
    A(f'<text x="{x+20}" y="{y+30}" fill="{WHITE}" font-size="14" font-weight="bold">{esc(title)}</text>')


# ---------- A. 바깥에서 보는 1호 ----------
ax, ay, aw, ah = 30, 90, 440, 520
block(ax, ay, aw, ah, "밖에서 보는 1호")
# wings
for wx in (ax + 22, ax + 338):
    A(f'<rect x="{wx}" y="{ay+120}" width="80" height="40" rx="3" fill="{GOLD}" stroke="#8a6a12" stroke-width="1"/>')
    for k in range(1, 3):
        A(f'<line x1="{wx + k*80/3:.1f}" y1="{ay+120}" x2="{wx + k*80/3:.1f}" y2="{ay+160}" stroke="#8a6a12" stroke-width="1"/>')
# hull
A(f'<rect x="{ax+100}" y="{ay+95}" width="240" height="90" rx="40" fill="{HULL}" stroke="#b9b9b4" stroke-width="1.5"/>')
# docking port (left end), folded arm (bottom)
A(f'<rect x="{ax+84}" y="{ay+125}" width="18" height="30" rx="4" fill="#cfcfca" stroke="#9c9c97" stroke-width="1"/>')
A(f'<path d="M{ax+170},{ay+185} l 40,8 l 40,-6" fill="none" stroke="#8d8d88" stroke-width="3" stroke-linecap="round"/>')
# window with red dot
wx, wy = ax + 300, ay + 140
A(f'<circle cx="{wx}" cy="{wy}" r="16" fill="#0a0b0e" stroke="#b9b9b4" stroke-width="2"/>')
dot(wx + 3, wy + 3, r=2.6)
# wing tip flash
tx, ty = ax + 24, ay + 140
A(f'<circle cx="{tx}" cy="{ty}" r="16" fill="url(#gG)"/>')
A(f'<path d="M{tx},{ty-9} L{tx+2.5},{ty-2.5} L{tx+9},{ty} L{tx+2.5},{ty+2.5} L{tx},{ty+9} L{tx-2.5},{ty+2.5} L{tx-9},{ty} L{tx-2.5},{ty-2.5} Z" fill="#fff2b0"/>')
A(f'<text x="{ax+20}" y="{ay+215}" fill="{GREY}" font-size="11">창 안쪽 깊은 곳의 붉은 점 · 날개 끝 금박의 번쩍임이 밖으로 보내는 유일한 빛</text>')
# magnified window
mx, my = ax + 220, ay + 360
A(f'<clipPath id="winclip"><circle cx="{mx}" cy="{my}" r="76"/></clipPath>')
A(f'<circle cx="{mx}" cy="{my}" r="78" fill="#0a0b0e" stroke="#b9b9b4" stroke-width="3"/>')
A('<g clip-path="url(#winclip)">')
A(f'<rect x="{mx-70}" y="{my+10}" width="120" height="60" rx="6" fill="#2b2f36" stroke="#434954" stroke-width="1" clip-path="none"/>')
A(f'<rect x="{mx-20}" y="{my+22}" width="40" height="30" rx="5" fill="#b8271b"/>')
dot(mx, my + 10, r=5)
A('</g>')
A(f'<text x="{ax+20}" y="{ay+470}" fill="{GREY}" font-size="11">창 확대 · 패널의 표시등이 창을 통해 보인다. 밖의 붉은 점과 안의 표시등은 같은 LED다.</text>')
A(f'<text x="{ax+20}" y="{ay+490}" fill="{GREY}" font-size="11">얼굴을 그리지 않는다. 흰 원통, 작은 원형 창, 그 안의 점.</text>')

# ---------- B. 표시등 문법 ----------
bx, by, bw, bh = 500, 90, 460, 520
block(bx, by, bw, bh, "표시등 문법 · 10초")
x0, x1 = bx + 30, bx + 420
sec = (x1 - x0) / 10.0
rows = [
    ("평시 · 1초에 한 번", "매일의 보고, 대기, 돌봄", "once"),
    ("긴장 · 1초에 두 번", "접근 물체, 떡잎 발견, 디제이가 사연을 읽을 때", "twice"),
    ("마음이 움직임 · 켜진 채", "지구를 등진 새싹, 꽃말, '벌', 수신 확인 1건", "hold"),
    ("전원 단절 · 꺼짐", "2508일 정전, 랙이 들리는 12초", "off"),
]
for i, (lab, when, mode) in enumerate(rows):
    y = by + 90 + i * 108
    A(f'<text x="{x0}" y="{y-26}" fill="{WHITE}" font-size="12.5" font-weight="bold">{esc(lab)}</text>')
    A(f'<text x="{x0}" y="{y-10}" fill="{GREY}" font-size="10.5">{esc(when)}</text>')
    A(f'<line x1="{x0}" y1="{y+14}" x2="{x1}" y2="{y+14}" stroke="{DIM}" stroke-width="1" stroke-dasharray="{"3,3" if mode=="off" else "0"}"/>')
    for s in range(11):
        tx = x0 + s * sec
        A(f'<line x1="{tx:.1f}" y1="{y+11}" x2="{tx:.1f}" y2="{y+17}" stroke="{DIM}" stroke-width="1"/>')
    if mode == "once":
        for s in range(10):
            dot(x0 + s * sec + sec * 0.5, y, r=4.2)
    elif mode == "twice":
        for s in range(20):
            dot(x0 + s * sec / 2 + sec * 0.25, y, r=3.2)
    elif mode == "hold":
        A(f'<rect x="{x0}" y="{y-8}" width="{x1-x0}" height="16" rx="8" fill="url(#gR)"/>')
        A(f'<rect x="{x0}" y="{y-4}" width="{x1-x0}" height="8" rx="4" fill="{RED}"/>')
    A(f'<text x="{x1}" y="{y+30}" fill="{DIM}" font-size="9.5" text-anchor="end">10초</text>')
A(f'<text x="{x0}" y="{by+bh-22}" fill="{GREY}" font-size="11">표정은 속도뿐이다. 색도 모양도 바뀌지 않는다.</text>')

# ---------- C. 실내의 눈과 손 ----------
cx, cy, cw, ch = 990, 90, 440, 520
block(cx, cy, cw, ch, "안에서의 1호 · 눈과 손")
# rail + camera
ry = cy + 62
A(f'<rect x="{cx+20}" y="{ry}" width="{cw-40}" height="6" rx="3" fill="#4a505b"/>')
camx = cx + 250
A(f'<line x1="{camx}" y1="{ry+6}" x2="{camx}" y2="{ry+24}" stroke="#8d8d88" stroke-width="3"/>')
A(f'<rect x="{camx-34}" y="{ry+24}" width="68" height="36" rx="7" fill="#cfd3d8" stroke="#8f959e" stroke-width="1.5"/>')
A(f'<circle cx="{camx+36}" cy="{ry+42}" r="11" fill="#0b0c0f" stroke="#777" stroke-width="2"/>')
A(f'<circle cx="{camx+36}" cy="{ry+42}" r="4" fill="#2a2f3a"/>')
dot(camx - 22, ry + 34, r=3.2, col="white")
A(f'<path d="M{camx-120},{ry+70} l 14,-6 l 0,12 z" fill="{DIM}"/>')
A(f'<path d="M{camx+140},{ry+70} l -14,-6 l 0,12 z" fill="{DIM}"/>')
A(f'<line x1="{camx-106}" y1="{ry+70}" x2="{camx+126}" y2="{ry+70}" stroke="{DIM}" stroke-width="1" stroke-dasharray="3,3"/>')
A(f'<text x="{cx+20}" y="{ry+100}" fill="{WHITE}" font-size="12" font-weight="bold">정비 카메라 · 흰 점검등</text>')
A(f'<text x="{cx+20}" y="{ry+118}" fill="{GREY}" font-size="10.5">레일을 타고 다가가고 물러나고 갸웃거린다. 거리와 초점이 두 번째 표정이다.</text>')
# arm
base = (cx + 40, cy + 290)
pts = [base, (cx + 120, cy + 250), (cx + 210, cy + 282), (cx + 275, cy + 262)]
for (p, q) in zip(pts, pts[1:]):
    A(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="#aeb3ba" stroke-width="7" stroke-linecap="round"/>')
for p in pts[1:3]:
    A(f'<circle cx="{p[0]}" cy="{p[1]}" r="7" fill="#6b7280" stroke="#3a3f48" stroke-width="1.5"/>')
    dot(p[0], p[1] - 11, r=2.4, col="white")
A(f'<rect x="{base[0]-10}" y="{base[1]-8}" width="20" height="16" rx="3" fill="#6b7280"/>')
e = pts[-1]
A(f'<path d="M{e[0]},{e[1]} l 16,-8 M{e[0]},{e[1]} l 16,8" stroke="#aeb3ba" stroke-width="5" stroke-linecap="round" fill="none"/>')
A(f'<text x="{cx+20}" y="{cy+330}" fill="{WHITE}" font-size="12" font-weight="bold">정비 암 · 관절 표시등</text>')
A(f'<text x="{cx+20}" y="{cy+348}" fill="{GREY}" font-size="10.5">관절등을 끄면 암은 그 자세로 있는다. 새싹을 받칠 때, 랙을 물 때.</text>')
# takeover inset
ix, iy = cx + 20, cy + 380
A(f'<clipPath id="insetclip"><rect x="{ix}" y="{iy}" width="{cw-40}" height="118" rx="10"/></clipPath>')
A(f'<rect x="{ix}" y="{iy}" width="{cw-40}" height="118" rx="10" fill="#111317" stroke="#2c3038" stroke-width="1"/>')
A(f'<ellipse cx="{ix+cw-40}" cy="{iy+59}" rx="120" ry="80" fill="url(#halo)" clip-path="url(#insetclip)"/>')
A(f'<rect x="{ix+cw-40-60}" y="{iy+18}" width="60" height="82" rx="8" fill="#b8271b" fill-opacity="0.9"/>')
A(f'<rect x="{ix+10}" y="{iy+14}" width="{cw-60}" height="4" rx="2" fill="#4a505b"/>')
sx = ix + 44
A(f'<line x1="{sx}" y1="{iy+18}" x2="{sx}" y2="{iy+30}" stroke="#8d8d88" stroke-width="2"/>')
A(f'<rect x="{sx-20}" y="{iy+30}" width="40" height="22" rx="5" fill="#cfd3d8" stroke="#8f959e" stroke-width="1"/>')
dot(sx - 12, iy + 37, r=3.2, col="white")
A(f'<text x="{ix+12}" y="{iy+76}" fill="{WHITE}" font-size="11.5" font-weight="bold">장악 중 · 2508~2513</text>')
A(f'<text x="{ix+12}" y="{iy+93}" fill="{GREY}" font-size="10.5">표시등이 덮개 빛에 묻히면 구석으로 물러난 카메라의</text>')
A(f'<text x="{ix+12}" y="{iy+108}" fill="{GREY}" font-size="10.5">흰 점검등이 1초에 한 번 깜빡인다. 맥박이 눈으로 옮겨 간다.</text>')

# caption
A(f'<text x="30" y="{H-48}" fill="{GREY}" font-size="12">표정은 셋뿐이다. 점의 속도, 카메라의 거리, 암의 관절등. 1호는 글자로 말하지 않고 벽의 큰 스피커로 말한다.</text>')
A(f'<text x="30" y="{H-28}" fill="{GREY}" font-size="12">그래서 레드의 붉은색이 패널을 다 덮어도 1호는 카메라 하나로 끝까지 얼굴이 있고, 2513일에 점이 다시 깜빡이면 관객은 1호가 돌아온 것을 안다.</text>')
A('</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT)
