# -*- coding: utf-8 -*-
"""生成《环境温度测量仪（简化版）》两块面包板版面分配图 -> 面包板版面图.svg
用法（在本目录）: python _gen_bb_layout.py
配色与《接线图.svg》保持一致（红=3.3V / 黑=GND / 橙=5V）。
"""
COL_W   = 20.0
NCOL    = 63
ML      = 72.0                     # 板内左边距（留出 a..j 行标）
MR      = 40.0
BOARD_W = NCOL * COL_W             # 1260
W       = ML + BOARD_W + MR        # 1372
FONT    = "Microsoft YaHei, SimHei, sans-serif"

ROWS_T = ['a', 'b', 'c', 'd', 'e']
ROWS_B = ['f', 'g', 'h', 'i', 'j']
ROW_H  = 20.0
ROW = {}
for i, r in enumerate(ROWS_T): ROW[r] = 96  + i * ROW_H     # 96..176
for i, r in enumerate(ROWS_B): ROW[r] = 196 + i * ROW_H     # 196..276
RULER_Y  = 24
RAIL_TOP = [48, 66]      # 上轨：3.3V / GND
RAIL_BOT = [300, 318]    # 下轨：5V(预留) / GND
BOARD_H  = 340

RED = "#E03131"; BLACK = "#212529"; ORANGE = "#F76707"; BLUE = "#4263EB"
TEAL = "#35626E"; PURPLE = "#7048E8"; GREEN = "#37B24D"; GRAY = "#8A8F98"
PINK = "#C2255C"; TITLE = "#1F3864"; SUB = "#667085"
BB_FILL = "#FCFAF4"; BB_EDGE = "#D9CCB4"; HOLE = "#DCD4C4"

def cx(c): return ML + (c - 0.5) * COL_W
def cl(c): return ML + (c - 1) * COL_W

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def txt(x, y, lines, size=11, fill=BLACK, anchor='middle', bold=False, lh=None):
    if isinstance(lines, str):
        lines = lines.split('\n')
    lh = lh or size + 2.5
    y0 = y - (len(lines) - 1) * lh / 2.0
    out = ['<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">'
           % (x, y0, size, fill, anchor, 'bold' if bold else 'normal')]
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else lh
        out.append('<tspan x="%.1f" dy="%.1f">%s</tspan>' % (x, dy, esc(ln)))
    out.append('</text>')
    return ''.join(out)

def rail(y0, y, phys, net, netcolor):
    p = ['<rect x="%.1f" y="%.1f" width="%.1f" height="14" rx="4" fill="%s" fill-opacity="0.16" stroke="%s" stroke-opacity="0.45" stroke-width="1"/>'
         % (ML - 10, y0 + y - 7, BOARD_W + 20, phys, phys)]
    for c in range(1, NCOL + 1):
        p.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#FFFFFF" stroke="%s" stroke-width="0.9" stroke-opacity="0.65"/>'
                 % (cx(c), y0 + y, phys))
    p.append(txt(ML - 4, y0 + y + 4, net, size=10, fill=netcolor, anchor='start', bold=True))
    p.append(txt(ML + BOARD_W + 4, y0 + y + 4, net, size=10, fill=netcolor, anchor='end', bold=True))
    return ''.join(p)

def zone(y0, c1, c2, r1, r2, color, label, size=11, dashed=False, solid=False):
    x = cl(c1); w = (c2 - c1 + 1) * COL_W
    y = y0 + ROW[r1] - 9; h = (ROW[r2] - ROW[r1]) + 18
    dash = ' stroke-dasharray="7 4"' if dashed else ''
    if solid:
        rect = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s" fill-opacity="0.9" stroke="%s" stroke-width="1.6"%s/>'
                % (x, y, w, h, color, color, dash))
        fg = '#FFFFFF'
    else:
        rect = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s" fill-opacity="0.12" stroke="%s" stroke-width="1.6"%s/>'
                % (x, y, w, h, color, color, dash))
        fg = color
    return rect + txt(x + w / 2.0, y + h / 2.0, label, size=size, fill=fg, bold=True)

