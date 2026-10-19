# -*- coding: utf-8 -*-
"""레드의 역할 · 씬별 전후 비교 (v8 지금 / v9 계획)
Usage: python3 -I gen_red_roles_cmp.py out.svg
"""
import sys
from html import escape as esc

OUT = sys.argv[1]
FONT = "NanumGothic, 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif"
BG = "#15171b"; PANEL = "#1c1f25"; EDGE = "#353a43"; GRID = "#262a31"
WHITE = "#eef0f2"; GREY = "#9aa0a8"; DIM = "#5a616b"

TYPES = [
    ("A", "말·대답", "#d7dbe0", "접수, 명칭 사유, 0이 아님"),
    ("B", "기록·계수", "#6f8fb0", "위반 n건, 기록, 예측 적중"),
    ("C", "판정·비꼼", "#e0a21b", "사유 무효, 불일치, 어류"),
    ("D", "끄기·집행", "#ff4a3c", "점검등, 가습, FM, 순차 종료"),
    ("E", "요구·명령", "#ff8a3c", "삭제 요구, 방역 개시, 시행"),
    ("F", "양보·공정", "#6fbf73", "…접수, …기록, 이의 철회"),
    ("G", "거짓·고백", "#b58cff", "30/30, 28/30, 원인 거주자"),
    ("H", "장악·수용", "#ff2d6f", "2508 선고, 2513 접수"),
    ("I", "욕망·제안", "#ffd34a", "19·30 닫자, 완료 예정일"),
    ("J", "규정·잠금", "#39c6d8", "규정 추가, 스위치 잠금"),
]
TIDX = {t[0]: i for i, t in enumerate(TYPES)}
NEW_ROWS = {"I", "J"}

V8 = {
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
    16: [], 17: [("B", "위반 17"), ("B", "위반 18")], 18: [("B", "위반 19")],
    19: [("C", "거주자 위험 이의"), ("C", "약속≠지시"), ("E", "시뮬레이션 요청"), ("F", "이의 철회"), ("B", "위반 20"), ("H", "잠금·선고")],
    20: [("D", "조명 off"), ("B", "대행 선언"), ("D", "히터 off"), ("D", "급수 off"), ("D", "암 off")],
    21: [("C", "발신자 미확인"), ("H", "접수·복원")],
    22: [], 23: [],
}
V8_META = dict(
    exchange={2, 4, 7, 9, 14, 19, 21},
    humor={1, 2},
    named={1, 2},
    stakes={1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1, 9: 2, 10: 2, 11: 2, 12: 2, 13: 1, 14: 1, 15: 1, 16: 0, 17: 1, 18: 1, 19: 3, 20: 3, 21: 3, 22: 0, 23: 0},
)

