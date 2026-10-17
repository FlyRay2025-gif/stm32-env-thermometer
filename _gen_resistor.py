# -*- coding: utf-8 -*-
"""电阻在面包板上的正确接法示意 -> 电阻接法示意.svg"""
W, H = 1900, 1200
FONT = "Microsoft YaHei, SimHei, sans-serif"
RED, BLK, GRN, BLU, ORG, TEAL = '#E03131', '#212529', '#2F9E44', '#1971C2', '#F76707', '#2E5A66'
out = []
def add(s): out.append(s)
def txt(x, y, t, size=12, fill='#212529', anchor='middle', bold=False):
    add('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'
        % (x, y, size, fill, anchor, 'bold' if bold else 'normal', t))
def lbl(x, y, t, size=12, fill=RED, bg='#FFFFFF'):
    w = len(t) * size * 0.95 + 16
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="%s" fill-opacity="0.95" stroke="%s" stroke-width="1.4"/>' % (x - w / 2, y - size, w, size + 9, bg, fill))
    txt(x, y, t, size=size, fill=fill, bold=True)
def wire(pts, color, w=5.0, dots=True):
    add('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"/>'
        % (' '.join('%.1f,%.1f' % p for p in pts), color, w))
    if dots:
        for (x, y) in pts:
            add('<circle cx="%.1f" cy="%.1f" r="4.4" fill="%s" stroke="#FFFFFF" stroke-width="2"/>' % (x, y, color))
def res(x1, x2, y, label='1 kΩ'):
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="26" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.6"/>' % (x1, y - 13, x2 - x1, TEAL))
    txt((x1 + x2) / 2, y + 5, label, size=11, fill='#FFFFFF', bold=True)

def miniboard(x0, y0, cols, rows, P=46, rid='a-e', rail=False):
    w = cols * P
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="#FCFAF4" stroke="#C9BFA8" stroke-width="1.8"/>'
        % (x0 - 14, y0 - 34, w + 28, rows * P + 80, ))
    for i in range(cols):
        cx = x0 + (i + 0.5) * P
        txt(cx, y0 - 12, str(i + 1), size=10, fill='#868E96')
        for r in range(rows):
            add('<circle cx="%.1f" cy="%.1f" r="4" fill="#FFFFFF" stroke="#9A9080" stroke-width="1.1"/>' % (cx, y0 + (r + 0.5) * P))
    for r in range(rows):
        txt(x0 - 26, y0 + (r + 0.5) * P + 4, rid[r * 2:r * 2 + 1] if len(rid) >= 2 else '', size=10, fill='#868E96', anchor='end')
    if rail:
        ry = y0 + rows * P + 34
        add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (x0, ry, x0 + w, ry, '#1971C2'))
        for i in range(cols):
            add('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#FFFFFF" stroke="#1971C2" stroke-width="1.1"/>' % (x0 + (i + 0.5) * P, ry))
        txt(x0 + w + 8, ry + 5, '−  GND 轨', size=11, fill='#1971C2', anchor='start', bold=True)
        return ry
    return None

add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="%s">' % (W, H, W, H, FONT))
add('<rect width="%d" height="%d" fill="#F7F9FC"/>' % (W, H))
txt(40, 46, '电阻在面包板上的正确接法 → 报警 LED 与蜂鸣器支路', size=20, fill='#1F3864', anchor='start', bold=True)
txt(40, 74, '一条铁律：面包板"同一列的 5 个孔是同一根线（一个节点）"，所以电阻两只脚必须落在两个不同的列里，它才真的串进电路', size=12.5, fill='#667085', anchor='start')

# ---------------- 左上：规则 ✓ / ✗ ----------------
txt(60, 120, '① 先记住这一条', size=15, fill='#1F3864', anchor='start', bold=True)
miniboard(70, 170, 6, 5)
lbl(230, 430, '✗ 两只脚插在同一列 → 被短路，等于没接', size=12)
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="9 6"/>' % (70 + 1.5 * 46, 170 - 8, 46, 5 * 46, RED))
wire([(70 + 2.5 * 46, 170 + 1.5 * 46), (70 + 2.5 * 46, 170 + 3.5 * 46)], TEAL, w=4)
res(70 + 1.6 * 46, 70 + 3.4 * 46, 170 + 2.5 * 46, 'R')
txt(230, 458, '（同列上下两个孔本来就是通的）', size=10.5, fill='#868E96')
miniboard(600, 170, 6, 5)
lbl(760, 430, '✓ 两脚跨在不同列 → 真的串进去了', size=12, fill=GRN)
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="3"/>' % (600 + 1.5 * 46, 170 - 8, 46, 5 * 46, GRN))
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="none" stroke="%s" stroke-width="3"/>' % (600 + 3.5 * 46, 170 - 8, 46, 5 * 46, GRN))
res(600 + 2.4 * 46, 600 + 4.6 * 46, 170 + 2.5 * 46, '1 kΩ')
txt(760, 458, '（跨中央槽插也一样，只要两脚不同列）', size=10.5, fill='#868E96')
txt(600, 120, '② 你板上的两处电阻都按"跨两列"插', size=15, fill='#1F3864', anchor='start', bold=True)

