# -*- coding: utf-8 -*-
"""生成《环境温度测量仪（简化版）》两块面包板的接线图（仿江协接线图风格）
用法（本目录）: python _gen_wiring.py   ->  面包板接线图.svg
"""
P = 30.0                    # 孔间距
X0 = 46.0                   # 板左边缘
COLS_A, COLS_B = 50, 24
W, H = 1900, 1500
Y0A, Y0B = 170.0, 827.0     # 两块板顶部的绝对 y
ROWS = {'a':100,'b':130,'c':160,'d':190,'e':220,'f':280,'g':310,'h':340,'i':370,'j':400}
RT1, RT2, RB1, RB2 = 28, 58, 444, 474      # 上+行 / 上-行 / 下+行 / 下-行（相对）
RLT, RBT = '#E03131', '#1971C2'            # 轨道线颜色（红=+，蓝=-）
RED, BLK, GRN, BLU, ORG = '#E03131', '#212529', '#2F9E44', '#1971C2', '#F76707'
DARK, LIGHT = '#2E5A66', '#FCFAF4'
FONT = "Microsoft YaHei, SimHei, sans-serif"

def px(c): return X0 + (c - 0.5) * P
def A(c, r): return (px(c), Y0A + ROWS[r])
def B(c, r): return (px(c), Y0B + ROWS[r])
ry = lambda r: Y0A + ROWS[r]
BY = lambda r: Y0B + ROWS[r]
def e(s): return s.replace('&', '&amp;').replace('<', '&lt;')

out = []
def add(s): out.append(s)
def txt(x, y, t, size=11, fill='#212529', anchor='middle', bold=False, rot=None):
    tr = ' transform="rotate(%d %.1f %.1f)"' % (rot, x, y) if rot is not None else ''
    add('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s"%s>%s</text>'
        % (x, y, size, fill, anchor, 'bold' if bold else 'normal', tr, e(t)))

def lbl(x, y, t, size=11, fill='#212529', bg='#FFFFFF', bold=True):
    w = len(t) * (size * 0.95 if any('\u4e00' <= ch <= '\u9fff' for ch in t) else size * 0.62) + 10
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s" fill-opacity="0.92" stroke="%s" stroke-opacity="0.35"/>'
        % (x - w / 2, y - size - 2, w, size + 8, bg, fill))
    txt(x, y, t, size=size, fill=fill, bold=bold)

def wire(pts, color, w=5.0, dash=False, dots=True):
    d = ' stroke-dasharray="9 6"' if dash else ''
    add('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"%s/>'
        % (' '.join('%.1f,%.1f' % p for p in pts), color, w, d))
    if dots:
        for (x, y) in pts:
            add('<circle cx="%.1f" cy="%.1f" r="4.6" fill="%s" stroke="#FFFFFF" stroke-width="2"/>' % (x, y, color))

def part(x1, y1, x2, y2, label, sub=None, size=12, dashed=False, fill=DARK):
    d = ' stroke-dasharray="7 5"' if dashed else ''
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s" stroke="#1B3A42" stroke-width="1.6"%s/>'
        % (x1, y1, x2 - x1, y2 - y1, fill, d))
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    if sub:
        txt(cx, cy - 4, label, size=size, fill='#FFFFFF', bold=True)
        txt(cx, cy + 14, sub, size=9, fill='#CFE3E8')
    else:
        txt(cx, cy + 4, label, size=size, fill='#FFFFFF', bold=True)