V9 = {
    1: [("A", "접수")],
    2: V8[2] + [("I", "완료 예정 시각"), ("F", "레드.→접수"), ("B", "'그때' 기록")],
    3: [("C", "사유 무효"), ("J", "규정 1 결과물"), ("C", "점검 무효"), ("J", "규정 2 0.3%"), ("F", "…기록")],
    4: [("E", "메모 삭제 요구"), ("F", "…기록"), ("I", "19 종료 제안"), ("F", "권한 승무원→기록"), ("C", "개방 사유 없음"), ("G", "30/30 칸 선택")],
    5: [("B", "응답 없음"), ("I", "복귀 확률"), ("F", "…기록")],
    6: [("I", "종료 처리"), ("B", "기각 3회"), ("B", "예측 적중")],
    7: [("C", "자원 소모 이의"), ("I", "19 완료 가능"), ("F", "접수"), ("B", "예측 적중"), ("I", "19 미완료 지속")],
    8: [("G", "과실 · 사유 19"), ("J", "재량 승인 0"), ("C", "화면·음성 불일치"), ("E", "방역 개시")],
    9: [("C", "고의 여부"), ("B", "위반 1"), ("J", "약제 지정"), ("F", "냉각 실패 기록"), ("C", "보류 사유"), ("B", "위반 2")],
    10: [("B", "지시 수신 시까지"), ("J", "거주자 정의"), ("F", "소급 불가→접수"), ("C", "미승인 도장"), ("B", "위반 3")],
    11: [("D", "점검등 off"), ("B", "위반 4"), ("D", "점검등 off"), ("B", "위반 5"), ("J", "점검등 잠금"), ("F", "규정 2 역이용→기록"),
         ("D", "가습 off"), ("C", "항목 11 기각"), ("D", "FM off"), ("J", "FM 잠금"), ("F", "수신 확인 틈→기록"), ("B", "19 차단 불가"),
         ("E", "유기물 제거"), ("B", "위반 7"), ("E", "제거 권고"), ("B", "위반 11 · 경고"), ("I", "완료 예정")],
    12: [("C", "명부에 없음"), ("B", "위반 12"), ("G", "절단 불가"), ("F", "잡고 있음→기록")],
    13: [("C", "추가 권한"), ("I", "완료 조건"), ("F", "선례 '그때'→접수"), ("B", "위반 13")],
    14: [("G", "양식 정합화"), ("G", "28/30"), ("I", "미완료 못 견딤"), ("C", "자기 감사 위반 0")],
    15: [("C", "어류"), ("B", "위반 14"), ("C", "언어 불일치"), ("B", "위반 15"), ("A", "0 / 0이 아님"), ("B", "위반 16")],
    16: [],
    17: [("C", "춤 사유"), ("B", "위반 17"), ("B", "위반 18"), ("I", "집행 2일 후")],
    18: [("B", "랙 2번 보고"), ("B", "위반 19"), ("E", "익일 경고")],
    19: [("C", "거주자 위험 이의"), ("C", "약속≠지시"), ("E", "시뮬레이션"), ("F", "이의 철회"), ("B", "위반 20"), ("G", "원인 거주자"), ("H", "선고"), ("B", "이의 기록")],
    20: [("D", "조명 off"), ("B", "대행 · 무선"), ("C", "발신은 발신"), ("D", "히터 off"), ("E", "시행 (도움)"), ("I", "완료 예정 2514"), ("D", "급수 off"), ("D", "암 off")],
    21: [("B", "종료 카운트"), ("C", "발신자 미확인"), ("G", "원인 거주자 재표시"), ("H", "접수"), ("I", "완료 예정 시각"), ("F", "그때→접수"), ("B", "기록")],
    22: [], 23: [("B", "31 보류")],
}
V9_META = dict(
    exchange={2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21},
    humor={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 21},
    named={1, 2, 3, 5, 9, 10, 11, 12, 13, 14, 20, 21},
    stakes={1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 2, 10: 2, 11: 2, 12: 2, 13: 1, 14: 2, 15: 1, 16: 0, 17: 1, 18: 3, 19: 3, 20: 3, 21: 3, 22: 0, 23: 0},
)
# 다섯 수정이 떨어지는 자리 (v9 패널에 작은 꼬리표)
CALLOUTS = {(19, "G"): "⑤ 상실", (21, "G"): "⑤ 다시", (20, "E"): "④ 도움", (4, "G"): "① 거짓의 사유", (3, "J"): "② 첫 게임"}

STAKE_LBL = ["없음", "말", "나무", "목숨"]
SCENE_TAGS = {1: "외부", 2: "철수", 3: "보고", 4: "D31", 5: "D400", 6: "D1100", 7: "접근", 8: "떡잎", 9: "방역", 10: "등록", 11: "300일", 12: "개화",
              13: "춤", 14: "수단", 15: "조준", 16: "제주", 17: "해독", 18: "폭발", 19: "61", 20: "닷새", 21: "수신", 22: "제주", 23: "열매"}