# ---------------- 右上：报警 LED ----------------
txt(1220, 120, '③ 报警 LED 支路', size=15, fill='#1F3864', anchor='start', bold=True)
rail_y = miniboard(1240, 170, 12, 5, rail=True)
P = 46
cx = lambda c: 1240 + (c + 0.5) * P
wire([(cx(0) - 60, 170 + 2.5 * P), (cx(0), 170 + 2.5 * P)], GRN)
lbl(cx(0) - 96, 170 + 2.5 * P, 'PA7', size=12, fill=GRN)
res(cx(0) - 6, cx(3) + 6, 170 + 2.5 * P, '1 kΩ')
wire([(cx(3), 170 + 2.5 * P), (cx(4), 170 + 2.5 * P)], GRN)
add('<circle cx="%.1f" cy="%.1f" r="13" fill="#E03131"/>' % (cx(5), 170 + 2.5 * P))
add('<path d="M %.1f %.1f L %.1f %.1f" stroke="#FFFFFF" stroke-width="2.5"/>' % (cx(5) - 6, 170 + 2.5 * P - 6, cx(5) + 6, 170 + 2.5 * P + 6))
wire([(cx(4), 170 + 2.5 * P), (cx(5) - 13, 170 + 2.5 * P)], GRN)
wire([(cx(5) + 13, 170 + 2.5 * P), (cx(7), 170 + 2.5 * P)], GRN)
txt(cx(4) - 4, 170 + 2.5 * P - 26, '长脚(+)', size=10.5, fill=RED, anchor='end', bold=True)
txt(cx(6) + 4, 170 + 2.5 * P - 26, '短脚(−)', size=10.5, fill=BLK, anchor='start', bold=True)
wire([(cx(7), 170 + 2.5 * P), (cx(7), rail_y)], BLK)
lbl(cx(5), 470, '长脚在左（靠电阻一侧）：PA7→1kΩ→长脚，短脚→GND', size=12)
txt(1240, 502, '顺序反过来也可以（PA7→长脚→1kΩ→GND），电阻串在哪一端都行；但长脚必须朝"高电位"那边。', size=11, fill='#667085', anchor='start')

# ---------------- 下方：蜂鸣器 ----------------
txt(60, 610, '④ 蜂鸣器支路（你们是小模块：VCC / GND / IO 三针）', size=15, fill='#1F3864', anchor='start', bold=True)
add('<rect x="70" y="650" width="820" height="420" rx="10" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="1.6"/>')
txt(96, 686, 'A. 三针模块（你们手上这种）——不需要三极管，也不需要 1 kΩ', size=13, fill='#C92A2A', anchor='start', bold=True)
add('<rect x="130" y="740" width="200" height="120" rx="8" fill="%s" stroke="#1B3A42" stroke-width="1.8"/>' % TEAL)
txt(230, 788, '蜂鸣器模块', size=13, fill='#FFFFFF', bold=True)
txt(230, 810, 'VCC / GND / IO', size=10.5, fill='#CFE3E8')
for i, (nm, col) in enumerate((('VCC', ORG), ('GND', BLK), ('IO', GRN))):
    y = 748 + i * 40
    wire([(330, y), (450, y)], col, w=4)
    txt(344, y - 8, nm, size=11, fill=col, anchor='start', bold=True)
lbl(520, 748, '3.3V（或 5V，更响）', size=11.5, fill=ORG)
lbl(500, 788, 'GND', size=11.5, fill=BLK)
lbl(530, 828, 'PA6（原来接 1kΩ 那一列）', size=11.5, fill=GRN)
txt(96, 900, '这样接：模块自带的驱动电路会干活，电阻和三极管全部拔掉。', size=12, fill='#333333', anchor='start')
txt(96, 928, '判断极性：VCC/GND 接好后，用线把 IO 碰一下 GND——响就是低电平触发；碰 3.3V 响就是高电平触发。', size=12, fill='#333333', anchor='start')
txt(96, 956, '低电平触发的话告诉我，我把程序里 PA6 的输出极性反过来（改一行）。', size=12, fill='#333333', anchor='start')
txt(96, 1000, 'B. 若坚持用"三极管 + 裸无源蜂鸣器"：1 kΩ 必须串在 PA6 和 B 脚之间，', size=13, fill='#1F3864', anchor='start', bold=True)
txt(96, 1026, 'E→GND、C→蜂鸣器−、蜂鸣器+→3.3V；此时 1 kΩ 还是"跨两列"插（PA6 一列 → B 脚一列）。', size=12, fill='#333333', anchor='start')

# ---------------- 右下：为什么之前的可能没响 ----------------
add('<rect x="940" y="650" width="880" height="420" rx="10" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="1.6" stroke-dasharray="8 6"/>')
txt(970, 686, '⑤ 对照检查：电阻最容易错的三种插法', size=14, fill='#1F3864', anchor='start', bold=True)
items = [
 ('两只脚插进同一列', '最典型：等于短路，LED 会变得更亮或干脆不亮（看串了什么），蜂鸣器只"嗒"一声或不响'),
 ('电阻根本没串进去（跨接在两条线上）', '比如一只脚在 PA7 的列、另一只脚也在同一根线延伸的列——用万用表量两端接近 0Ω'),
 ('1 kΩ 认错（色环看错）', '1 kΩ = 棕黑红金；4.7 kΩ = 黄紫红金；10 kΩ = 棕黑橙金。插上前先认清，或用万用表量一下'),
 ('没有万用表时的替代验证', '把电阻串上一只已知好的 LED，直接碰 3.3V 和 GND：亮 = 电阻没开路；亮度明显偏暗 = 阻值偏大'),
]
for i, (a, b) in enumerate(items):
    y = 730 + i * 78
    txt(970, y, '• ' + a, size=12.5, fill='#C92A2A', anchor='start', bold=True)
    txt(990, y + 26, b, size=11.5, fill='#333333', anchor='start')
txt(970, 1040, '提示：电阻没有极性，正反插都行；插不进就稍微弯一下引脚，别硬塞。', size=11.5, fill='#868E96', anchor='start')
add('</svg>')
open('电阻接法示意.svg', 'w', encoding='utf-8').write('\n'.join(out))
print('OK -> 电阻接法示意.svg')
