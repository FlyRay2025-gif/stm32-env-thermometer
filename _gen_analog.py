# -*- coding: utf-8 -*-
"""B 板模拟通道接线图（LM35 + MCP6002）-> B板模拟接线图.svg"""
W, H = 1900, 1280
FONT = "Microsoft YaHei, SimHei, sans-serif"
RED, BLK, ORG, GRN, BLU, TEAL, PUR = '#E03131', '#212529', '#F76707', '#2F9E44', '#1971C2', '#2E5A66', '#7048E8'
out = []
def add(s): out.append(s)
def txt(x, y, t, size=12, fill='#212529', anchor='middle', bold=False):
    add('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'
        % (x, y, size, fill, anchor, 'bold' if bold else 'normal', t))
def box(x1, y1, x2, y2, label, sub=None, fill=TEAL, size=13, dashed=False):
    d = ' stroke-dasharray="7 5"' if dashed else ''
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="7" fill="%s" stroke="#1B3A42" stroke-width="1.8"%s/>'
        % (x1, y1, x2 - x1, y2 - y1, fill, d))
    cx = (x1 + x2) / 2
    if sub:
        txt(cx, (y1 + y2) / 2 - 4, label, size=size, fill='#FFFFFF', bold=True)
        txt(cx, (y1 + y2) / 2 + 16, sub, size=9.5, fill='#CFE3E8')
    else:
        txt(cx, (y1 + y2) / 2 + 5, label, size=size, fill='#FFFFFF', bold=True)
def wire(pts, color, w=5.0, dash=False, dots=True):
    d = ' stroke-dasharray="9 6"' if dash else ''
    add('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"%s/>'
        % (' '.join('%.1f,%.1f' % p for p in pts), color, w, d))
    if dots:
        for (x, y) in pts:
            add('<circle cx="%.1f" cy="%.1f" r="4.4" fill="%s" stroke="#FFFFFF" stroke-width="2"/>' % (x, y, color))
def tag(x, y, t, color, side='r'):
    w = len(t) * 11 + 16
    x0 = x if side == 'r' else x - w
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="26" rx="6" fill="#FFFFFF" stroke="%s" stroke-width="1.8"/>' % (x0, y - 13, w, color))
    txt(x0 + w / 2, y + 5, t, size=12, fill=color, bold=True)

add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" font-family="%s">' % (W, H, W, H, FONT))
add('<rect width="%d" height="%d" fill="#F7F9FC"/>' % (W, H))
txt(40, 46, 'B 板模拟通道接线图：LM35 + MCP6002（把 −20～+135℃ 映射到 0～3.3V 给 PA4/ADC 采样）', size=20, fill='#1F3864', anchor='start', bold=True)
txt(40, 74, '信号：LM35(10mV/℃) → R5/R6 求和抬升 → U4B 放大 2 倍 → R9+C3 抗混叠 → PA4（ADC1_IN4）｜红=3.3V 橙=5V 黑=GND｜线交叉处不相连', size=12, fill='#667085', anchor='start')

# ---------- 器件 ----------
box(150, 590, 330, 750, 'LM35DZ', 'TO-92 · 必须 5V 供电')
wire([(330, 615), (470, 615)], ORG, w=4); txt(340, 607, '1 VCC', size=10.5, fill=ORG, anchor='start')
tag(470, 615, '5V 电源', ORG, 'r')
wire([(330, 660), (392, 660)], GRN, w=4); txt(340, 652, '2 OUT（10mV/℃）', size=10.5, fill=GRN, anchor='start')
wire([(330, 705), (430, 705)], BLK, w=4); txt(340, 697, '3 GND', size=10.5, fill=BLK, anchor='start')
tag(430, 705, 'GND', BLK, 'r')
add('<rect x="620" y="470" width="380" height="330" rx="8" fill="%s" stroke="#1B3A42" stroke-width="2"/>' % TEAL)
txt(810, 508, 'MCP6002（DIP-8）', size=15, fill='#FFFFFF', bold=True)
add('<line x1="628" y1="640" x2="992" y2="640" stroke="#9AD1D4" stroke-width="1" stroke-dasharray="5 4"/>')
txt(700, 600, 'U4A 基准缓冲', size=11, fill='#CFE3E8', bold=True)
txt(700, 700, 'U4B 偏置放大', size=11, fill='#CFE3E8', bold=True)
PINS_L = [(1, 'OUT A', 520), (2, 'IN A−', 560), (3, 'IN A+', 600), (4, 'GND', 720)]
PINS_R = [(8, 'VCC', 520), (7, 'OUT B', 560), (6, 'IN B−', 600), (5, 'IN B+', 720)]
for (no, nm, y) in PINS_L:
    wire([(620, y), (556, y)], '#1B3A42', w=4)
    txt(612, y - 7, '%d %s' % (no, nm), size=10, fill='#FFFFFF', anchor='end')