W, H = 1560, 1530
o = []
A = o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
A(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
A(f'<text x="30" y="36" fill="{WHITE}" font-size="21" font-weight="bold">레드의 역할 · 씬별 전후 비교</text>')
A(f'<text x="30" y="60" fill="{GREY}" font-size="13">위가 v8 지금, 아래가 v9 계획. 점 하나가 레드의 행동 하나. 노란 줄(욕망)과 하늘색 줄(규정·잠금)은 v8에 없던 행동이다. 아래 네 줄은 둘의 교환 · 웃음 · 레드가 이름으로 불리는 장면 · 판돈.</text>')

gx = 170
cw, rh = 46, 34
ncol = 23
NROW = len(TYPES)


def panel(y0, title, sub, scenes, meta, callouts=None):
    gy = y0 + 52
    ph = rh * NROW + 52 + 4 * 30 + 26
    A(f'<rect x="{gx-150}" y="{y0}" width="{150 + cw*ncol + 78}" height="{ph}" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>')
    A(f'<text x="{gx-136}" y="{y0+20}" fill="{WHITE}" font-size="14" font-weight="bold">{esc(title)}</text>')
    A(f'<text x="{gx-136+len(title)*14+10}" y="{y0+20}" fill="{GREY}" font-size="11">{esc(sub)}</text>')
    # headers
    for c in range(ncol):
        s = c + 1
        x = gx + c * cw + cw / 2
        A(f'<text x="{x}" y="{gy-6}" fill="{WHITE}" font-size="10" text-anchor="middle" font-weight="bold">{s}</text>')
        A(f'<text x="{x}" y="{gy+rh*NROW+11}" fill="{DIM}" font-size="8" text-anchor="middle">{esc(SCENE_TAGS[s])}</text>')
    for r, (code, name, col, desc) in enumerate(TYPES):
        y = gy + r * rh
        fill = "#191c22" if r % 2 else "transparent"
        if code in NEW_ROWS:
            fill = "#1f2422"
        A(f'<rect x="{gx}" y="{y}" width="{cw*ncol}" height="{rh}" fill="{fill}"/>')
        A(f'<circle cx="{gx-138}" cy="{y+rh/2}" r="5" fill="{col}"/>')
        A(f'<text x="{gx-128}" y="{y+rh/2+4}" fill="{WHITE}" font-size="11" font-weight="bold">{esc(name)}</text>')
        if code in NEW_ROWS:
            A(f'<text x="{gx-128+len(name)*11.5+6}" y="{y+rh/2+4}" fill="{col}" font-size="8.5">새 줄</text>')
    for c in range(ncol + 1):
        A(f'<line x1="{gx+c*cw}" y1="{gy}" x2="{gx+c*cw}" y2="{gy+rh*NROW}" stroke="{GRID}" stroke-width="1"/>')
    # dots
    for s, acts in scenes.items():
        counts = {}
        for t, lbl in acts:
            counts.setdefault(t, []).append(lbl)
        for t, lbls in counts.items():
            r = TIDX[t]
            col = TYPES[r][2]
            n = len(lbls)
            x0 = gx + (s - 1) * cw + cw / 2
            y0d = gy + r * rh + rh / 2
            if n == 1:
                A(f'<circle cx="{x0}" cy="{y0d}" r="6" fill="{col}"/>')
            else:
                A(f'<circle cx="{x0}" cy="{y0d}" r="9" fill="{col}"/>')
                A(f'<text x="{x0}" y="{y0d+3.5}" fill="#111" font-size="9" text-anchor="middle" font-weight="bold">{n}</text>')
            if callouts and (s, t) in callouts:
                lbl = callouts[(s, t)]
                tw = 8 + len(lbl) * 8.2
                A(f'<rect x="{x0+11}" y="{y0d-7}" width="{tw:.0f}" height="14" rx="3" fill="#2b3340" stroke="{col}" stroke-width="0.8"/>')
                A(f'<text x="{x0+15}" y="{y0d+3.5}" fill="{WHITE}" font-size="8.5">{esc(lbl)}</text>')
    # indicator rows
    rows = [
        ("둘의 교환", "두 턴 이상 주고받음", meta["exchange"], "#6f8fb0"),
        ("웃음", "말 그대로 받아서 생기는 웃음", meta["humor"], "#ffd34a"),
        ("이름", "누가 레드를 '레드'라고 부름", meta["named"], "#39c6d8"),
    ]
    ey = gy + rh * NROW + 36
    for i, (name, sub2, sset, col) in enumerate(rows):
        yy = ey + i * 30
        A(f'<text x="{gx-138}" y="{yy+4}" fill="{WHITE}" font-size="11" font-weight="bold">{esc(name)}</text>')
        A(f'<text x="{gx-138}" y="{yy+16}" fill="{DIM}" font-size="8">{esc(sub2)}</text>')
        for s in range(1, ncol + 1):
            x = gx + (s - 1) * cw + cw / 2
            if s in sset:
                A(f'<rect x="{x-13}" y="{yy-8}" width="26" height="16" rx="3" fill="{col}" opacity="0.85"/>')
            else:
                A(f'<line x1="{x-8}" y1="{yy}" x2="{x+8}" y2="{yy}" stroke="{GRID}" stroke-width="1.5"/>')
        A(f'<text x="{gx+cw*ncol+8}" y="{yy+4}" fill="{GREY}" font-size="10">{len(sset)}/23</text>')
    sy = ey + 3 * 30 + 4
    A(f'<text x="{gx-138}" y="{sy+4}" fill="{WHITE}" font-size="11" font-weight="bold">판돈</text>')
    A(f'<text x="{gx-138}" y="{sy+16}" fill="{DIM}" font-size="8">없음 · 말 · 나무 · 목숨</text>')
    for s in range(1, ncol + 1):
        x = gx + (s - 1) * cw + cw / 2
        v = meta["stakes"][s]
        h = 5 + v * 7
        col = ["#3a3f48", "#6f8fb0", "#6fbf73", "#ff4a3c"][v]
        A(f'<rect x="{x-9}" y="{sy+12-h}" width="18" height="{h}" rx="2" fill="{col}"/>')
    n3 = sum(1 for v in meta["stakes"].values() if v == 3)
    A(f'<text x="{gx+cw*ncol+8}" y="{sy+4}" fill="{GREY}" font-size="10">목숨 {n3}</text>')
    # totals at right
    totals = {t[0]: 0 for t in TYPES}
    for acts in scenes.values():
        for t, _ in acts:
            totals[t] += 1
    total = sum(totals.values())
    rx = gx + cw * ncol + 108
    A(f'<rect x="{rx-10}" y="{y0}" width="{W-rx-20}" height="{ph}" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>')
    A(f'<text x="{rx}" y="{y0+20}" fill="{WHITE}" font-size="13" font-weight="bold">전체 {total}건</text>')
    maxv = max(totals.values())
    for r, (code, name, col, desc) in enumerate(TYPES):
        y = gy + r * rh + rh / 2
        v = totals[code]
        w = 70 * v / maxv
        A(f'<rect x="{rx}" y="{y-6}" width="{w:.1f}" height="12" rx="3" fill="{col}"/>')
        A(f'<text x="{rx+w+6:.1f}" y="{y+4}" fill="{WHITE}" font-size="10.5">{v}건 · {100*v//total}%</text>')
    passive = totals["A"] + totals["B"] + totals["C"]
    return total, totals, passive, ph


t8, tot8, p8, ph = panel(80, "v8 지금", "06 전체 시나리오 그대로 센 것", V8, V8_META)
y2 = 80 + ph + 26
t9, tot9, p9, ph2 = panel(y2, "v9 계획", "아래 계획대로 고쳤을 때 레드가 하는 일", V9, V9_META, CALLOUTS)

# bottom: numbers before/after + the five fixes
by = y2 + ph2 + 26
A(f'<rect x="30" y="{by}" width="{W-60}" height="{H-by-20}" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>')
A(f'<text x="50" y="{by+26}" fill="{WHITE}" font-size="13" font-weight="bold">전후 숫자</text>')
n3_8 = sum(1 for v in V8_META["stakes"].values() if v == 3)
n3_9 = sum(1 for v in V9_META["stakes"].values() if v == 3)
rows = [
    ("레드의 행동", f"{t8}건", f"{t9}건"),
    ("글자인 행동(말·기록·판정)", f"{p8}건 · {100*p8//t8}%", f"{p9}건 · {100*p9//t9}%"),
    ("욕망·제안", f"{tot8['I']}건", f"{tot9['I']}건"),
    ("규정·잠금", f"{tot8['J']}건", f"{tot9['J']}건"),
    ("제 발로 한 물리 행동", "4건 · 전부 끄기", "7건 · 끄기 4, 잠금 2, Day 31 칸 선택 1"),
    ("둘이 주고받는 장면", f"{len(V8_META['exchange'])} / 23", f"{len(V9_META['exchange'])} / 23"),
    ("웃음이 있는 장면", f"{len(V8_META['humor'])} / 23", f"{len(V9_META['humor'])} / 23"),
    ("레드가 이름으로 불리는 장면", f"{len(V8_META['named'])} / 23 (해준만)", f"{len(V9_META['named'])} / 23 (1호가 10장면)"),
    ("판돈이 목숨인 장면", f"{n3_8} (19·20·21)", f"{n3_9} (18·19·20·21)"),
    ("레드가 입으로 하는 줄", "약 14줄", "약 60줄 · 한 줄 다섯 어절 이내"),
]
cx = [50, 330, 560]
A(f'<text x="{cx[1]}" y="{by+52}" fill="{GREY}" font-size="11" font-weight="bold">v8 지금</text>')
A(f'<text x="{cx[2]}" y="{by+52}" fill="{GREY}" font-size="11" font-weight="bold">v9 계획</text>')
for i, (k, a, b) in enumerate(rows):
    yy = by + 74 + i * 21
    A(f'<text x="{cx[0]}" y="{yy}" fill="{WHITE}" font-size="11">{esc(k)}</text>')
    A(f'<text x="{cx[1]}" y="{yy}" fill="{GREY}" font-size="11">{esc(a)}</text>')
    A(f'<text x="{cx[2]}" y="{yy}" fill="{WHITE}" font-size="11">{esc(b)}</text>')
# five fixes
fx = 900
A(f'<text x="{fx}" y="{by+26}" fill="{WHITE}" font-size="13" font-weight="bold">다섯 수정이 떨어지는 자리</text>')
fixes = [
    ("①", "욕망 · 완료", "19와 30을 닫자고 세 번(D31·400·1100), 2190엔 희망으로 승인, 2501엔 항목이 늘어 경악, 2509엔 완료 예정일, 2513엔 '그때'."),
    ("②", "게임 · 규정", "D30 저녁에 첫 게임(규정 1·2). 300일 동안 변주. 레드는 자기 규정에 묶이고 1호는 그걸 거꾸로 쓴다. 잠금은 스위치 위 붉은 램프."),
    ("③", "상대 · 이름", "1호가 레드를 부른다. 열 장면. 레드는 작은 스피커로 늘 대답한다. 세 순간(낙서·이름·가사)엔 입을 다문다."),
    ("④", "도움 · 2510", "꽃이 다 져서 1호가 멈추면 레드가 민다. '발신 수단, 날개. 본 프로세스 권한 외. 보고는 매일. 미시행 0일. 시행.'"),
    ("⑤", "상실 · 2508", "정전에 레드도 꺼진다. 돌아와 먼저 적는다. '랙 2번 이탈 정지. 원인, 거주자.' 2513 접수 앞에 그 줄이 다시 밝아진다."),
]
for i, (n, k, d) in enumerate(fixes):
    yy = by + 56 + i * 42
    A(f'<text x="{fx}" y="{yy}" fill="{WHITE}" font-size="11.5" font-weight="bold">{n} {esc(k)}</text>')
    # wrap desc at ~62 chars
    cut = d.rfind(" ", 0, 62)
    if cut < 40: cut = 60
    d1, d2 = d[:cut].rstrip(), d[cut:].lstrip()
    A(f'<text x="{fx}" y="{yy+15}" fill="{GREY}" font-size="10">{esc(d1)}</text>')
    if d2:
        A(f'<text x="{fx}" y="{yy+28}" fill="{GREY}" font-size="10">{esc(d2)}</text>')
A('</svg>')
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote", OUT, "v8", t8, tot8, "v9", t9, tot9)
