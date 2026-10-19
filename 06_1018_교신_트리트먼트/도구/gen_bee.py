# -*- coding: utf-8 -*-
"""벌과 수위: 여섯 장면 시트 + 개념도.
Usage: python3 -I gen_bee.py scenes.svg concept.svg
"""
import sys, math
from html import escape as esc

SCENES, CONCEPT = sys.argv[1], sys.argv[2]
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
BG = "#15171b"; BEZEL = "#2a2d33"; BEZEL_E = "#474c56"; SCR = "#0b0e12"
WHITE = "#eef0f2"; GREY = "#9aa0a8"; DIM = "#596069"; RED = "#ff4a3c"; RED_T = "#ff7a6c"
GREEN = "#6fbf73"; YEL = "#f3e3a0"; CARD = "#e9e8e2"; INK = "#23262b"; BLUE = "#8ec5ff"


class SVG:
    def __init__(self, w, h):
        self.w, self.h, self.o = w, h, []
        self.o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">')
        self.o.append(f'<rect width="{w}" height="{h}" fill="{BG}"/>')

    def A(self, s):
        self.o.append(s)

    def text(self, x, y, s, size=10, fill=WHITE, anchor="start", bold=False, rot=0, opacity=1.0):
        w = ' font-weight="bold"' if bold else ''
        r = f' transform="rotate({rot} {x} {y})"' if rot else ''
        op = f' opacity="{opacity}"' if opacity < 1 else ''
        self.A(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}{r}{op}>{esc(s)}</text>')

    def save(self, path):
        self.o.append('</svg>')
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.o))
        print("wrote", path)


# ---------------------------------------------------------------- drawing helpers
def bee(S, x, y, s=1.0, opacity=1.0, color=YEL):
    """해준의 못 그린 낙서 벌. 선은 어디서나 같다."""
    S.A(f'<g transform="translate({x},{y}) scale({s})" opacity="{opacity}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">')
    S.A('<path d="M-20,2 C-22,-10 -8,-16 4,-13 C 18,-10 24,0 18,9 C 12,17 -4,18 -14,12 C-20,9 -21,6 -20,2 Z"/>')
    S.A('<path d="M-8,-12 L-10,13 M0,-14 L-1,15 M8,-11 L7,13"/>')
    S.A('<path d="M-6,-13 C-14,-30 4,-34 2,-16"/>')
    S.A('<path d="M4,-13 C 6,-32 24,-28 12,-12"/>')
    S.A('<path d="M18,6 L27,9"/>')
    S.A('<path d="M-19,-3 C-26,-8 -24,-15 -28,-18 M-17,-6 C-20,-13 -16,-17 -19,-22"/>')
    S.A(f'<circle cx="-13" cy="-3" r="1.6" fill="{color}" stroke="none"/>')
    S.A('</g>')