def board(y0, title, subtitle, zones):
    p = []
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="%s" stroke="%s" stroke-width="2"/>'
             % (ML - 20, y0 - 34, BOARD_W + 40, BOARD_H + 56, BB_FILL, BB_EDGE))
    p.append(txt(ML - 6, y0 - 16, title, size=15, fill=TITLE, anchor='start', bold=True))
    p.append(txt(ML + BOARD_W + 6, y0 - 16, subtitle, size=11, fill=SUB, anchor='end'))
    # 列号尺
    for c in range(5, NCOL + 1, 5):
        p.append(txt(cx(c), y0 + RULER_Y, str(c), size=9, fill=GRAY))
    for c in range(1, NCOL + 1):
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#CFC7B6" stroke-width="0.8"/>'
                 % (cx(c), y0 + RULER_Y + 3, cx(c), y0 + RULER_Y + 8))
    # 行号
    for r in ROWS_T + ROWS_B:
        p.append(txt(ML - 26, y0 + ROW[r] + 4, r, size=9, fill=GRAY, anchor='end'))
    # 电源轨
    p.append(rail(y0, RAIL_TOP[0], RED,   '3.3V', RED))
    p.append(rail(y0, RAIL_TOP[1], BLUE,  'GND',  BLACK))
    p.append(rail(y0, RAIL_BOT[0], ORANGE, '5V 预留', ORANGE))
    p.append(rail(y0, RAIL_BOT[1], BLUE,  'GND',  BLACK))
    # 中央槽
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#E4DACA" stroke-width="2" stroke-dasharray="6 4"/>'
             % (ML - 10, y0 + 186, ML + BOARD_W + 10, y0 + 186))
    # 电源轨分段标记 ①
    xb = cl(32)
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1.2" stroke-dasharray="4 3"/>'
             % (xb, y0 + 34, xb, y0 + 80, GRAY))
    p.append(txt(xb, y0 + 30, '①', size=11, fill=GRAY, bold=True))
    # 孔阵
    p.append('<g>')
    for r in ROWS_T + ROWS_B:
        y = y0 + ROW[r]
        for c in range(1, NCOL + 1):
            p.append('<circle cx="%.1f" cy="%.1f" r="2.5" fill="#FFFFFF" stroke="%s" stroke-width="0.9"/>'
                     % (cx(c), y, HOLE))
    p.append('</g>')
    # 功能分区
    for z in zones:
        p.append(zone(y0, *z))
    return ''.join(p)

YA, YB = 160, 690
H = 1220

p = []
p.append('<?xml version="1.0" encoding="UTF-8"?>')
p.append('<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" viewBox="0 0 %.0f %.0f" font-family="%s">'
         % (W, H, W, H, FONT))
p.append('<rect x="0" y="0" width="%.0f" height="%.0f" fill="#F7F9FC"/>' % (W, H))
p.append(txt(40, 48, '环境温度测量仪（简化版）· 两块面包板版面分配图', size=25, fill=TITLE, anchor='start', bold=True))
p.append(txt(40, 78, 'A 板 = 主控与人机界面　B 板 = 传感器与模拟预留　|　本图只管「谁放在哪一段」，到脚的连线照《接线表与上机指南》',
             size=13, fill=SUB, anchor='start'))

# ---- 图例 ----
lx, ly = W - 470, 24
p.append('<rect x="%.1f" y="%.1f" width="430" height="84" rx="8" fill="#FFFFFF" stroke="#D9CCB4" stroke-width="1.2"/>' % (lx, ly))
p.append('<rect x="%.1f" y="%.1f" width="26" height="15" rx="3" fill="%s" fill-opacity="0.12" stroke="%s" stroke-width="1.6"/>' % (lx + 16, ly + 13, BLUE, BLUE))
p.append(txt(lx + 50, ly + 21, '实线框 = 本次装（简化版）', size=11, fill=BLACK, anchor='start'))
p.append('<rect x="%.1f" y="%.1f" width="26" height="15" rx="3" fill="%s" fill-opacity="0.12" stroke="%s" stroke-width="1.6" stroke-dasharray="6 3"/>' % (lx + 252, ly + 13, BLUE, BLUE))
p.append(txt(lx + 286, ly + 21, '虚线框 = 预留区', size=11, fill=BLACK, anchor='start'))
p.append(txt(lx + 16, ly + 44, '轨道约定：红轨 = 3.3V　蓝轨 = GND（板上丝印红=+、蓝=−）　橙轨 = 5V（预留）', size=11, fill=SUB, anchor='start'))
p.append(txt(lx + 16, ly + 66, '杜邦线习惯：红=3.3V　黑=GND　橙=5V　绿=信号', size=11, fill=SUB, anchor='start'))

