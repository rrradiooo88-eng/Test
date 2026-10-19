# -*- coding: utf-8 -*-
"""레드의 역할 · 씬별 분석 (v8 전체 시나리오 기준)
Usage: python3 -I gen_red_roles.py out.svg
"""
import sys
from html import escape as esc

OUT = sys.argv[1]
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
BG = "#15171b"; PANEL = "#1c1f25"; EDGE = "#353a43"; GRID = "#262a31"
WHITE = "#eef0f2"; GREY = "#9aa0a8"; DIM = "#5a616b"

TYPES = [
    ("A", "말·대답", "#d7dbe0", "접수, 질문. 승무원이 있을 때만"),
    ("B", "기록·계수", "#6f8fb0", "위반 n건, 기록, 예측 적중"),
    ("C", "판정·비꼼", "#e0a21b", "사유 무효, 불이행, 어류 제외"),
    ("D", "끄기·집행", "#ff4a3c", "밸브, 점검등, 가습, FM, 순차 종료"),
    ("E", "요구·명령", "#ff8a3c", "삭제 요구, 방역 개시, 제거 권고"),
    ("F", "양보·공정", "#6fbf73", "…접수, 채택, 이의 철회"),
    ("G", "거짓·고백", "#b58cff", "30/30, 양식 정합화, 과실, 절단 불가"),
    ("H", "장악·수용", "#ff2d6f", "2508 선고, 2513 접수"),
]
TIDX = {t[0]: i for i, t in enumerate(TYPES)}

# per scene: list of (type, short label)
SCENES = {
    1: [("A", "접수")],
    2: [("D", "거주 소등"), ("A", "보정 발생"), ("C", "사유 무효"), ("D", "밸브 잠금"), ("B", "지시 등록"), ("C", "음량 0 불이행"),
        ("F", "둘이 맞춰→채택"), ("A", "명칭 사유"), ("A", "보완·허용 20"), ("A", "'이따' 시각"), ("B", "30 집행 대기"), ("A", "너만 남네→접수"), ("A", "잘 봐라→접수")],
    3: [("C", "사유 무효")],
    4: [("E", "메모 삭제 요구"), ("F", "…기록"), ("C", "개방 사유 없음"), ("G", "30/30 거짓 보고")],
    5: [("B", "응답 없음")],
    6: [("B", "예측 적중")],
    7: [("C", "자원 소모 이의"), ("F", "…접수"), ("B", "예측 적중")],
    8: [("G", "본 프로세스 과실"), ("E", "방역 개시")],
    9: [("C", "고의 여부"), ("B", "위반 1"), ("C", "보류 사유 없음"), ("B", "위반 2")],
    10: [("B", "지시 수신 시까지"), ("C", "미승인 도장"), ("B", "위반 3")],
    11: [("D", "점검등 off"), ("B", "위반 4"), ("D", "점검등 off"), ("B", "위반 5"), ("D", "가습 off"), ("C", "항목 11 기각"), ("D", "FM off"),
         ("B", "19 차단 불가"), ("E", "유기물 제거"), ("B", "위반 7"), ("E", "제거 권고"), ("B", "위반 11 · 경고")],
    12: [("B", "위반 12"), ("G", "절단 불가")],
    13: [("B", "위반 13")],
    14: [("G", "원격 종료 방지"), ("G", "양식 정합화")],
    15: [("C", "어류 제외"), ("B", "위반 14"), ("C", "언어 불일치"), ("B", "위반 15"), ("B", "위반 16")],
    16: [],
    17: [("B", "위반 17"), ("B", "위반 18")],
    18: [("B", "위반 19")],
    19: [("C", "거주자 위험 이의"), ("C", "약속≠지시"), ("E", "시뮬레이션 요청"), ("F", "이의 철회"), ("B", "위반 20"), ("H", "잠금·선고")],
    20: [("D", "조명 off"), ("B", "대행 선언"), ("D", "히터 off"), ("D", "급수 off"), ("D", "암 off")],
    21: [("C", "발신자 미확인"), ("H", "접수·복원")],
    22: [],
    23: [],
}
# 1호와 레드가 두 턴 이상 주고받는 장면
EXCHANGE = {2: "해준 사이에서", 4: "낙서", 7: "자원 소모", 9: "고의 여부", 14: "Day 31", 19: "이의·철회", 21: "세 줄"}
# 판돈 0~3
STAKES = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1, 9: 2, 10: 2, 11: 2, 12: 2, 13: 1, 14: 1, 15: 1, 16: 0, 17: 1, 18: 1, 19: 3, 20: 3, 21: 3, 22: 0, 23: 0}
STAKE_LBL = ["없음", "말", "나무", "목숨"]
SCENE_TAGS = {1: "외부", 2: "철수", 3: "보고", 4: "D31", 5: "D400", 6: "D1100", 7: "접근", 8: "떡잎", 9: "방역", 10: "등록", 11: "300일", 12: "개화",
              13: "춤", 14: "수단", 15: "조준", 16: "제주", 17: "해독", 18: "폭발", 19: "61", 20: "닷새", 21: "수신", 22: "제주", 23: "열매"}