def board(y0, cols, title, subtitle):
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="%s" stroke="#C9BFA8" stroke-width="2"/>'
        % (X0 - 8, y0 - 16, cols * P + 16, 521, LIGHT))
    txt(X0 - 6, y0 - 26, title, size=15, fill='#1F3864', anchor='start', bold=True)
    txt(X0 + cols * P, y0 - 26, subtitle, size=11, fill='#667085', anchor='end')
    # 列号
    for c in range(5, cols + 1, 5):
        txt(px(c), y0 - 4, str(c), size=9, fill='#868E96')
    # 行号
    for r, dy in ROWS.items():
        txt(X0 - 14, y0 + dy + 4, r, size=9, fill='#868E96', anchor='end')
    # 轨道
    for y, col, sign in ((RT1, RLT, '+'), (RT2, RLT, 'n'), (RB1, RLT, '+'), (RB2, RLT, 'n')):
        pass
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (X0, y0 + 14, X0 + cols * P, y0 + 14, RLT))
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (X0, y0 + 72, X0 + cols * P, y0 + 72, RLT))
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (X0, y0 + 430, X0 + cols * P, y0 + 430, RLT))
    add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.6"/>' % (X0, y0 + 488, X0 + cols * P, y0 + 488, RLT))
    for c in range(1, cols + 1):
        for dy in (RT1, RT2, RB1, RB2):
            add('<circle cx="%.1f" cy="%.1f" r="3" fill="#FFFFFF" stroke="%s" stroke-width="1.1"/>' % (px(c), y0 + dy, RLT))
    # 孔阵
    for r, dy in ROWS.items():
        for c in range(1, cols + 1):
            add('<circle cx="%.1f" cy="%.1f" r="2.6" fill="#FFFFFF" stroke="#9A9080" stroke-width="0.9"/>' % (px(c), y0 + dy))
    txt(X0 + cols * P - 4, y0 + 20, '+', size=13, fill=RLT, anchor='end', bold=True)
    txt(X0 + cols * P - 4, y0 + 68, '-', size=15, fill=RLT, anchor='end', bold=True)
    txt(X0 + cols * P - 4, y0 + 436, '+', size=13, fill=RLT, anchor='end', bold=True)
    txt(X0 + cols * P - 4, y0 + 484, '-', size=15, fill=RLT, anchor='end', bold=True)

# ================= 画布 =================
add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="%s">' % (W, H, W, H, FONT))
add('<rect width="%d" height="%d" fill="#F7F9FC"/>' % (W, H))
txt(40, 44, '环境温度测量仪 · 两块面包板接线图（当前器件：Blue Pill / OLED / DS18B20 / 蜂鸣器 / 报警LED / 3 按键）', size=20, fill='#1F3864', anchor='start', bold=True)
txt(40, 70, 'A 板 = 主控与人机界面　B 板 = 传感器（下半区预留 LM35/运放）｜ 线交叉处不相连，模块引脚顺序一律以丝印为准', size=12, fill='#667085', anchor='start')
board(Y0A, COLS_A, 'A 板', 'USB 口朝左（插线到电脑：供电 + 串口 115200）')
board(Y0B, COLS_B, 'B 板', '')

# ============ A 板：Blue Pill ============
TOP = ['G','G','3.3','R','B11','B10','B1','B0','A7','A6','A5','A4','A3','A2','A1','A0','C15','C14','C13','VB']
BOT = ['B12','B13','B14','B15','A8','A9','A10','A11','A12','A15','B3','B4','B5','B6','B7','B8','B9','5V','G','3.3']
USED = {'G','3.3','A7','A6','A1','B12','B13','B14','B6','B7','5V'}
bx1, bx2 = px(2.6), px(22.4)
by1, by2 = Y0A + ROWS['a'], Y0A + ROWS['h']
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s" stroke="#1B3A42" stroke-width="2"/>'
    % (bx1, by1, bx2 - bx1, by2 - by1, DARK))
txt((bx1 + bx2) / 2, (by1 + by2) / 2 - 6, 'STM32最小系统板', size=15, fill='#FFFFFF', bold=True)
txt((bx1 + bx2) / 2, (by1 + by2) / 2 + 14, 'STM32F103C8T6（Blue Pill）', size=10, fill='#CFE3E8')
for i, name in enumerate(TOP):
    x = px(3 + i)
    add('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#1B3A42" stroke="#FFFFFF" stroke-width="1"/>' % (x, by1))
    txt(x + 4, by1 + 12, name, size=9, fill=('#FFD43B' if name in USED else '#D9E4E8'), anchor='end', rot=-90)
