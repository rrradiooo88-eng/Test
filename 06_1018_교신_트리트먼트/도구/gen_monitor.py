# -*- coding: utf-8 -*-
"""17인치 모니터 목업: 1안(그리는 1호, 찍는 레드) / 2안(해준이 그려 준 둘) × DAY 30 / 2508 / 2513
Usage: python3 -I gen_monitor.py out.svg
"""
import sys, math
from html import escape as esc

OUT = sys.argv[1]
W, H = 1460, 880
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
BG = "#15171b"; BEZEL = "#2a2d33"; BEZEL_E = "#474c56"; SCR = "#0b0e12"
WHITE = "#eef0f2"; GREY = "#9aa0a8"; DIM = "#596069"; RED = "#ff4a3c"; RED_T = "#ff6a5c"
GREEN = "#6fbf73"; YEL = "#f3e3a0"; CARD = "#e9e8e2"; INK = "#23262b"

o = []
A = o.append


def text(x, y, s, size=10, fill=WHITE, anchor="start", bold=False, rot=0, opacity=1.0):
    w = ' font-weight="bold"' if bold else ''
    r = f' transform="rotate({rot} {x} {y})"' if rot else ''
    op = f' opacity="{opacity}"' if opacity < 1 else ''
    A(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}{r}{op}>{esc(s)}</text>')


def monitor(x, y):
    """returns screen origin (sx, sy) and size (sw, sh)"""
    A(f'<rect x="{x}" y="{y}" width="440" height="280" rx="10" fill="{BEZEL}" stroke="{BEZEL_E}" stroke-width="1.5"/>')
    A(f'<rect x="{x+10}" y="{y+10}" width="420" height="258" rx="3" fill="{SCR}"/>')
    A(f'<circle cx="{x+220}" cy="{y+274}" r="1.8" fill="#6b7280"/>')
    return x + 10, y + 10, 420, 258


def topbar(sx, sy, sw, label):
    A(f'<rect x="{sx}" y="{sy}" width="{sw}" height="16" fill="#141920"/>')
    text(sx + 8, sy + 11.5, label, 8.5, GREY)