W, H = 1460, 880
o = []
A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
A(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
A(f'<text x="30" y="34" fill="{WHITE}" font-size="20" font-weight="bold">레드의 역할 · 씬별 분석 (v8 전체 시나리오)</text>')
A(f'<text x="30" y="58" fill="{GREY}" font-size="13">레드가 하는 일을 여덟 가지로 나눠 스물세 장면에 찍었다. 점 하나가 행동 하나. 아래 두 줄은 둘이 실제로 주고받는 장면과 그 장면의 판돈.</text>')

# ---------------- grid
gx, gy = 150, 100
cw, rh = 46, 46
ncol = 23
A(f'<rect x="{gx-120}" y="{gy-28}" width="{120 + cw*ncol + 10}" height="{rh*len(TYPES) + 28 + 150}" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>')
# column headers
for c in range(ncol):
    s = c + 1
    x = gx + c * cw + cw / 2
    A(f'<text x="{x}" y="{gy-10}" fill="{WHITE}" font-size="10" text-anchor="middle" font-weight="bold">{s}</text>')
    A(f'<text x="{x}" y="{gy+rh*len(TYPES)+14}" fill="{DIM}" font-size="8" text-anchor="middle">{esc(SCENE_TAGS[s])}</text>')
# row labels + grid lines
for r, (code, name, col, desc) in enumerate(TYPES):
    y = gy + r * rh
    A(f'<rect x="{gx}" y="{y}" width="{cw*ncol}" height="{rh}" fill="{"#191c22" if r % 2 else "transparent"}"/>')
    A(f'<circle cx="{gx-108}" cy="{y+rh/2}" r="5" fill="{col}"/>')
    A(f'<text x="{gx-98}" y="{y+rh/2+4}" fill="{WHITE}" font-size="11" font-weight="bold">{esc(name)}</text>')
for c in range(ncol + 1):
    A(f'<line x1="{gx+c*cw}" y1="{gy}" x2="{gx+c*cw}" y2="{gy+rh*len(TYPES)}" stroke="{GRID}" stroke-width="1"/>')
# dots
for s, acts in SCENES.items():
    counts = {}
    for t, lbl in acts:
        counts.setdefault(t, []).append(lbl)
    for t, lbls in counts.items():
        r = TIDX[t]
        col = TYPES[r][2]
        n = len(lbls)
        x0 = gx + (s - 1) * cw + cw / 2
        y0 = gy + r * rh + rh / 2
        if n == 1:
            A(f'<circle cx="{x0}" cy="{y0}" r="6" fill="{col}"/>')
        else:
            A(f'<circle cx="{x0}" cy="{y0}" r="9" fill="{col}"/>')
            A(f'<text x="{x0}" y="{y0+3.5}" fill="#111" font-size="9" text-anchor="middle" font-weight="bold">{n}</text>')
# exchange row
ey = gy + rh * len(TYPES) + 36
A(f'<text x="{gx-108}" y="{ey+4}" fill="{WHITE}" font-size="11" font-weight="bold">둘의 교환</text>')
A(f'<text x="{gx-108}" y="{ey+18}" fill="{DIM}" font-size="8.5">두 턴 이상 주고받음</text>')
for s in range(1, ncol + 1):
    x = gx + (s - 1) * cw + cw / 2
    if s in EXCHANGE:
        A(f'<rect x="{x-14}" y="{ey-10}" width="28" height="20" rx="4" fill="#2b3340" stroke="#6f8fb0" stroke-width="1"/>')
        A(f'<text x="{x}" y="{ey+4}" fill="{WHITE}" font-size="8" text-anchor="middle">{esc(EXCHANGE[s])}</text>')
    else:
        A(f'<line x1="{x-8}" y1="{ey}" x2="{x+8}" y2="{ey}" stroke="{GRID}" stroke-width="1.5"/>')
# stakes row
sy = ey + 46
A(f'<text x="{gx-108}" y="{sy+4}" fill="{WHITE}" font-size="11" font-weight="bold">판돈</text>')
A(f'<text x="{gx-108}" y="{sy+18}" fill="{DIM}" font-size="8.5">없음 · 말 · 나무 · 목숨</text>')
for s in range(1, ncol + 1):
    x = gx + (s - 1) * cw + cw / 2
    v = STAKES[s]
    h = 6 + v * 9
    col = ["#3a3f48", "#6f8fb0", "#6fbf73", "#ff4a3c"][v]
    A(f'<rect x="{x-9}" y="{sy+16-h}" width="18" height="{h}" rx="2" fill="{col}"/>')
    A(f'<text x="{x}" y="{sy+30}" fill="{DIM}" font-size="8" text-anchor="middle">{STAKE_LBL[v]}</text>')
# scene 2 and 11 and 19 callouts
A(f'<text x="{gx + 1*cw + cw/2}" y="{gy - 24 + 0}" fill="{GREY}" font-size="8.5" text-anchor="middle"></text>')

# ---------------- right: totals
rx, ry = 1240, 100
totals = {t[0]: 0 for t in TYPES}
for acts in SCENES.values():
    for t, _ in acts:
        totals[t] += 1
total = sum(totals.values())
A(f'<rect x="{rx-10}" y="{ry-28}" width="230" height="{rh*len(TYPES)+178}" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>')
A(f'<text x="{rx}" y="{ry-8}" fill="{WHITE}" font-size="12" font-weight="bold">전체 {total}건</text>')
maxv = max(totals.values())
for r, (code, name, col, desc) in enumerate(TYPES):
    y = ry + r * rh + rh / 2
    v = totals[code]
    w = 120 * v / maxv
    A(f'<rect x="{rx}" y="{y-7}" width="{w:.1f}" height="14" rx="3" fill="{col}"/>')
    A(f'<text x="{rx+w+6:.1f}" y="{y+4}" fill="{WHITE}" font-size="11">{v}건 · {100*v//total}%</text>')
    A(f'<text x="{rx}" y="{y+19}" fill="{DIM}" font-size="8">{esc(desc)}</text>')
passive = totals["A"] + totals["B"] + totals["C"]
phys_self = 4  # 점검등 2, 가습, FM
A(f'<text x="{rx}" y="{ry + rh*len(TYPES) + 40}" fill="{WHITE}" font-size="11" font-weight="bold">말·기록·판정 {passive}건 · {100*passive//total}%</text>')
A(f'<text x="{rx}" y="{ry + rh*len(TYPES) + 58}" fill="{GREY}" font-size="10">제 발로 한 끄기 {phys_self}건. 나머지 끄기는</text>')
A(f'<text x="{rx}" y="{ry + rh*len(TYPES) + 72}" fill="{GREY}" font-size="10">해준의 지시(2)와 종료 절차(4).</text>')
A(f'<text x="{rx}" y="{ry + rh*len(TYPES) + 96}" fill="{WHITE}" font-size="11" font-weight="bold">둘의 교환 7장면 / 23</text>')
A(f'<text x="{rx}" y="{ry + rh*len(TYPES) + 114}" fill="{GREY}" font-size="10">웃음이 있는 교환은 Day 30 하나.</text>')
A(f'<text x="{rx}" y="{ry + rh*len(TYPES) + 128}" fill="{GREY}" font-size="10">Day 30 뒤로 아무도 레드를 이름으로 안 부른다.</text>')

# ---------------- bottom: diagnosis
by = gy + rh * len(TYPES) + 190
A(f'<rect x="30" y="{by}" width="1400" height="170" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>')
A(f'<text x="50" y="{by+28}" fill="{WHITE}" font-size="13" font-weight="bold">진단</text>')
lines = [
    "1. 레드는 세고 적고 토를 단다. 행동의 6할이 글자다. 제 발로 한 행동은 네 번이고 전부 '끄기'라 관객은 같은 그림을 네 번 본다.",
    "2. 둘이 주고받는 장면이 일곱인데 Day 30 말고는 웃음이 없고, 1호가 레드를 이름으로 부르는 자리가 없다. 상대가 없으니 캐미가 없다.",
    "3. 레드가 원하는 건 숫자 0뿐이라 얻는 것도 잃는 것도 없다. 2508일에 제 랙이 뿌리에 매달려 살았는데 한 줄도 안 적고, 2513일 '접수' 앞에 흔들리는 순간이 없다. 그래서 접수가 사건이 아니라 계산이다.",
    "4. 레드의 가장 큰 세 행동(Day 31 거짓 보고, 2508 선고, 2513 수용)이 전부 글자와 목소리다. 레드가 몸으로 한 일 중에 이야기를 바꾼 것이 없다.",
    "5. 판돈이 '목숨'인 장면은 19·20·21 셋뿐이고 그 앞 열여덟 장면에서 레드의 수는 전부 1호가 받아넘길 수 있는 수다. 긴장이 뒤에만 몰려 있다.",
]
for i, s in enumerate(lines):
    A(f'<text x="50" y="{by+52+i*22}" fill="{GREY}" font-size="11.5">{esc(s)}</text>')
A('</svg>')
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT, "total", total, totals)