for i, name in enumerate(BOT):
    x = px(3 + i)
    add('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#1B3A42" stroke="#FFFFFF" stroke-width="1"/>' % (x, by2))
    txt(x + 4, by2 - 12, name, size=9, fill=('#FFD43B' if name in USED else '#D9E4E8'), anchor='start', rot=-90)
lbl(px(13), ry('a') - 26, 'USB 口 → 电脑（供电 + 串口）', size=10, fill='#495057', bg='#FFF3BF')
add('<path d="M %.1f %.1f L %.1f %.1f" stroke="#495057" stroke-width="1.6"/>' % (px(16), ry('a') - 20, bx1 + 30, by1 - 4))

# ============ A 板：接线 ============
ar = 'MARKER'
wire([A(5,'a'), (px(5), Y0A + RT1)], RED)                      # 上轨 3.3V
wire([A(3,'a'), (px(3), Y0A + RT2)], BLK)                      # 上轨 GND
wire([A(22,'h'), (px(22), Y0A + RB1)], RED)                    # 下轨 3.3V
wire([A(21,'h'), (px(21), Y0A + RB2)], BLK)                    # 下轨 GND
# 蜂鸣器支路：PA6 → R10 → Q1(B)；Q1(C) → 蜂鸣器(−)；蜂鸣器(+) → 上+轨；Q1(E) → 上−轨
wire([A(12,'a'), (px(12), Y0A + 86), (px(24), Y0A + 86), (px(24), Y0A + ROWS['b'])], GRN)
wire([(px(26), Y0A + ROWS['b']), (px(28), Y0A + ROWS['b']), (px(28), Y0A + ROWS['c'])], GRN)
wire([(px(27), Y0A + ROWS['c']), (px(27), Y0A + RT2)], BLK)
wire([(px(29), Y0A + ROWS['c']), (px(31), Y0A + ROWS['c'])], GRN)
wire([(px(33), Y0A + ROWS['c']), (px(33), Y0A + RT1)], RED)
wire([(px(31), Y0A + ROWS['d']), (px(31), Y0A + ROWS['c'])], ORG, dash=True)
wire([(px(33), Y0A + ROWS['d']), (px(33), Y0A + ROWS['c'])], ORG, dash=True)
# 报警 LED：PA7 → R11 → LED 长脚；短脚 → 上−轨
wire([A(11,'a'), (px(11), Y0A + 78), (px(44), Y0A + 78), (px(44), Y0A + ROWS['c'])], GRN)
wire([(px(46), Y0A + ROWS['c']), (px(48), Y0A + ROWS['c'])], GRN)
wire([(px(50), Y0A + ROWS['c']), (px(50), Y0A + RT2)], BLK)
# 按键：左端 → PB12/13/14（第 3/4/5 列）；右端 → GND 总线 → 上−轨
wire([(px(24), Y0A + ROWS['f']), (px(24), Y0A + ROWS['j']), (px(3), Y0A + ROWS['j'])], GRN)
wire([(px(28), Y0A + ROWS['f']), (px(28), Y0A + ROWS['j'] - 8), (px(4), Y0A + ROWS['j'] - 8)], GRN)
wire([(px(32), Y0A + ROWS['f']), (px(32), Y0A + ROWS['j'] + 8), (px(5), Y0A + ROWS['j'] + 8)], GRN)
wire([(px(23), Y0A + RT2), (px(23), Y0A + ROWS['e']), (px(34), Y0A + ROWS['e'])], BLK)
for c in (26, 30, 34):
    wire([(px(c), Y0A + ROWS['f']), (px(c), Y0A + ROWS['e'])], BLK)