def graph(x, y, w, h, label="발전량", beats=True):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    text(x + 6, y + 11, label, 8, GREY)
    pts = []
    n = 60
    for i in range(n + 1):
        px = x + 8 + (w - 16) * i / n
        base = y + h * 0.62 + 3 * math.sin(i / 4.0)
        bump = 0
        if beats and i % 6 in (1, 2):
            bump = -h * 0.22
        pts.append(f"{px:.1f},{base + bump:.1f}")
    A(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#8ec5ff" stroke-width="1.3"/>')


def checklist(x, y, items, w=170):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{14 + 13*len(items)}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    text(x + 6, y + 11, "철수 체크리스트 30항목", 8, GREY)
    for i, (num, name, done) in enumerate(items):
        yy = y + 24 + i * 13
        A(f'<rect x="{x+7}" y="{yy-7}" width="7" height="7" rx="1" fill="{"#8ec5ff" if done else "none"}" stroke="#8ec5ff" stroke-width="0.8"/>')
        text(x + 19, yy, f"{num}  {name}", 8, WHITE if done else GREY)


def redbar(sx, sy, sw, sh, label, h=14):
    A(f'<rect x="{sx}" y="{sy+sh-h}" width="{sw}" height="{h}" fill="{RED}" fill-opacity="0.22"/>')
    A(f'<rect x="{sx}" y="{sy+sh-h}" width="{sw}" height="1" fill="{RED}"/>')
    text(sx + 8, sy + sh - 4, label, 8, RED_T)


def seedling(x, y, s=1.0, fruit=False, leaves=4):
    A(f'<g transform="translate({x},{y}) scale({s})">')
    A(f'<path d="M0,0 C 2,-18 -3,-34 1,-52" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round"/>')
    for i in range(leaves):
        ly = -14 - i * 11
        side = 1 if i % 2 == 0 else -1
        A(f'<ellipse cx="{side*9}" cy="{ly}" rx="10" ry="4.5" fill="{GREEN}" transform="rotate({-28*side} {side*9} {ly})"/>')
    if fruit:
        A(f'<circle cx="7" cy="-46" r="3.6" fill="#e0543f"/>')
    A('</g>')


def photo_box(x, y, w, h, fruit=False, with_bee=False):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#0b0e12"/>')
    seedling(x + w * (0.35 if with_bee else 0.5), y + h - 6, s=0.78, fruit=fruit)
    if with_bee:
        bee_doodle(x + w * 0.74, y + h * 0.5, 0.55)


def stamp(cx, cy, label, color, rot=-12, w=96, h=22):
    A(f'<g transform="rotate({rot} {cx} {cy})" opacity="0.92">')
    A(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="3" fill="none" stroke="{color}" stroke-width="2"/>')
    text(cx, cy + 4, label, 10, color, anchor="middle", bold=True)
    A('</g>')


def card(x, y, w=200, h=118, approved=False, fruit=False, with_bee=False):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{CARD}"/>')
    photo_box(x + 8, y + 8, 78, h - 16, fruit=fruit, with_bee=with_bee)
    tx = x + 94
    text(tx, y + 22, "거주자 등록 카드", 9, INK, bold=True)
    text(tx, y + 38, "거주자 1", 10, INK)
    text(tx, y + 52, "등록  Day 2204", 8, "#555a63")
    text(tx, y + 64, "천도복숭아 · 승무원 잔류물", 8, "#555a63")
    text(tx, y + 76, "결실 1" if fruit else "개화 7", 8, "#555a63")
    stamp(x + w - 64, y + h - 28, "승무원 미승인", RED, rot=-10, w=92, h=20)
    if approved:
        stamp(x + w - 50, y + h - 54, "승인 · 항목 31", "#2f8f4a", rot=7, w=92, h=20)


def bee_doodle(x, y, s=1.0):
    """해준의 못 그린 낙서 벌 (삐뚤삐뚤)"""
    A(f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{YEL}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">')
    A('<path d="M-20,2 C-22,-10 -8,-16 4,-13 C 18,-10 24,0 18,9 C 12,17 -4,18 -14,12 C-20,9 -21,6 -20,2 Z"/>')
    A('<path d="M-8,-12 L-10,13 M0,-14 L-1,15 M8,-11 L7,13"/>')
    A('<path d="M-6,-13 C-14,-30 4,-34 2,-16"/>')
    A('<path d="M4,-13 C 6,-32 24,-28 12,-12"/>')
    A('<path d="M18,6 L27,9"/>')
    A('<path d="M-19,-3 C-26,-8 -24,-15 -28,-18 M-17,-6 C-20,-13 -16,-17 -19,-22"/>')
    A('<circle cx="-13" cy="-3" r="1.6" fill="#f3e3a0" stroke="none"/>')
    A('</g>')


def red_doodle(x, y, size=24, slash=True):
    """해준이 그린 성난 붉은 네모 (크기만 변한다)"""
    k = size / 24.0
    A(f'<g transform="translate({x},{y}) scale({k})" fill="{RED}" fill-opacity="0.16" stroke="{RED}" stroke-width="{3/k if k>1 else 3}" stroke-linecap="round" stroke-linejoin="round">')
    A('<path d="M-12,-11 C-6,-13 5,-12 12,-12 C13,-5 12,4 12,12 C4,13 -5,12 -12,12 C-13,5 -11,-4 -12,-11 Z"/>')
    if slash:
        A(f'<path d="M-9,-8 C-2,-1 3,4 9,9" fill="none"/>')
    A('</g>')


def bee_precise(x, y, s=1.0, bent=True):
    """1호가 그린 정확한 벌. 오른쪽 날개가 꺾여 있다."""
    A(f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="#d9dde2" stroke-width="1.3">')
    A('<ellipse cx="0" cy="0" rx="18" ry="10"/>')
    for sx_ in (-8, 0, 8):
        A(f'<line x1="{sx_}" y1="-9.6" x2="{sx_}" y2="9.6"/>')
    A('<ellipse cx="-9" cy="-16" rx="7" ry="12" transform="rotate(-25 -9 -16)"/>')
    if bent:
        A('<path d="M3,-9 L10,-20 L22,-16" />')
        A('<path d="M10,-20 L7,-27" stroke-dasharray="2,2"/>')
    else:
        A('<ellipse cx="9" cy="-16" rx="7" ry="12" transform="rotate(25 9 -16)"/>')
    A('<path d="M18,0 L25,2"/>')
    A('<path d="M-17,-4 L-24,-12 M-15,-7 L-19,-16"/>')
    A('</g>')


def ledger(sx, sy, lines, size=10, start=None, color=RED_T, lh=15):
    y = start if start is not None else sy + 34
    for s in lines:
        text(sx + 14, y, s, size, color)
        y += lh


def note(x, y, s, w=None):
    text(x, y, s, 9.5, GREY)


# ------------------------------------------------------------------ header
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
A(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
text(30, 34, "17인치 모니터 · 두 안", 20, WHITE, bold=True)
text(30, 58, "패널 한가운데 모니터. Day 30에는 해준이 보고, 그 뒤 7년은 1호가 아무도 안 보는 화면에 계속 그린다. 레드는 처음엔 아주 작은 지분으로 있다가 화면을 점령한다.", 13, GREY)

cols = [30, 510, 990]
col_titles = ["DAY 30 · 철수", "DAY 2508 · 장악", "DAY 2513 · 수신 확인"]
row_y = [134, 520]
row_titles = ["1안 · 그리는 1호, 찍는 레드  (추천)", "2안 · 해준이 그려 준 둘"]
for r, ry in enumerate(row_y):
    text(30, ry - 14, row_titles[r], 15, WHITE, bold=True)
for c, cx in enumerate(cols):
    text(cx, 86, col_titles[c], 12, GREY, bold=True)

# ------------------------------------------------------------------ 1안
# DAY 30
sx, sy, sw, sh = monitor(cols[0], row_y[0])
topbar(sx, sy, sw, "꿀벌1호 · DAY 30 · 철수 · 승무원 1명")
graph(sx + 10, sy + 26, 200, 92)
checklist(sx + 222, sy + 26, [("11", "식수 밸브 잠금", True), ("12", "폐기물 봉투 밀봉", False), ("19", "오락 시스템 종료", False), ("20", "식단 기록 마감", False), ("30", "메인 AI 종료", False)], w=186)
A(f'<rect x="{sx+10}" y="{sy+128}" width="398" height="96" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
text(sx + 16, sy + 139, "기체 도면 · 귀환선 도킹 중", 8, GREY)
A(f'<rect x="{sx+120}" y="{sy+160}" width="170" height="44" rx="20" fill="none" stroke="#8ec5ff" stroke-width="1.2"/>')
A(f'<rect x="{sx+60}" y="{sy+172}" width="56" height="20" rx="2" fill="none" stroke="#c9a94a" stroke-width="1"/>')
A(f'<rect x="{sx+294}" y="{sy+172}" width="56" height="20" rx="2" fill="none" stroke="#c9a94a" stroke-width="1"/>')
A(f'<rect x="{sx+96}" y="{sy+174}" width="24" height="16" rx="3" fill="none" stroke="#8ec5ff" stroke-width="1"/>')
redbar(sx, sy, sw, sh, "감사 · 위반 0 · 허용 20")
note(cols[0], row_y[0] + 296, "레드의 지분은 맨 아래 붉은 띠 한 줄. 해준은 한 번도 안 본다.")

# DAY 2508
sx, sy, sw, sh = monitor(cols[1], row_y[0])
A(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{RED}" fill-opacity="0.2"/>')
topbar(sx, sy, sw, "감사 · DAY 2508 · 위반 20 · 임계 도달")
ledger(sx, sy, ["항목 30   메인 AI 종료", "집행 개시 · 순차 종료", "조명 → 히터 → 급수 → 정비 암", "→ 수신기 → 메인", "단계별 24시간 안정 확인", "'보고는 계속 해'   종료 후 대행", "잔여 유예   0"], size=11, lh=17)
# 1호 thumbnail
tx, ty, tw, th = sx + 290, sy + 150, 118, 96
A(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="3" fill="#0b0e12" stroke="#8ec5ff" stroke-width="1"/>')
text(tx + 6, ty + 11, "정비 카메라 · 거주자", 7.5, "#8ec5ff")
seedling(tx + tw / 2, ty + th - 8, s=0.85, leaves=5)
note(cols[1], row_y[0] + 296, "붉은색이 화면 전체. 1호의 작업창은 구석 썸네일이 되고 그 안에 진짜 새싹만 나온다.")

# DAY 2513
sx, sy, sw, sh = monitor(cols[2], row_y[0])
topbar(sx, sy, sw, "꿀벌1호 · DAY 2513 · 수신 확인 1건")
card(sx + 22, sy + 36, w=240, h=130, approved=True, fruit=True)
A(f'<rect x="{sx+278}" y="{sy+36}" width="130" height="130" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
text(sx + 284, sy + 48, "일일보고 · Day 2513", 8, GREY)
for i, s in enumerate(["전력  이상 없음", "패널 1매 손상", "거주자 1명  양호", "결실 1", "수신자  승무원 1명", "수신 확인  1건"]):
    text(sx + 284, sy + 66 + i * 14, s, 8.5, WHITE if i == 5 else GREY, bold=(i == 5))
text(sx + 22, sy + 190, "미확인 돌기 1개 · 대조 · 결실", 9, "#8ec5ff")
redbar(sx, sy, sw, sh, "감사 · 위반 0")
note(cols[2], row_y[0] + 296, "등록 카드에 '승인 · 항목 31'이 찍힌다. 띠는 Day 30 자리로 돌아가 '위반 0'.")

# ------------------------------------------------------------------ 2안
# DAY 30
sx, sy, sw, sh = monitor(cols[0], row_y[1])
topbar(sx, sy, sw, "꿀벌1호 · DAY 30 · 철수 · 승무원 1명")
graph(sx + 10, sy + 26, 200, 92)
checklist(sx + 222, sy + 26, [("11", "식수 밸브 잠금", True), ("12", "폐기물 봉투 밀봉", False), ("19", "오락 시스템 종료", False), ("20", "식단 기록 마감", False), ("30", "메인 AI 종료", False)], w=186)
A(f'<rect x="{sx+10}" y="{sy+128}" width="398" height="118" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
text(sx + 16, sy + 139, "메모 · 터치 낙서", 8, GREY)
bee_doodle(sx + 70, sy + 190, 1.1)
text(sx + 112, sy + 186, "너 꿀벌이잖아", 9, YEL, opacity=0.85)
red_doodle(sx + 372, sy + 214, 24)
text(sx + 372, sy + 240, "레드 · 위반 0", 7.5, RED_T, anchor="middle")
note(cols[0], row_y[1] + 296, "해준이 심심해서 그린 벌과 성난 붉은 네모. 1호가 둘을 아이콘으로 등록한다. 승무원이 그려서 둘 다 못 바꾼다.")

# DAY 2508
sx, sy, sw, sh = monitor(cols[1], row_y[1])
red_doodle(sx + sw / 2, sy + sh / 2 + 6, 236)
topbar(sx, sy, sw, "감사 · DAY 2508 · 위반 20 · 임계 도달")
bee_doodle(sx + 22, sy + 36, 0.42)
tx, ty, tw, th = sx + 300, sy + 150, 108, 96
A(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="3" fill="#0b0e12" stroke="#8ec5ff" stroke-width="1"/>')
text(tx + 6, ty + 11, "1호 작업창", 7.5, "#8ec5ff")
bee_precise(tx + tw / 2, ty + 58, 1.0, bent=True)
ledger(sx + 100, sy, ["항목 30  집행 개시", "순차 종료 · 24시간 확인"], size=10, start=sy + sh - 40, lh=14)
note(cols[1], row_y[1] + 296, "해준의 네모가 화면만큼 커졌다. 같은 낙서, 크기만 다르다. 1호는 제 작업창에 날개 꺾인 벌을 새로 그린다.")

# DAY 2513
sx, sy, sw, sh = monitor(cols[2], row_y[1])
topbar(sx, sy, sw, "꿀벌1호 · DAY 2513 · 수신 확인 1건")
bee_doodle(sx + 36, sy + 52, 0.75)
card(sx + 70, sy + 60, w=250, h=130, approved=True, fruit=True, with_bee=True)
text(sx + 70, sy + 214, "거주자 1 · 승인자  승무원 1명 · 완료 조건  '그때'", 8.5, "#8ec5ff")
red_doodle(sx + 372, sy + 214, 24)
text(sx + 372, sy + 240, "레드 · 위반 0", 7.5, RED_T, anchor="middle")
note(cols[2], row_y[1] + 296, "네모는 구석의 제 크기로 돌아가고, 등록 카드에 떡잎 사진과 해준의 벌이 나란히 붙는다. 해준은 이 화면을 못 본다.")

# ------------------------------------------------------------------ footer
text(30, H - 44, "1안은 1호가 자기 얼굴을 끝까지 안 그린다. 관객이 보는 건 1호가 그리기로 한 것들이다. 해준의 늙은 얼굴, 등록 카드, 제주까지의 선, 레드가 시킨 추락 시뮬레이션과 그걸 끄고 비춘 진짜 새싹.", 12, GREY)
text(30, H - 24, "2안은 아이콘이 해준의 손이라 이입이 바로 생긴다. 값은 톤이다. 낙서는 못 그려야 하고 1호의 그림은 정확해야 하고 둘이 한 화면에서 섞이면 안 된다. 절충은 1안에 레드의 네모만 가져오는 것.", 12, GREY)
A('</svg>')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT)
