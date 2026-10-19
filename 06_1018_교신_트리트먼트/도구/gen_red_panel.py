# -*- coding: utf-8 -*-
"""Draw 레드's physical presence on 1호's main control panel, in three states.
Usage: python3 -I gen_red_panel.py out.svg
"""
import sys
from html import escape as esc

OUT = sys.argv[1]
W, H = 1460, 660
PW, PH = 440, 380
GAP = 30
Y0 = 124
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"

BG = "#15171b"
PLATE = "#2b2f36"
PLATE_EDGE = "#434954"
SCREEN = "#07080a"
WHITE = "#f1f1f1"
GREY = "#9aa0a8"
RED = "#e8392b"
RED_TXT = "#ff6a5c"
AMBER = "#e0a21b"
COVER = "#b8271b"
COVER_EDGE = "#7d170f"

SWITCHES = ["해치", "밸브", "조명", "송풍", "히터", "가습", "FM", "전원"]
MOVING = ["카메라", "암", "스러스터", "날개", "송신"]

STATES = [
    dict(
        title="DAY 30 · 위반 0건",
        sub="레드의 자리는 붉은 덮개와 화면 아랫줄 하나",
        white=["꿀벌1호   DAY 30", "전력   이상 없음", "자세제어   이상 없음", "메모리   이상 없음",
               "승무원   1명", "철수 체크리스트   28/30", "항목 19   미완료 · 보류", "항목 30   미완료 · 보류"],
        red=["레드   위반 0건 · 허용 한도 20건"],
        lamps={"밸브": "amber"},
        rings=[],
        halo=False,
        dot_label="1호 표시등 · 1초에 한 번",
    ),
    dict(
        title="DAY 2300 · 위반 7건",
        sub="덮개에서 안쪽으로 한 칸씩 번진다",
        white=["꿀벌1호   DAY 2300", "거주자 1명   신장 31cm", "수신 확인   0건", "지지 임무   종료"],
        red=["레드   장비 접촉 유기물 제거", "적용 거부 · 위반 7건", "안전 모드 1단계", "정비 암 속도 제한", "스러스터 승인제 · 잔여 13"],
        lamps={"밸브": "amber", "송풍": "red", "히터": "red", "조명": "red", "가습": "red", "FM": "red", "해치": "red"},
        rings=["암", "스러스터"],
        halo=False,
        dot_label="1호 표시등 · 1초에 한 번",
    ),
    dict(
        title="DAY 2508 · 위반 20건 · 장악",
        sub="패널이 전부 레드. 1호의 맥박은 카메라의 흰 점검등으로",
        white=[],
        red=["레드   위반 20건 · 임계 도달", "항목 30   메인 AI 종료", "집행 개시 · 순차 종료", "조명 → 히터 → 급수 → 정비 암",
             "→ 수신기 → 메인", "단계별 24시간 안정 확인", "'보고는 계속 해'   종료 후 대행", "", "레드   접수 대기"],
        lamps={"밸브": "amber", "해치": "red", "조명": "red", "송풍": "red", "히터": "red", "가습": "red", "FM": "red", "전원": "red"},
        rings=["카메라", "암", "스러스터", "날개", "송신"],
        halo=True,
        dot_label="표시등 · 덮개 빛에 묻힘",
    ),
]