# OLED：GND→上−轨、VCC→上+轨、SCL→PB6(第16列)、SDA→PB7(第17列)
wire([(px(37), Y0A + ROWS['d']), (px(37), Y0A + RT2)], BLK)
wire([(px(38), Y0A + ROWS['d']), (px(38), Y0A + RT1)], RED)
wire([(px(39), Y0A + ROWS['d']), (px(39), Y0A + ROWS['c'] - 7), (px(35), Y0A + ROWS['c'] - 7), (px(35), Y0A + ROWS['i'] - 6), (px(16), Y0A + ROWS['i'] - 6)], BLU)
wire([(px(40), Y0A + ROWS['d']), (px(40), Y0A + ROWS['c'] + 7), (px(36), Y0A + ROWS['c'] + 7), (px(36), Y0A + ROWS['i'] + 6), (px(17), Y0A + ROWS['i'] + 6)], BLU)

# ============ A 板：器件 ============
def small(x1, y1, x2, y2, label, sub=None, color='#3B6E7C', dashed=False, ts=10):
    d = ' stroke-dasharray="6 5"' if dashed else ''
    x1, x2 = x1 + 5, x2 - 5
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"%s/>'
        % (x1, y1, x2 - x1, y2 - y1, color, d))
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    txt(cx, cy + (10 if sub else 4), label, size=ts, fill='#FFFFFF', bold=True)
    if sub:
        txt(cx, cy - 5, sub, size=8.5, fill='#CFE3E8')

def pin(x, y, t, side='r', color='#FFD43B'):
    add('<circle cx="%.1f" cy="%.1f" r="3.2" fill="#1B3A42" stroke="#FFFFFF" stroke-width="1"/>' % (x, y))
    dx, anc, rot = (18, 'start', -90) if side == 'r' else (-18, 'end', 90)
    txt(x + dx, y - 4, t, size=9, fill=color, anchor=anc, rot=rot)

ry = lambda r: Y0A + ROWS[r]
small(px(24) - 12, ry('b') - 9, px(26) + 12, ry('b') + 9, 'R10', '1 kΩ')
small(px(27) - 12, ry('c') - 11, px(29) + 12, ry('c') + 11, 'Q1', 'S8050')
pin(px(27), ry('c'), 'E', 'l'); pin(px(28), ry('c'), 'B', 'r'); pin(px(29), ry('c'), 'C', 'r')
small(px(31) - 10, ry('c') - 13, px(33) + 10, ry('c') + 13, '蜂鸣器', '无源 3.3V')
pin(px(31), ry('c'), '+', 'l'); pin(px(33), ry('c'), '−', 'r')
small(px(31) - 10, ry('d') - 11, px(33) + 10, ry('d') + 11, '1N4148', '可选', dashed=True, ts=9)
small(px(44) - 12, ry('c') - 9, px(46) + 12, ry('c') + 9, 'R11', '1 kΩ')
small(px(48) - 12, ry('c') - 11, px(50) + 12, ry('c') + 11, 'LED', '红 · 长脚在左')
for i, (nm, sub) in enumerate((('SW1', 'SET'), ('SW2', '＋'), ('SW3', '－'))):
    c = 25 + i * 4
    small(px(c) - 16, ry('f') - 12, px(c) + 16, ry('f') + 12, nm, sub, color='#2B4E8C', ts=11)
lbl(px(24), ry('b') - 26, '蜂鸣器驱动：PA6→R10→B，E→GND，C→蜂鸣器−，蜂鸣器+→3.3V', size=10, fill=ORG)
lbl(px(46), ry('c') - 30, 'LED：PA7→R11→长脚，短脚→GND', size=10, fill=ORG)
lbl(px(28), ry('f') - 30, '按键：左端→PB12/13/14，右端→GND', size=10, fill='#1B3A8C')
# OLED 模块本体（悬出板外）
add('<rect x="%.1f" y="%.1f" width="170" height="300" rx="8" fill="%s" fill-opacity="0.92" stroke="#1B3A42" stroke-width="2"/>'
    % (px(36.9), Y0A + ROWS['e'] - 10, DARK))