for (no, nm, y) in PINS_R:
    wire([(1000, y), (1064, y)], '#1B3A42', w=4)
    txt(1008, y - 7, '%d %s' % (no, nm), size=10, fill='#FFFFFF', anchor='start')

# ---------- 基准分压 ----------
tag(624, 240, '3.3V', RED, 'r'); wire([(660, 240), (660, 317), (700, 317)], RED)
add('<rect x="700" y="300" width="120" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(760, 323, 'R3 15k', size=12, fill='#FFFFFF', bold=True)
wire([(820, 317), (900, 317)], BLK)
add('<rect x="900" y="300" width="120" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(960, 323, 'R4 1k', size=12, fill='#FFFFFF', bold=True)
wire([(1020, 317), (1080, 317), (1080, 240)], BLK); tag(1080, 222, 'GND', BLK)

add('<rect x="540" y="330" width="140" height="30" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5" stroke-dasharray="6 4"/>' % TEAL)
txt(610, 351, 'C2 100nF', size=11, fill='#FFFFFF', bold=True)
wire([(610, 330), (610, 270)], GRN); wire([(610, 360), (610, 430)], BLK); tag(610, 448, 'GND', BLK)
wire([(860, 317), (860, 270), (500, 270), (500, 600), (556, 600)], GRN)   # V_OFF → 3 脚(U4A+)
txt(560, 505, 'V_OFF = 3.3×1/16 ≈ 0.206V', size=10.5, fill='#2F9E44', anchor='start')
wire([(556, 560), (520, 560), (520, 520), (556, 520)], GRN)   # 1↔2 短接（跟随器）

# ---------- 求和 + 放大 ----------
wire([(392, 660), (392, 620), (430, 620)], GRN)     # LM35 OUT
add('<rect x="430" y="603" width="130" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(495, 626, 'R5 10k', size=12, fill='#FFFFFF', bold=True)
wire([(560, 620), (600, 620), (600, 830), (1064, 830), (1064, 720)], GRN)   # 求和节点 → 5 脚
add('<rect x="380" y="700" width="130" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(445, 723, 'R6 10k', size=12, fill='#FFFFFF', bold=True)
wire([(510, 717), (600, 717)], GRN)
wire([(380, 717), (340, 717), (340, 460), (540, 460), (540, 520), (556, 520)], GRN)
txt(620, 866, 'V+ = (V_SEN + V_OFF)/2 （求和节点）', size=11, fill='#2F9E44', anchor='start', bold=True)
add('<rect x="1090" y="560" width="140" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(1160, 583, 'R8 30k', size=12, fill='#FFFFFF', bold=True)
wire([(1064, 600), (1090, 583)], GRN); wire([(1230, 583), (1300, 583)], GRN)
add('<rect x="1090" y="640" width="140" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(1160, 663, 'R7 10k', size=12, fill='#FFFFFF', bold=True)
wire([(1064, 600), (1064, 657), (1090, 657)], GRN); wire([(1230, 657), (1300, 657), (1300, 740)], BLK)
tag(1300, 758, 'GND', BLK)

# ---------- 输出 ----------
wire([(1064, 560), (1300, 560)], GRN); txt(1180, 548, 'Vout = 2·V_SEN + 0.4125 V', size=11, fill='#2F9E44', bold=True)
add('<rect x="1300" y="543" width="140" height="34" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(1370, 566, 'R9 100Ω', size=12, fill='#FFFFFF', bold=True)
wire([(1440, 560), (1560, 560)], BLU); tag(1600, 560, 'PA4 / ADC1_IN4', BLU, 'r')
add('<rect x="1470" y="600" width="140" height="30" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(1540, 621, 'C3 100nF', size=11, fill='#FFFFFF', bold=True)
wire([(1540, 600), (1540, 560)], BLU); wire([(1540, 630), (1540, 700)], BLK); tag(1540, 718, 'GND', BLK)
wire([(1300, 560), (1300, 583)], GRN)

# ---------- 电源 ----------
tag(700, 900, '3.3V', RED, 'r'); wire([(730, 900), (1000, 900), (1000, 520), (1064, 520)], RED)
txt(1012, 890, '运放供电 3.3V（8 脚）；4 脚接 GND', size=11, fill='#C92A2A', anchor='end')
wire([(556, 720), (500, 720), (500, 830)], BLK); tag(500, 848, 'GND', BLK)
tag(392, 615, '5V', ORG, 'r'); wire([(360, 615), (392, 615)], ORG)
add('<rect x="120" y="820" width="150" height="30" rx="5" fill="%s" stroke="#1B3A42" stroke-width="1.5"/>' % TEAL)
txt(195, 841, 'C1 100nF', size=11, fill='#FFFFFF', bold=True)
wire([(195, 820), (195, 788)], ORG); tag(195, 774, '5V', ORG); wire([(195, 850), (195, 930)], BLK); tag(195, 948, 'GND', BLK)

# ---------- DIP-8 实物脚位 ----------
add('<rect x="1560" y="120" width="300" height="200" rx="8" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="1.6"/>')
txt(1710, 144, '面包板上 DIP-8 实际脚位', size=12, fill='#1F3864', bold=True)
add('<rect x="1600" y="180" width="220" height="100" rx="6" fill="#2E5A66"/>')
for i in range(4):
    add('<circle cx="%.1f" cy="170" r="5" fill="#1B3A42"/>' % (1630 + i * 55))
    add('<circle cx="%.1f" cy="290" r="5" fill="#1B3A42"/>' % (1630 + i * 55))
for i, n in enumerate(('8', '7', '6', '5')):
    txt(1630 + i * 55, 162, n, size=12, fill='#C92A2A', bold=True)
for i, n in enumerate(('1', '2', '3', '4')):
    txt(1630 + i * 55, 312, n, size=12, fill='#C92A2A', bold=True)
add('<circle cx="1600" cy="230" r="14" fill="#FFFFFF"/>')
txt(1710, 216, '缺口朝左 · 跨中央槽', size=10.5, fill='#FFFFFF')
txt(1710, 236, '下排左起 1-4 · 上排左起 8-5', size=10.5, fill='#FFFFFF')
txt(1710, 256, '（左下角即 1 脚）', size=10.5, fill='#CFE3E8')

# ---------- 说明 ----------
add('<rect x="40" y="980" width="1820" height="270" rx="10" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="1.6" stroke-dasharray="8 6"/>')
txt(60, 1014, '原理与要点', size=15, fill='#1F3864', anchor='start', bold=True)
lines = [
 '1  为什么要这套电路：LM35 输出只有 10mV/℃，0～100℃ 才 0～1V，而且 0℃ 以下输出是负电压——STM32 的 ADC 只能测 0～3.3V，'
 '   直接接量程太小、负温还会读不了。所以用"抬升 + 放大"：把 LM35 的电压先抬到 0.4125V 起步，再放大 2 倍。',
 '2  抬升（R3/R4 + U4A）：3.3V 经 R3(15k)、R4(1k) 分压得到 0.206V，U4A 接成电压跟随器（1:1 缓冲）得到稳定的 V_OFF——'
 '   用运放跟随是为了让这个基准"带得起负载"，不被后面的求和电阻拉偏。',
 '3  求和与放大（R5/R6 + U4B）：R5、R6 各 10k，把 LM35 电压和 V_OFF 各取一半求平均 → V+ = (V_SEN + V_OFF)/2；'
 '   U4B 是同相放大，增益 = 1 + R8/R7 = 1 + 30k/10k = 4 → Vout = 4 × V+/2 = 2·V_SEN + 0.4125V。',
 '4  结果：0℃ → 0.4125V，25℃ → 0.9125V，100℃ → 2.4125V，始终落在 ADC 量程内；程序里 T = (Vout − 0.4125)/0.02 反算回温度。',
 '5  输出滤波（R9 + C3）：100Ω + 100nF 抗混叠，同时给 ADC 采样保持电容"备料"；程序里 ADC 采样时间设 239.5 周期，否则读数会偏低。',
 '6  误差大头是电阻：增益靠 R7/R8 决定，1% 电阻会带来约 2% 增益误差（25℃ 时约 0.5℃），所以 R5/R6/R7/R8 尽量用 1% 精挑配对，剩下的靠软件标定补。',
 '7  供电：LM35 必须 5V（范围 4～30V，3.3V 不够）；MCP6002 用 3.3V（8 脚），别接 5V。LM35 和运放都放 B 板下半区，地回 GND 轨单点；C1 100nF 跨在 LM35 的 5V/GND 之间去耦，C2 100nF 稳住 V_OFF 基准。',
]
for i, t in enumerate(lines):
    txt(60, 1046 + i * 29, t, size=11.5, fill='#333333', anchor='start')
add('</svg>')
open('B板模拟接线图.svg', 'w', encoding='utf-8').write('\n'.join(out))
print('OK -> B板模拟接线图.svg')