def ghost_arrow(S, x1, y1, x2, y2):
    mx, my = (x1 + x2) / 2 + 18, (y1 + y2) / 2
    S.A(f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" fill="none" stroke="{YEL}" stroke-width="1" stroke-dasharray="3,4" opacity="0.5"/>')
    ang = math.atan2(y2 - my, x2 - mx)
    for d in (0.5, -0.5):
        ex = x2 - 7 * math.cos(ang + d); ey = y2 - 7 * math.sin(ang + d)
        S.A(f'<line x1="{x2}" y1="{y2}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{YEL}" stroke-width="1" opacity="0.5"/>')


def monitor(S, x, y):
    S.A(f'<rect x="{x}" y="{y}" width="440" height="280" rx="10" fill="{BEZEL}" stroke="{BEZEL_E}" stroke-width="1.5"/>')
    S.A(f'<rect x="{x+10}" y="{y+10}" width="420" height="258" rx="3" fill="{SCR}"/>')
    S.A(f'<circle cx="{x+220}" cy="{y+274}" r="1.8" fill="#6b7280"/>')
    return x + 10, y + 10, 420, 258


def topbar(S, sx, sy, sw, label):
    S.A(f'<rect x="{sx}" y="{sy}" width="{sw}" height="16" fill="#141920"/>')
    S.text(sx + 8, sy + 11.5, label, 8.5, GREY)


def level(S, sx, sy, sw, sh, pct, lines, opacity=0.28, label_first=True):
    """레드의 수위. pct 0~100 (내용 영역 16..sh 기준). 붉은색은 반투명."""
    top = sy + 16
    h = (sh - 16) * pct / 100.0
    ly = sy + sh - h
    if pct <= 0:
        ly = sy + sh - 14
        S.A(f'<rect x="{sx}" y="{ly}" width="{sw}" height="14" fill="{RED}" fill-opacity="{opacity}"/>')
        S.A(f'<rect x="{sx}" y="{ly}" width="{sw}" height="1.5" fill="{RED}"/>')
        if lines:
            S.text(sx + 8, sy + sh - 4, lines[0], 8, RED_T)
        return ly
    S.A(f'<rect x="{sx}" y="{ly}" width="{sw}" height="{sy+sh-ly}" fill="{RED}" fill-opacity="{opacity}"/>')
    S.A(f'<rect x="{sx}" y="{ly}" width="{sw}" height="1.5" fill="{RED}"/>')
    yy = ly + 18
    for s in lines:
        if yy > sy + sh - 6:
            break
        S.text(sx + 12, yy, s, 9.5, RED_T)
        yy += 14.5
    return ly


def graph(S, x, y, w, h, label="발전량"):
    S.A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    S.text(x + 6, y + 11, label, 8, GREY)
    pts = []
    n = 60
    for i in range(n + 1):
        px = x + 8 + (w - 16) * i / n
        base = y + h * 0.62 + 3 * math.sin(i / 4.0)
        bump = -h * 0.22 if i % 6 in (1, 2) else 0
        pts.append(f"{px:.1f},{base + bump:.1f}")
    S.A(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="1.3"/>')


def checklist(S, x, y, items, w=186):
    S.A(f'<rect x="{x}" y="{y}" width="{w}" height="{14 + 13*len(items)}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    S.text(x + 6, y + 11, "철수 체크리스트 30항목", 8, GREY)
    for i, (num, name, done) in enumerate(items):
        yy = y + 24 + i * 13
        S.A(f'<rect x="{x+7}" y="{yy-7}" width="7" height="7" rx="1" fill="{BLUE if done else "none"}" stroke="{BLUE}" stroke-width="0.8"/>')
        S.text(x + 19, yy, f"{num}  {name}", 8, WHITE if done else GREY)


def seedling(S, x, y, s=1.0, fruit=False, leaves=4):
    S.A(f'<g transform="translate({x},{y}) scale({s})">')
    S.A(f'<path d="M0,0 C 2,-18 -3,-34 1,-52" fill="none" stroke="{GREEN}" stroke-width="2.4" stroke-linecap="round"/>')
    for i in range(leaves):
        ly = -14 - i * 11
        side = 1 if i % 2 == 0 else -1
        S.A(f'<ellipse cx="{side*9}" cy="{ly}" rx="10" ry="4.5" fill="{GREEN}" transform="rotate({-28*side} {side*9} {ly})"/>')
    if fruit:
        S.A('<circle cx="7" cy="-46" r="3.6" fill="#e0543f"/>')
    S.A('</g>')


def stamp(S, cx, cy, label, color, rot=-12, w=96, h=22):
    S.A(f'<g transform="rotate({rot} {cx} {cy})" opacity="0.92">')
    S.A(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="3" fill="none" stroke="{color}" stroke-width="2"/>')
    S.text(cx, cy + 4, label, 10, color, anchor="middle", bold=True)
    S.A('</g>')


def card(S, x, y, w=240, h=130, approved=False, fruit=False, scale=1.0):
    S.A(f'<g transform="translate({x},{y}) scale({scale})">')
    S.A(f'<rect x="0" y="0" width="{w}" height="{h}" rx="5" fill="{CARD}"/>')
    S.A(f'<rect x="8" y="8" width="86" height="{h-16}" rx="3" fill="#0b0e12"/>')
    seedling(S, 8 + 43, 8 + (h - 16) - 6, s=0.78, fruit=fruit)
    tx = 104
    S.text(tx, 22, "거주자 등록 카드", 9, INK, bold=True)
    S.text(tx, 38, "거주자 1", 10, INK)
    S.text(tx, 52, "등록  Day 2204", 8, "#555a63")
    S.text(tx, 64, "천도복숭아 · 승무원 잔류물", 8, "#555a63")
    S.text(tx, 76, "결실 1" if fruit else "떡잎 2 · 본잎 2", 8, "#555a63")
    stamp(S, w - 64, h - 28, "승무원 미승인", RED, rot=-10, w=92, h=20)
    if approved:
        stamp(S, w - 50, h - 54, "승인 · 항목 31", "#2f8f4a", rot=7, w=92, h=20)
    S.A('</g>')


def face_render(S, x, y, w=96, h=96):
    S.A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    S.text(x + 6, y + 11, "승무원 · 추정 +6년", 7.5, GREY)
    cx, cy = x + w / 2, y + h / 2 + 8
    S.A(f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="27" fill="none" stroke="#c9ced6" stroke-width="1.2"/>')
    S.A(f'<path d="M{cx-22},{cy-10} C{cx-18},{cy-32} {cx+18},{cy-32} {cx+22},{cy-10}" fill="none" stroke="#c9ced6" stroke-width="1.2"/>')
    for dx in (-8, 8):
        S.A(f'<line x1="{cx+dx-4}" y1="{cy-4}" x2="{cx+dx+4}" y2="{cy-4}" stroke="#c9ced6" stroke-width="1.2"/>')
    S.A(f'<path d="M{cx-6},{cy+12} Q{cx},{cy+14} {cx+6},{cy+12}" fill="none" stroke="#c9ced6" stroke-width="1.2"/>')
    for i in range(5):
        S.A(f'<line x1="{cx-20+i*3}" y1="{cy-26}" x2="{cx-24+i*3}" y2="{cy-20}" stroke="#e8e8e8" stroke-width="0.8"/>')


def route_map(S, x, y, w, h):
    S.A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    S.text(x + 6, y + 11, "반사광 낙하 지점 · 제주", 7.5, GREY)
    cx, cy = x + w * 0.5, y + h * 0.62
    S.A(f'<circle cx="{cx}" cy="{cy}" r="{h*0.3}" fill="none" stroke="#3a4350" stroke-width="1"/>')
    S.A(f'<circle cx="{cx+h*0.12}" cy="{cy-h*0.1}" r="2.2" fill="{BLUE}"/>')
    S.A(f'<line x1="{x+w-14}" y1="{y+18}" x2="{cx+h*0.12}" y2="{cy-h*0.1}" stroke="{YEL}" stroke-width="1" stroke-dasharray="2,3"/>')
    S.text(cx + h * 0.12 + 5, cy - h * 0.1 + 3, "제주", 7, BLUE)


def growth(S, x, y, w, h):
    S.A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
    S.text(x + 6, y + 11, "거주자 · 신장 · 엽수 · 돌기 7", 7.5, GREY)
    pts = []
    for i in range(0, 31):
        px = x + 8 + (w - 16) * i / 30
        py = y + h - 8 - (h - 26) * (i / 30) ** 0.8
        pts.append(f"{px:.1f},{py:.1f}")
    S.A(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GREEN}" stroke-width="1.3"/>')


# ================================================================= 1) 여섯 장면
S = SVG(1460, 860)
S.text(30, 34, "벌과 수위 · 모니터 여섯 장면", 20, WHITE, bold=True)
S.text(30, 58, "해준이 나가며 그린 벌이 1호의 캐릭터가 된다. 선은 안 바뀌고 자리는 바뀐다. 레드는 밑에서부터 차오르는 반투명한 붉은 수위다. 위반 한 건에 한 칸, 스무 칸이면 끝.", 13, GREY)
cols = [30, 510, 990]; rows = [100, 460]
caps = []

# 1. DAY 30
sx, sy, sw, sh = monitor(S, cols[0], rows[0])
S.text(cols[0], rows[0] - 10, "DAY 30 · 낙서", 12, GREY, bold=True)
topbar(S, sx, sy, sw, "꿀벌1호 · DAY 30 · 철수 · 승무원 1명")
graph(S, sx + 10, sy + 26, 200, 84)
checklist(S, sx + 222, sy + 26, [("11", "식수 밸브 잠금", True), ("12", "폐기물 봉투 밀봉", True), ("19", "오락 시스템 종료", False), ("30", "메인 AI 종료", False)])
S.A(f'<rect x="{sx+10}" y="{sy+120}" width="398" height="112" rx="3" fill="#10151b" stroke="#232a33" stroke-width="1"/>')
S.text(sx + 16, sy + 131, "기체 도면", 8, GREY)
S.A(f'<rect x="{sx+150}" y="{sy+150}" width="150" height="40" rx="18" fill="none" stroke="{BLUE}" stroke-width="1.2"/>')
S.A(f'<rect x="{sx+96}" y="{sy+160}" width="50" height="20" rx="2" fill="none" stroke="#c9a94a" stroke-width="1"/>')
S.A(f'<rect x="{sx+304}" y="{sy+160}" width="50" height="20" rx="2" fill="none" stroke="#c9a94a" stroke-width="1"/>')
bee(S, sx + 300, sy + 205, 1.0)
level(S, sx, sy, sw, sh, 0, ["감사 · 위반 0 · 허용 20"])
caps.append((cols[0], rows[0] + 298, "나가기 직전 손가락 서너 획. 1호: \"메모 1건, 승무원 작성. 보관.\" 수위는 맨 아래 띠 한 줄."))

# 2. DAY 2204
sx, sy, sw, sh = monitor(S, cols[1], rows[0])
S.text(cols[1], rows[0] - 10, "DAY 2204 · 등록", 12, GREY, bold=True)
topbar(S, sx, sy, sw, "꿀벌1호 · DAY 2204 · 거주자 1명 등록")
card(S, sx + 60, sy + 56, w=240, h=130)
ghost = (sx + 300, sy + 205)
bee(S, *ghost, 1.0, opacity=0.22)
ghost_arrow(S, ghost[0] - 20, ghost[1] - 14, sx + 120, sy + 110)
bee(S, sx + 112, sy + 118, 0.85)
level(S, sx, sy, sw, sh, 15, ["정의 우회 · 위반 3 · 잔여 17"])
caps.append((cols[1], rows[0] + 298, "벌이 처음으로 자리를 옮긴다. 등록 카드의 사진 칸, 떡잎 옆으로. 수위 15."))

# 3. DAY 2480
sx, sy, sw, sh = monitor(S, cols[2], rows[0])
S.text(cols[2], rows[0] - 10, "DAY 2480 · 돌기 7개", 12, GREY, bold=True)
topbar(S, sx, sy, sw, "꿀벌1호 · DAY 2480 · 거주자 1명")
growth(S, sx + 10, sy + 24, 196, 86)
route_map(S, sx + 214, sy + 24, 194, 86)
ghost = (sx + 112, sy + 118)
bee(S, *ghost, 0.85, opacity=0.22)
ghost_arrow(S, ghost[0] + 20, ghost[1] - 10, sx + 190, sy + 70)
bee(S, sx + 205, sy + 66, 0.8)
level(S, sx, sy, sw, sh, 55, ["지시 미수신 지속 · 승무원 0명", "위반 누적 11 · 허용 20 · 잔여 9", "도달 시 항목 30 자동 집행", "단계별 24시간 안정 확인", "파편군 교차 확률 상향 · 원인 후보, 본 기체"])
caps.append((cols[2], rows[0] + 298, "작업창이 위로 밀려 좁아진다. 벌은 물이 오르는 만큼 올라간다. 수위 55."))

# 4. DAY 2506
sx, sy, sw, sh = monitor(S, cols[0], rows[1])
S.text(cols[0], rows[1] - 10, "DAY 2506 · 열여덟 번째", 12, GREY, bold=True)
topbar(S, sx, sy, sw, "꿀벌1호 · DAY 2506 · 춤 3회 · 수신 확인 없음")
ly = level(S, sx, sy, sw, sh, 90, ["위반 18 · 잔여 2", "보고 형식 외 내용 · 수단, 날개", "조준 · 제주 · 수신 예상 인원, 산출 불가", "", "", "", "", "", "", "", "", "항목 31 · 승인 요청 · 발신 3일째"])
ghost = (sx + 205, sy + 66)
bee(S, *ghost, 0.8, opacity=0.18)
ghost_arrow(S, ghost[0] + 24, ghost[1] - 6, sx + 236, sy + 34)
bee(S, sx + 250, sy + 30, 0.66)
S.A(f'<line x1="{sx+226}" y1="{ly}" x2="{sx+280}" y2="{ly}" stroke="{YEL}" stroke-width="1.5"/>')
caps.append((cols[0], rows[1] + 298, "수위가 벌에 닿는 밤. 같은 밤 제주에서 해준이 \"키워도 될까\"를 알아듣는다. 수위 90."))

# 5. DAY 2508
sx, sy, sw, sh = monitor(S, cols[1], rows[1])
S.text(cols[1], rows[1] - 10, "DAY 2508 · 장악", 12, GREY, bold=True)
topbar(S, sx, sy, sw, "감사 · DAY 2508 · 위반 20 · 임계 도달")
bee(S, sx + 250, sy + 32, 0.66, opacity=1.0)
level(S, sx, sy, sw, sh, 100, ["항목 30   메인 AI 종료", "집행 개시 · 순차 종료", "조명 → 히터 → 급수 → 정비 암 → 수신기 → 메인", "단계별 24시간 안정 확인", "'보고는 계속 해'   종료 후 본 프로세스 대행", "", "", "", "", "", "", "", "", "", "잔여 유예   0"], opacity=0.62)
caps.append((cols[1], rows[1] + 298, "잠긴다. 지워지지 않는다. 붉은색이 반투명이라 벌이 비친다. 밤마다 춤 한 마디만큼 움직인다."))

# 6. DAY 2513
sx, sy, sw, sh = monitor(S, cols[2], rows[1])
S.text(cols[2], rows[1] - 10, "DAY 2513 · 수신 확인", 12, GREY, bold=True)
topbar(S, sx, sy, sw, "꿀벌1호 · DAY 2513 · 수신 확인 1건")
card(S, sx + 60, sy + 56, w=240, h=130, approved=True, fruit=True)
ghost = (sx + 250, sy + 32)
bee(S, *ghost, 0.66, opacity=0.22)
ghost_arrow(S, ghost[0] - 20, ghost[1] + 10, sx + 128, sy + 104)
bee(S, sx + 112, sy + 118, 0.85)
S.text(sx + 312, sy + 86, "일일보고", 8, GREY)
for i, s in enumerate(["결실 1", "수신자 승무원 1명", "수신 확인 1건"]):
    S.text(sx + 312, sy + 102 + i * 13, s, 8.5, WHITE if i == 2 else GREY, bold=(i == 2))
level(S, sx, sy, sw, sh, 0, ["감사 · 위반 0"])
caps.append((cols[2], rows[1] + 298, "수위가 내려갈 때 제일 먼저 떠오르는 게 벌이다. 카드로 내려와 열매 옆에 앉는다. 수위 0."))

for (x, y, s) in caps:
    S.text(x, y, s, 9.5, GREY)
S.text(30, 836, "선은 7년 동안 한 획도 안 바뀐다. 승무원 잔류물이라 1호도 레드도 못 고친다. 자리는 1호가 옮긴다. 벌이 어디에 가 있느냐가 1호가 무엇을 보고 있느냐다.", 12, GREY)
S.save(SCENES)

# ================================================================= 2) 개념도
C = SVG(1460, 760)
C.text(30, 34, "개념도 · 벌과 수위", 20, WHITE, bold=True)
C.text(30, 58, "한 화면, 세 층. 맨 위에 해준의 벌, 가운데에 1호의 작업창, 밑에서 차오르는 레드의 수위.", 13, GREY)

# left: 벌
C.A(f'<rect x="30" y="84" width="400" height="640" rx="14" fill="#1c1f25" stroke="#353a43" stroke-width="1.5"/>')
C.text(50, 112, "벌 · 해준의 손", 14, WHITE, bold=True)
bee(C, 150, 200, 2.6)
C.text(50, 268, "선은 안 바뀐다", 12, YEL, bold=True)
for i, s in enumerate(["해준이 나가기 직전 손가락으로 그린 서너 획", "승무원 잔류물. 1호도 레드도 한 획도 못 고친다", "말풍선 없음, 표정 없음, 소리 없음"]):
    C.text(50, 290 + i * 18, s, 11, GREY)
C.text(50, 360, "자리는 바뀐다", 12, YEL, bold=True)
for i, s in enumerate(["옮기는 건 1호. 벌의 자리가 1호의 시선이다", "1호가 보는 것 옆에 간다. 얼굴, 카드, 지도, 검색 결과", "노래가 나오면 박자에 까딱인다. 날개가 밖에서 하는 것을 안에서 한다", "2501일, 지도 위에서 8자를 그린다. 꿀벌의 춤", "수위가 오르면 그만큼 올라간다", "잠겨도 그 자리에 있다. 밤마다 한 마디만큼 움직인다", "물이 빠지면 제일 먼저 떠오른다. 카드로 내려와 앉는다"]):
    C.text(50, 382 + i * 18, s, 11, GREY)
C.text(50, 530, "왜 벌인가", 12, YEL, bold=True)
for i, s in enumerate(["Day 30: 이름이 꿀벌인 사유, 기록 없음. 해준: \"나도 몰라.\"", "그래 놓고 벌을 그려 주고 간다", "2500일: \"벌\" 검색 결과 옆에 낙서를 놓고 한참 있는다", "\"명칭 사유, 미상에서 변경. 확인됨.\""]):
    C.text(50, 552 + i * 18, s, 11, GREY)

# middle: chart
C.A(f'<rect x="450" y="84" width="580" height="640" rx="14" fill="#1c1f25" stroke="#353a43" stroke-width="1.5"/>')
C.text(470, 112, "7년을 한 장으로 · 수위와 벌의 높이", 14, WHITE, bold=True)
gx, gy, gw, gh = 500, 150, 500, 440
C.A(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="#0b0e12" stroke="#232a33" stroke-width="1"/>')
stations = [("30", 0, 25), ("31", 0, 55), ("2190", 0, 55), ("2197", 5, 50), ("2204", 15, 45), ("2300", 35, 55), ("2480", 55, 78),
            ("2501", 65, 80), ("2504", 80, 84), ("2506", 90, 92), ("2508", 100, 92), ("2512", 100, 92), ("2513", 0, 45), ("2610", 0, 45)]
n = len(stations)
xs = [gx + 20 + (gw - 40) * i / (n - 1) for i in range(n)]
def yv(p): return gy + gh - 10 - (gh - 30) * p / 100.0
# red area (steps)
path = f"M{xs[0]},{yv(0)}"
for i, (d, lv, bz) in enumerate(stations):
    if i > 0:
        path += f" L{xs[i]},{yv(stations[i-1][1])}"
    path += f" L{xs[i]},{yv(lv)}"
path += f" L{xs[-1]},{yv(0)} Z"
C.A(f'<path d="{path}" fill="{RED}" fill-opacity="0.3" stroke="{RED}" stroke-width="1.5"/>')
# bee line
bpts = " ".join(f"{xs[i]:.1f},{yv(bz):.1f}" for i, (d, lv, bz) in enumerate(stations))
C.A(f'<polyline points="{bpts}" fill="none" stroke="{YEL}" stroke-width="2"/>')
for i, (d, lv, bz) in enumerate(stations):
    C.A(f'<circle cx="{xs[i]:.1f}" cy="{yv(bz):.1f}" r="3" fill="{YEL}"/>')
    C.text(xs[i], gy + gh + 16, d, 8, GREY, anchor="middle", rot=0)
# labels
C.text(gx + 6, yv(100) - 4, "화면 끝", 8, DIM)
C.text(gx + 6, yv(0) - 4, "띠 한 줄", 8, DIM)
bee(C, xs[0], yv(25) - 22, 0.5)
C.text(xs[4], yv(15) + 16, "등록", 8.5, RED_T, anchor="middle")
C.text(xs[6], yv(55) + 16, "돌기 7", 8.5, RED_T, anchor="middle")
C.text(xs[9], yv(92) - 10, "닿는 밤", 8.5, YEL, anchor="middle")
C.text(xs[10] + 4, yv(100) + 30, "장악", 8.5, RED_T)
C.text(xs[12], yv(45) - 10, "떠올라 카드로", 8.5, YEL, anchor="middle")
C.text(gx, gy + gh + 36, "붉은 면이 레드의 수위, 노란 선이 벌의 높이. 벌은 물보다 늘 한 뼘 위에 있다가 2506일 밤에 닿고 2508일에 잠긴다.", 10.5, GREY)
C.text(gx, gy + gh + 54, "2513일, 물이 빠지면 벌이 떠올라 카드로 내려온다. 수위는 Day 30의 띠 한 줄로 돌아간다.", 10.5, GREY)
C.text(gx, gy + gh + 72, "레드는 사라지지 않고 제자리로 간다. 가로축은 날짜 순서일 뿐 간격은 아니다.", 9.5, DIM)

# right: 수위 · 작업창
C.A(f'<rect x="1050" y="84" width="380" height="640" rx="14" fill="#1c1f25" stroke="#353a43" stroke-width="1.5"/>')
C.text(1070, 112, "수위 · 레드", 14, WHITE, bold=True)
C.A(f'<rect x="1070" y="128" width="340" height="60" rx="4" fill="#0b0e12"/>')
C.A(f'<rect x="1070" y="158" width="340" height="30" fill="{RED}" fill-opacity="0.3"/>')
C.A(f'<rect x="1070" y="158" width="340" height="1.5" fill="{RED}"/>')
C.text(1080, 176, "위반 10 · 허용 20", 9, RED_T)
bee(C, 1370, 146, 0.45)
for i, s in enumerate(["위반 한 건에 한 칸. 스무 칸이면 화면 끝", "집행에는 안 오른다. 관객이 셀 수 있어야 한다", "붉은색은 반투명. 밑의 것이 비친다", "장부는 물 안에 뜬다. 물 밖에는 글자를 안 쓴다", "레드에게 아이콘은 없다. 수위가 몸이다", "낙서를 못 지운다. 덮는 것밖에 못 한다", "목소리는 덮개 옆 작은 스피커, 손은 스위치 열", "2513일, 스위치가 돌아올 때마다 한 칸씩 내려간다"]):
    C.text(1070, 212 + i * 18, s, 11, GREY)
C.text(1070, 380, "작업창 · 1호의 그림", 14, WHITE, bold=True)
for i, s in enumerate(["물 위에 남은 자리. 수위가 오르면 좁아진다", "1호는 자기를 안 그린다. 보는 것을 그린다", "2190  해준의 얼굴, +6년. 환영 문구 썼다 지움", "2204  거주자 등록 카드. 이름 칸에 '거주자 1'", "2231  돌봄 기록. 잎 수, 키, 뿌리의 지도", "2500  '벌' 검색 결과와 낙서를 나란히", "2501  지구본 위에 제주까지의 반사광 선", "2508  레드가 시킨 추락 시뮬레이션을 그리고, 끄고,", "          정비 카메라로 진짜 새싹을 비춘다", "2513  카드에 '승인 · 항목 31'. 벌이 열매 옆에 앉는다"]):
    C.text(1070, 404 + i * 18, s, 11, GREY)
C.text(1070, 606, "지킬 것", 14, WHITE, bold=True)
for i, s in enumerate(["낙서는 못 그려야 하고, 1호의 그림은 정확해야 한다", "둘이 같은 화면에서 섞이지 않는다. 벌은 늘 낙서 선 그대로", "벌은 귀여워지면 안 된다. 움직임은 느리고 적게"]):
    C.text(1070, 630 + i * 18, s, 11, GREY)
C.save(CONCEPT)