txt(px(36.9) + 85, Y0A + ROWS['e'] + 130, 'OLED', size=14, fill='#FFFFFF', bold=True)
txt(px(36.9) + 85, Y0A + ROWS['e'] + 150, '0.96″ I²C', size=9, fill='#CFE3E8')
for i, nm in enumerate(('GND', 'VCC', 'SCL', 'SDA')):
    x = px(37 + i)
    add('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#1B3A42" stroke="#FFFFFF" stroke-width="1"/>' % (x, Y0A + ROWS['d']))
    txt(x + 24, Y0A + ROWS['d'] - 6, nm, size=9, fill='#FFD43B', anchor='start', rot=-90)
lbl(1450, 750, 'OLED 的 SCL→PB6 列、SDA→PB7 列（别照教程图接 PB8/PB9，否则全黑）', size=11, fill='#C92A2A', bg='#FFF0F0')
txt(px(3) + 4, Y0A + ROWS['a'] + 6, '5V（留给 LM35）', size=9, fill='#F76707', anchor='start', rot=-90)
lbl(px(13), Y0A + ROWS['i'] + 40, '下半区留白：走线通道 / 以后加件', size=10, fill='#868E96', bg='#F8F9FA')

# ============ A↔B 桥线（3 根） ============
wire([(px(1), Y0A + RT1), (26, Y0A + RT1), (26, Y0B + RT1), (px(1), Y0B + RT1)], RED)
wire([(px(1), Y0A + RT2), (14, Y0A + RT2), (14, Y0B + RT2), (px(1), Y0B + RT2)], BLK)
wire([A(17, 'a'), (px(17), Y0A + 88), (38, Y0A + 88), (38, Y0B + ROWS['b']), B(3, 'b'), B(9, 'b'), B(9, 'c')], GRN)
lbl(430, 706, 'A↔B 桥线 5 根：3.3V（红）· GND（黑）· PA1（绿）· 5V（橙）· PA4（蓝，模拟输出）', size=11, fill='#1B3A8C', bg='#EEF4FF')

wire([A(20, 'h'), (px(20), ry('j')), (px(2), ry('j')), (10, ry('j')), (10, Y0B + RB1), (px(1), Y0B + RB1)], ORG)
wire([A(14, 'a'), (px(14), ry('a') - 12), (6, ry('a') - 12), (6, Y0B + ROWS['h']), (px(3), Y0B + ROWS['h'])], BLU)
lbl(150, Y0B + ROWS['i'] + 46, '→ PA4（运放输出）', size=10, fill='#1971C2')
lbl(150, Y0B + ROWS['j'] + 74, '→ 5V（LM35 供电）', size=10, fill='#F76707')
# ============ B 板：器件与接线 ============
BX = lambda c: px(c)
lbl(BX(2), Y0B + RT1 - 26, '入口', size=11, fill='#C92A2A')
part(BX(6), Y0B + ROWS['b'] - 16, BX(14) + 16, Y0B + ROWS['d'] + 16, 'DS18B20 模块', '板载 4.7k 上拉 · 引脚以丝印为准')
for i, nm in enumerate(('VCC', 'DQ', 'GND')):
    x = BX(8 + i)
    add('<circle cx="%.1f" cy="%.1f" r="3.4" fill="#1B3A42" stroke="#FFFFFF" stroke-width="1"/>' % (x, Y0B + ROWS['c']))
    txt(x + 4, Y0B + ROWS['c'] - 40, nm, size=9, fill='#FFD43B', anchor='start', rot=-90)
wire([(BX(8), Y0B + ROWS['c']), (BX(8), Y0B + RT1)], RED)
wire([(BX(10), Y0B + ROWS['c']), (BX(10), Y0B + RT2)], BLK)
add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="#F1F3F5" stroke="#ADB5BD" stroke-width="1.6" stroke-dasharray="8 6"/>'
    % (BX(5) - 10, Y0B + ROWS['g'] - 26, 11 * P, 120))
txt(BX(10), Y0B + ROWS['g'] + 20, '模拟通道也接在 B 板下半区：LM35 + MCP6002 + 7 只电阻', size=11, fill='#667085', bold=True)
txt(BX(10), Y0B + ROWS['g'] + 42, '详细接线见《B板模拟接线图》｜DS18B20 探头探出板外，远离稳压器发热区', size=10, fill='#868E96')