# ---- A 板 ----
zonesA = [
    (1, 2, 'a', 'j', RED, '电源\n入口', 10, False, False),
    (3, 22, 'a', 'j', TEAL, 'U1  Blue Pill\nSTM32F103C8T6\n跨中央槽 · USB 口朝板外', 12, False, True),
    (24, 28, 'b', 'd', BLUE, 'SW1 SET\n→ PB12', 10, False, False),
    (29, 33, 'b', 'd', BLUE, 'SW2 ＋\n→ PB13', 10, False, False),
    (34, 38, 'b', 'd', BLUE, 'SW3 －\n→ PB14', 10, False, False),
    (40, 42, 'a', 'd', ORANGE, 'R10\n1kΩ', 9, False, False),
    (44, 46, 'a', 'd', ORANGE, 'Q1\nS8050', 9, False, False),
    (48, 51, 'a', 'd', ORANGE, '蜂鸣器\n无源', 9, False, False),
    (53, 55, 'a', 'd', ORANGE, '1N4148\n有则加', 9, False, False),
    (57, 63, 'a', 'd', PURPLE, 'OLED 4P 模块\n（悬出板外）', 10, False, False),
    (24, 30, 'f', 'j', PINK, '报警 LED\n1kΩ → PA7', 10, False, False),
    (32, 63, 'f', 'j', GRAY, '走线通道 / 备用（心跳灯在 Blue Pill 板上，无需接线）', 10, True, False),
]
p.append(board(YA, 'A 板（主控 · 人机界面）', '列号 1–63，两块板列号对齐', zonesA))

# ---- A↔B 桥线带 ----
by = 560
p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="62" rx="10" fill="#EEF4FF" stroke="#4263EB" stroke-width="1.4"/>'
         % (ML - 20, by, BOARD_W + 40, ))
p.append(txt(ML - 4, by + 22, 'A ↔ B 桥线（20 cm 母对母杜邦线）　现在 3 根：3.3V（红）· GND（黑）· PA1（绿，1-Wire 数据）',
             size=13, fill="#1B3A8C", anchor='start', bold=True))
p.append(txt(ML - 4, by + 44, '以后加 LM35/运放时再补 2 根：5V（橙）· PA4（黄，ADC 输入）　—　板间地线只走这一根，接在 B 板入口单点',
             size=12, fill=SUB, anchor='start'))

# ---- B 板 ----
zonesB = [
    (1, 3, 'a', 'j', RED, '入口\nA↔B 3 线', 10, False, False),
    (6, 16, 'a', 'e', GREEN, 'DS18B20 模块（3P，板载 4.7k）\nDQ → PA1 · 探头探出板外', 11, False, False),
    (19, 45, 'a', 'e', BLUE, '预留区：LM35 + MCP6002 调理电路（方案 4.3）\n加件时启用，不用重排', 11, True, False),
    (19, 45, 'f', 'j', BLUE, '预留区：AT24C02（I²C 0x50）· 第二只 DS18B20 · I²C 上拉', 11, True, False),
    (48, 63, 'a', 'j', GRAY, '留白\n走线', 10, True, False),
]
p.append(board(YB, 'B 板（传感器 · 模拟预留）', 'DS18B20 放这里，远离 Blue Pill 上的 AMS1117（发热影响测量）', zonesB))

# ---- 底部说明 ----
notes = [
    '① 830 型面包板的红/蓝电源轨多在正中（本图列号 32 附近）分成两段：跨中点要补一根跳线，别指望一侧有电全轨都有电（到手先用万用表通断档量一遍）。',
    '② Blue Pill 跨中央槽插（跨距约 8 格 / 0.8 英寸，两排脚各在槽一侧）；插前把板子虚放核对落孔，插错一排后面全乱。',
    '③ 6×6 轻触开关四脚间距 4.5 / 6.5 mm，把脚稍掰一下才进 2.54 mm 网格；无源蜂鸣器脚距 7.62 mm，正好跨 3 格；S8050 字面朝自己、引脚朝下为 E-B-C。',
    '④ 按键另一端只接 GND 即可（软件消抖已够）；想加 100 nF 硬件消抖更稳，不加也能用。蜂鸣器 1N4148 反并有就加，没有不接也能工作。',
    '⑤ B 板现在很空是正常的：留白区就是给 LM35、MCP6002、AT24C02、第二只探头预留的，以后加件不用重排。',
    '⑥ 与洞洞板版的关系：本图只是把同一套接线搬到两块面包板上先跑通；照《接线表与上机指南》逐条连线，模块引脚一律以丝印为准。',
]
p.append('<line x1="40" y1="%d" x2="%.0f" y2="%d" stroke="#D9CCB4" stroke-width="1.4"/>' % (1010, W - 40, 1010))
for i, n in enumerate(notes):
    p.append(txt(40, 1042 + i * 27, n, size=12, fill="#333333", anchor='start'))

p.append('</svg>')

with open('面包板版面图.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(p))
print('OK -> 面包板版面图.svg')