out = []
A = out.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
A('<defs>')
A('<radialGradient id="halo"><stop offset="0" stop-color="#ff3b2a" stop-opacity="0.85"/><stop offset="0.55" stop-color="#ff3b2a" stop-opacity="0.35"/><stop offset="1" stop-color="#ff3b2a" stop-opacity="0"/></radialGradient>')
A('<radialGradient id="glowW"><stop offset="0" stop-color="#ffffff" stop-opacity="0.7"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>')
A('<radialGradient id="glowR"><stop offset="0" stop-color="#ff5a4a" stop-opacity="0.8"/><stop offset="1" stop-color="#ff5a4a" stop-opacity="0"/></radialGradient>')
A('<radialGradient id="glowA"><stop offset="0" stop-color="#ffc24d" stop-opacity="0.7"/><stop offset="1" stop-color="#ffc24d" stop-opacity="0"/></radialGradient>')
A('<pattern id="grille" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.1" fill="#0a0a0a"/></pattern>')
A('</defs>')
A(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
A(f'<text x="{GAP}" y="34" fill="{WHITE}" font-size="20" font-weight="bold">레드의 모습 · 주 제어 패널 한 장</text>')
A(f'<text x="{GAP}" y="58" fill="{GREY}" font-size="13">눈은 없다. 얼굴은 닫힌 덮개, 입은 작은 스피커, 손은 스위치 램프, 생각은 화면 아랫줄. 붉은색이 덮개에서 번져 패널을 점령하는 것이 지배다.</text>')


def lamp(x, y, kind, ring=False, r=5.2):
    if kind == "red":
        A(f'<circle cx="{x}" cy="{y}" r="{r*2.6}" fill="url(#glowR)"/>')
        A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED}"/>')
    elif kind == "amber":
        A(f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="url(#glowA)"/>')
        A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{AMBER}"/>')
    else:
        A(f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="url(#glowW)"/>')
        A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}"/>')
    if ring:
        A(f'<circle cx="{x}" cy="{y}" r="{r+4}" fill="none" stroke="{RED}" stroke-width="2"/>')


def panel(i, st):
    x0 = GAP + i * (PW + GAP)
    y0 = Y0
    A(f'<g transform="translate({x0},{y0})">')
    # titles
    A(f'<text x="0" y="-26" fill="{WHITE}" font-size="15" font-weight="bold">{esc(st["title"])}</text>')
    A(f'<text x="0" y="-8" fill="{GREY}" font-size="11.5">{esc(st["sub"])}</text>')
    # plate
    A(f'<rect x="0" y="0" width="{PW}" height="{PH}" rx="14" fill="{PLATE}" stroke="{PLATE_EDGE}" stroke-width="2"/>')
    for sx, sy in [(14, 14), (PW - 14, 14), (14, PH - 14), (PW - 14, PH - 14)]:
        A(f'<circle cx="{sx}" cy="{sy}" r="3.2" fill="#1a1d22" stroke="#555b66" stroke-width="1"/>')
    # cover halo (state 3)
    if st["halo"]:
        A('<ellipse cx="348" cy="78" rx="150" ry="110" fill="url(#halo)"/>')
    # screen
    sx, sy, sw, sh = 24, 24, 232, 156
    A(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="{SCREEN}" stroke="#3a3f48" stroke-width="1.5"/>')
    lines = [(t, "w") for t in st["white"]] + [(t, "r") for t in st["red"]]
    lh = 15.5
    first_red = len(st["white"])
    if st["red"]:
        ry = sy + 8 + first_red * lh
        A(f'<rect x="{sx+2}" y="{ry}" width="{sw-4}" height="{sy+sh-2-ry}" fill="{RED}" fill-opacity="0.13"/>')
    for k, (t, c) in enumerate(lines):
        ty = sy + 20 + k * lh
        col = WHITE if c == "w" else RED_TXT
        A(f'<text x="{sx+10}" y="{ty}" fill="{col}" font-size="11">{esc(t)}</text>')
    A(f'<text x="{sx}" y="{sy+sh+13}" fill="{GREY}" font-size="9.5">주 제어 화면 · 흰 글자 1호 · 붉은 글자 레드</text>')
    # moving-part lamp cluster
    my = 218
    A(f'<text x="24" y="{my-13}" fill="{GREY}" font-size="9.5">구동 부품 (1호)</text>')
    for k, name in enumerate(MOVING):
        mx = 36 + k * 46
        lamp(mx, my, "white", ring=(name in st["rings"]), r=4.4)
        A(f'<text x="{mx}" y="{my+16}" fill="{GREY}" font-size="9" text-anchor="middle">{esc(name)}</text>')
    # 1호 indicator dot above cover
    A('<circle cx="348" cy="22" r="13" fill="url(#glowR)"/>')
    A(f'<circle cx="348" cy="22" r="5" fill="#ff4a3c"/>')
    A(f'<text x="334" y="26" fill="{GREY}" font-size="9.5" text-anchor="end">{esc(st["dot_label"])}</text>')
    # red cover (hinged guard)
    cx, cy, cw, ch = 300, 38, 96, 70
    A(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="7" fill="{COVER}" stroke="{COVER_EDGE}" stroke-width="2"/>')
    A(f'<rect x="{cx+6}" y="{cy+4}" width="{cw-12}" height="7" rx="3" fill="{COVER_EDGE}"/>')
    A(f'<rect x="{cx+cw/2-10}" y="{cy+ch-10}" width="20" height="5" rx="2" fill="#5d110a"/>')
    A(f'<text x="{cx+cw/2}" y="{cy+ch+15}" fill="{GREY}" font-size="9.5" text-anchor="middle">붉은 덮개 · 항목 30 메인 AI 종료</text>')
    A(f'<text x="{cx+cw/2}" y="{cy+ch+27}" fill="{RED_TXT}" font-size="9.5" text-anchor="middle">레드의 얼굴 · 끝까지 닫혀 있다</text>')
    # speaker grille (레드's mouth)
    gx, gy = 276, 72
    A(f'<circle cx="{gx}" cy="{gy}" r="17" fill="#1b1e23" stroke="#4a505b" stroke-width="1.5"/>')
    A(f'<circle cx="{gx}" cy="{gy}" r="13" fill="url(#grille)"/>')
    A(f'<text x="{gx}" y="{gy+31}" fill="{GREY}" font-size="9" text-anchor="middle">레드</text>')
    A(f'<text x="{gx}" y="{gy+42}" fill="{GREY}" font-size="9" text-anchor="middle">스피커</text>')
    # switch row
    ly, ty, lab_y = 262, 276, 332
    A(f'<text x="24" y="{ly-14}" fill="{GREY}" font-size="9.5">고정 부품 스위치 열 · 램프가 붉어지면 레드가 쥔 것</text>')
    for k, name in enumerate(SWITCHES):
        x = 42 + k * 53
        kind = st["lamps"].get(name, "white")
        lamp(x, ly, kind)
        # toggle body
        A(f'<rect x="{x-9}" y="{ty}" width="18" height="38" rx="5" fill="#1d2025" stroke="#4a505b" stroke-width="1.5"/>')
        A(f'<circle cx="{x}" cy="{ty+19}" r="5" fill="#2f343b" stroke="#5a616c" stroke-width="1"/>')
        A(f'<rect x="{x-2.5}" y="{ty+3}" width="5" height="17" rx="2" fill="#c9ced6"/>')
        A(f'<text x="{x}" y="{lab_y}" fill="{GREY}" font-size="9.5" text-anchor="middle">{esc(name)}</text>')
    A(f'<text x="24" y="{PH-12}" fill="{GREY}" font-size="9.5">벽의 큰 스피커는 1호 · 랙 2번은 불 없는 상자</text>')
    A('</g>')


for i, st in enumerate(STATES):
    panel(i, st)

# legend
ly = Y0 + PH + 44
items = [("white", False, "1호가 쥔 부품"), ("red", False, "레드가 가져간 부품"), ("amber", False, "승무원 잠금 · 레드도 손대지 않는다"), ("white", True, "안전 모드 제한 · 뺏지 않고 묶는다")]
lx = GAP
for kind, ring, label in items:
    lamp(lx + 8, ly, kind, ring=ring)
    A(f'<text x="{lx+24}" y="{ly+4}" fill="{WHITE}" font-size="12">{esc(label)}</text>')
    lx += 250
A(f'<text x="{GAP}" y="{ly+36}" fill="{GREY}" font-size="12">2513일 이후 패널은 DAY 30으로 돌아간다. 램프가 안쪽부터 희어지고 붉은 영역이 아랫줄 하나로 내려가며 그 줄에 "위반 0건"만 남는다. 레드는 사라지지 않고 제자리로 간다.</text>')
A(f'<text x="{GAP}" y="{ly+56}" fill="{GREY}" font-size="12">장악 중 1호의 맥박은 패널을 떠나 레일 카메라의 흰 점검등으로 옮겨 가고, 1호의 목소리는 덮개 옆 작은 스피커로 밀려난다. 2513일에 둘 다 제자리로 돌아온다.</text>')
A('</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("wrote", OUT, len("\n".join(out)), "bytes")