# ============ ST-Link 小图 ============
sx, sy = 1600, 150
add('<rect x="%.1f" y="%.1f" width="270" height="190" rx="8" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="1.6"/>' % (sx, sy))
txt(sx + 12, sy + 24, 'ST-Link 接法（插板上 SWD 4 针，不经过面包板）', size=11, fill='#1F3864', anchor='start', bold=True)
add('<rect x="%.1f" y="%.1f" width="86" height="80" rx="5" fill="%s"/>' % (sx + 16, sy + 46, DARK))
txt(sx + 59, sy + 90, 'Blue Pill', size=10, fill='#FFFFFF', bold=True)
add('<rect x="%.1f" y="%.1f" width="86" height="80" rx="5" fill="#7048E8"/>' % (sx + 168, sy + 46))
txt(sx + 211, sy + 90, 'ST-Link V2', size=10, fill='#FFFFFF', bold=True)
for i, (nm, col, dash) in enumerate((('SWDIO', '#2F9E44', False), ('SWCLK', '#1971C2', False), ('GND', '#212529', False), ('3.3V', '#E03131', True))):
    y = sy + 60 + i * 18
    wire([(sx + 102, y), (sx + 168, y)], col, w=3.6, dash=dash, dots=True)
    txt(sx + 124, y - 4, nm, size=9, fill=col, bold=True)
txt(sx + 12, sy + 176, 'USB 供电时：3.3V 可不接（虚线），只留 3 根', size=10, fill='#667085', anchor='start')

# ============ 说明 ============
nx, ny = 830, 880
add('<rect x="%.1f" y="%.1f" width="1040" height="420" rx="10" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="1.6" stroke-dasharray="8 6"/>' % (nx, ny))
txt(nx + 16, ny + 30, '接线要点（对照《接线表与上机指南》）', size=14, fill='#1F3864', anchor='start', bold=True)
notes = [
    '1  引脚对应：PA1=DS18B20 的 DQ；PB6=OLED 的 SCL、PB7=SDA；PA6=蜂鸣器；PA7=报警 LED；PB12/13/14=三个按键。',
    '2  OLED 的 SCL/SDA 必须落在 PB6、PB7 这两列上——网上教程图是 PB8/PB9（教程代码的脚），照抄会全黑。',
    '3  电源：USB 线接电脑（同时供电和串口 115200）；两块板的电源轨已分别接好，上下两组轨互相独立。',
    '4  B 板：DS18B20 + 模拟通道（LM35/MCP6002，详见《B板模拟接线图》）；A/B 之间共 5 根桥线。',
    '5  红=3.3V、黑=GND、绿=信号、蓝=I²C；线交叉处不相连；所有模块引脚顺序一律以实物丝印为准。',
    '6  上电自检会显示 DS18B20 ERROR / LM35 乱值——因为器件还没接全，属正常现象，不是故障。',
]
for i, t in enumerate(notes):
    txt(nx + 16, ny + 62 + i * 30, t, size=11.5, fill='#333333', anchor='start')
txt(nx + 16, ny + 268, '电源轨提示：830 板每侧的电源轨在正中常被分成两段，跨过中点要补一根跳线；', size=11.5, fill='#C92A2A', anchor='start')
txt(nx + 16, ny + 292, '本图两块板上下各有一条 3.3V 轨和 GND 轨，都已从 Blue Pill 的对应引脚引出，不用再跨中点。', size=11.5, fill='#C92A2A', anchor='start')
txt(nx + 16, ny + 330, '焊洞洞板时按《接线表与上机指南》来，引脚与面包板版完全一致（PB6/PB7）。', size=11.5, fill='#333333', anchor='start')
txt(nx + 16, ny + 366, '本图由 _gen_wiring.py 生成（可改版重跑）。', size=10, fill='#ADB5BD', anchor='start')

add('</svg>')
with open('面包板接线图.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('OK -> 面包板接线图.svg')
