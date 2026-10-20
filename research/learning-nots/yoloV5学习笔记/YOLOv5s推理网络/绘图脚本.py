"""Generate editable Excalidraw scenes and matching SVG previews for this note."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
INK = "#25324a"
BLUE = "#e7f1ff"
GREEN = "#e7f7ed"
ORANGE = "#fff1dd"
PURPLE = "#f0eaff"
GRAY = "#f4f6f9"


class Scene:
    def __init__(self, name, width, height):
        self.name, self.width, self.height = name, width, height
        self.elements = []
        self.svg = []
        self.seq = 0

    def _id(self):
        self.seq += 1
        return f"{self.name}-{self.seq}"

    def box(self, x, y, w, h, label, fill=BLUE, size=20, stroke=INK):
        label = re.sub(r"\(B,([0-9,]+)\)", r"Size[B,\1]", label)
        if label:
            size = min(size, int((w - 14) / (max(len(line) for line in label.split("\n")) * .62)))
        self.elements.append(dict(id=self._id(), type="rectangle", x=x, y=y, width=w, height=h,
                                  angle=0, strokeColor=stroke, backgroundColor=fill, fillStyle="solid",
                                  strokeWidth=2, strokeStyle="solid", roughness=1, opacity=100,
                                  groupIds=[], frameId=None, roundness={"type": 3}, seed=self.seq * 73,
                                  version=1, versionNonce=self.seq * 107, isDeleted=False, boundElements=None,
                                  updated=1, link=None, locked=False))
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="11" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        self.text(x + w / 2, y + h / 2, label, size=size, center=True)

    def text(self, x, y, label, size=20, center=False, color=INK):
        lines = label.split("\n")
        width = max(20, max(len(line) for line in lines) * size * .69)
        height = len(lines) * size * 1.35
        xx = x - width / 2 if center else x
        yy = y - height / 2 if center else y
        self.elements.append(dict(id=self._id(), type="text", x=xx, y=yy, width=width, height=height,
                                  angle=0, strokeColor=color, backgroundColor="transparent", fillStyle="solid",
                                  strokeWidth=1, strokeStyle="solid", roughness=0, opacity=100,
                                  groupIds=[], frameId=None, roundness=None, seed=self.seq * 73,
                                  version=1, versionNonce=self.seq * 107, isDeleted=False,
                                  boundElements=None, updated=1, link=None, locked=False,
                                  text=label, fontSize=size, fontFamily=1, textAlign="center" if center else "left",
                                  verticalAlign="middle", baseline=int(size * .8), containerId=None,
                                  originalText=label, lineHeight=1.35))
        anchor = "middle" if center else "start"
        for j, line in enumerate(lines):
            ly = y + (j - (len(lines)-1)/2) * size * 1.35 + size*.35 if center else y + (j+1)*size*1.35-size*.25
            self.svg.append(f'<text x="{x}" y="{ly:.1f}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-family="Arial, Microsoft YaHei, sans-serif">{html.escape(line)}</text>')

    def arrow(self, x1, y1, x2, y2, color=INK):
        self.elements.append(dict(id=self._id(), type="arrow", x=x1, y=y1,
                                  width=x2-x1, height=y2-y1, angle=0, strokeColor=color,
                                  backgroundColor="transparent", fillStyle="solid", strokeWidth=2,
                                  strokeStyle="solid", roughness=1, opacity=100, groupIds=[], frameId=None,
                                  roundness={"type": 2}, seed=self.seq*73, version=1,
                                  versionNonce=self.seq*107, isDeleted=False, boundElements=None,
                                  updated=1, link=None, locked=False,
                                  points=[[0,0],[x2-x1,y2-y1]], lastCommittedPoint=None,
                                  startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow", elbowed=False))
        self.svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2.2" marker-end="url(#arrow)"/>')

    def save(self):
        scene = dict(type="excalidraw", version=2, source="https://excalidraw.com",
                     elements=self.elements, appState={"gridSize": None, "viewBackgroundColor":"#ffffff"}, files={})
        (ROOT / f"{self.name}.excalidraw").write_text(json.dumps(scene, ensure_ascii=False, indent=2), encoding="utf-8")
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
               f'viewBox="0 0 {self.width} {self.height}"><defs><marker id="arrow" markerWidth="9" '
               'markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9" '
               'fill="none" stroke="#25324a" stroke-width="1.5"/></marker></defs>'
               '<rect width="100%" height="100%" fill="#fff"/>' + ''.join(self.svg) + '</svg>')
        (ROOT / f"{self.name}.svg").write_text(svg, encoding="utf-8")


def architecture():
    s = Scene("01-整体网络", 1980, 1400)
    s.text(55, 35, "YOLOv5s v6.0 · 640×640 · COCO 80 类 · PyTorch NCHW", 30)
    s.text(55, 91, "手写图的主干 → 上采样融合 → 下采样融合 → P3/P4/P5；括号为 torch.Size", 20)
    xs = [70, 520, 1020, 1510]
    for x, title, fill in zip(xs, ["输入 / Backbone", "Neck · 自顶向下", "Neck · 自底向上", "Detect"], [BLUE,GREEN,ORANGE,PURPLE]):
        s.box(x, 135, 375, 52, title, fill, 24)
    left = [
        ("输入 RGB\n(B,3,640,640)", 210),
        ("0 Conv 6×6 /2 → 32\n(B,32,320,320)", 300),
        ("1 Conv 3×3 /2 → 64\n(B,64,160,160)", 390),
        ("2 C3 ×1\n(B,64,160,160)", 480),
        ("3 Conv 3×3 /2 → 128\n(B,128,80,80)", 570),
        ("4 C3 ×2 · Backbone P3\n(B,128,80,80)", 660),
        ("5 Conv 3×3 /2 → 256\n(B,256,40,40)", 750),
        ("6 C3 ×3 · Backbone P4\n(B,256,40,40)", 840),
        ("7 Conv 3×3 /2 → 512\n(B,512,20,20)", 930),
        ("8 C3 ×1\n(B,512,20,20)", 1020),
        ("9 SPPF\n(B,512,20,20)", 1110),
    ]
    for i, (label,y) in enumerate(left):
        s.box(70,y,375,66,label,BLUE,18)
        if i: s.arrow(257, left[i-1][1]+66, 257,y)
    top = [
        ("10 Conv 1×1 → 256\n(B,256,20,20)", 1085),
        ("11 Upsample ×2\n(B,256,40,40)", 965),
        ("12 Concat [11,6]\n(B,512,40,40)", 845),
        ("13 C3 ×1 → 256\n(B,256,40,40)", 725),
        ("14 Conv 1×1 → 128\n(B,128,40,40)", 605),
        ("15 Upsample ×2\n(B,128,80,80)", 485),
        ("16 Concat [15,4]\n(B,256,80,80)", 365),
        ("17 C3 ×1 → P3/8\n(B,128,80,80)", 245),
    ]
    for i,(label,y) in enumerate(top):
        s.box(520,y,375,76,label,GREEN,18)
        if i: s.arrow(707, top[i-1][1],707,y+76)
    s.arrow(445,1143,520,1123)
    s.arrow(445,873,520,883)
    s.arrow(445,693,520,403)
    bottom = [
        ("18 Conv 3×3 /2 → 128\n(B,128,40,40)", 285),
        ("19 Concat [18,14]\n(B,256,40,40)", 425),
        ("20 C3 ×1 → P4/16\n(B,256,40,40)", 565),
        ("21 Conv 3×3 /2 → 256\n(B,256,20,20)", 705),
        ("22 Concat [21,10]\n(B,512,20,20)", 845),
        ("23 C3 ×1 → P5/32\n(B,512,20,20)", 985),
    ]
    for i,(label,y) in enumerate(bottom):
        s.box(1020,y,375,76,label,ORANGE,18)
        if i: s.arrow(1207,bottom[i-1][1]+76,1207,y)
    s.arrow(895,283,1020,323)
    s.arrow(895,643,1020,463)
    s.arrow(895,1123,1020,883)
    for label,y in [("P3 /8\n(B,128,80,80)",245),("P4 /16\n(B,256,40,40)",565),("P5 /32\n(B,512,20,20)",985)]:
        s.box(1510,y,375,76,label,PURPLE,18)
    s.arrow(895,283,1510,283)
    s.arrow(1395,603,1510,603)
    s.arrow(1395,1023,1510,1023)
    s.box(1510,1130,375,86,"24 Detect → (B,25200,85)\nNMS → 每图 (N,6)",PURPLE,18)
    s.text(1515,1080,"P3 + P4 + P5 → Detect",20)
    s.arrow(1697,1061,1697,1130)
    s.text(55,1260,"注：箭头跨行表示跨层连接；最终 P3/P4/P5 分别是第 17/20/23 层。",20)
    s.save()


def modules():
    s=Scene("02-模块内部",1800,1300)
    s.text(55,35,"Conv / Bottleneck / C3 / SPPF · 以 640×640 输入路径中的实际层为例",29)
    # Conv
    s.box(55,105,815,535,"",GRAY)
    s.text(80,120,"A. Conv：第 3 层，3×3 /2，128 通道",25)
    labels=[("输入\n(B,64,160,160)",95),("Conv2d k3 s2 p1\n(B,128,80,80)",300),("BatchNorm2d\n(B,128,80,80)",505),("SiLU\n(B,128,80,80)",710)]
    for i,(lab,x) in enumerate(labels):
        s.box(x,290,155,95,lab,BLUE,16)
        if i:s.arrow(labels[i-1][1]+155,337,x,337)
    s.text(95,450,"普通 Conv = Conv2d → BN → SiLU；输出高宽由 k / s / p 决定。",19)
    s.text(95,490,"Detect 的 1×1 预测卷积是裸 nn.Conv2d，不带 BN / SiLU。",19)
    # Bottleneck
    s.box(925,105,815,535,"",GRAY)
    s.text(950,120,"B. Bottleneck：以 Backbone C3 第 4 层内部为例",25)
    s.box(965,290,150,90,"x\n(B,64,80,80)",GREEN,17)
    s.box(1190,205,155,90,"1×1 Conv\n(B,64,80,80)",GREEN,17)
    s.box(1415,205,155,90,"3×3 Conv\n(B,64,80,80)",GREEN,17)
    s.box(1415,375,155,90,"相加 y\n(B,64,80,80)",GREEN,17)
    s.arrow(1115,325,1190,250);s.arrow(1345,250,1415,250);s.arrow(1492,295,1492,375)
    s.arrow(1115,345,1415,420)
    s.text(965,490,"仅 shortcut=True 且输入输出通道相等时，才执行 x + F(x)。",18)
    # C3
    s.box(55,675,815,570,"",GRAY)
    s.text(80,690,"C. C3：第 4 层，实际 n=2，输入输出 128 通道",24)
    s.box(95,875,130,90,"x\n(B,128,80,80)",ORANGE,16)
    s.box(285,785,145,90,"cv1 1×1\n(B,64,80,80)",ORANGE,16)
    s.box(500,785,145,90,"Bottleneck ×2\n(B,64,80,80)",ORANGE,16)
    s.box(285,1005,145,90,"cv2 1×1\n(B,64,80,80)",ORANGE,16)
    s.box(500,1005,145,90,"Concat dim=1\n(B,128,80,80)",ORANGE,16)
    s.box(680,1005,145,90,"cv3 1×1\n(B,128,80,80)",ORANGE,16)
    s.arrow(225,905,285,830);s.arrow(430,830,500,830);s.arrow(225,935,285,1050)
    s.arrow(572,875,572,1005);s.arrow(430,1050,500,1050);s.arrow(645,1050,680,1050)
    s.text(95,1160,"Neck 的 C3 结构相同，但配置 shortcut=False。",18)
    # SPPF
    s.box(925,675,815,570,"",GRAY)
    s.text(950,690,"D. SPPF：第 9 层，三个串联的 5×5 MaxPool",24)
    s.box(960,790,145,80,"输入 x\n(B,512,20,20)",PURPLE,16)
    s.box(1150,790,145,80,"cv1 1×1\n(B,256,20,20)",PURPLE,16)
    s.arrow(1105,830,1150,830)
    for i,x in enumerate([970,1170,1370]):
        s.box(x,930,150,80,f"MaxPool {i+1}\n(B,256,20,20)",PURPLE,16)
    s.arrow(1222,870,1045,930);s.arrow(1120,970,1170,970);s.arrow(1320,970,1370,970)
    s.box(1160,1080,180,90,"Concat 4 路\n(B,1024,20,20)",PURPLE,16)
    s.box(1510,1080,180,90,"cv2 1×1\n(B,512,20,20)",PURPLE,16)
    for x in [1045,1245,1445]:s.arrow(x,1010,1250,1080)
    s.arrow(1222,870,1250,1080);s.arrow(1340,1125,1510,1125)
    s.save()


def detect():
    s=Scene("03-Detect与Anchor",1850,1220)
    s.text(55,35,"Detect · 1×1 预测卷积 → reshape → 网格与 Anchor 解码 → NMS",29)
    s.text(55,82,"示例：B 张 640×640 图像；每格 3 个 Anchor；每个 Anchor 输出 85 = 4 + 1 + 80 个数",20)
    rows=[("P3 /8",128,80,10,13,205),("P4 /16",256,40,30,61,425),("P5 /32",512,20,116,90,645)]
    for name,c,n,aw,ah,y in rows:
        fill={80:GREEN,40:ORANGE,20:PURPLE}[n]
        labels=[(65,235,f"{name} 输入\n(B,{c},{n},{n})"),
                (385,245,f"1×1 Conv → 255\n(B,255,{n},{n})"),
                (715,285,f"view + permute\n(B,3,{n},{n},85)"),
                (1085,280,f"网格 / Anchor 解码\n(B,3,{n},{n},85)"),
                (1475,290,f"展平\n(B,{3*n*n},85)")]
        for i,(x,w,lab) in enumerate(labels):
            s.box(x,y,w,100,lab,fill,18)
            if i:s.arrow(labels[i-1][0]+labels[i-1][1],y+50,x,y+50)
        s.text(1100,y+112,f"首个 Anchor = ({aw},{ah}) px；stride={640//(n*1)}",16)
    s.box(120,890,270,90,"P3 grid\nSize[1,3,80,80,2]",BLUE,18)
    s.box(460,890,330,90,"P3 anchor_grid\nSize[1,3,80,80,2]",BLUE,18)
    s.box(900,870,400,125,"解码 xywh，保留 obj / cls\n(B,3,80,80,85)",GREEN,18)
    s.arrow(390,890,900,870);s.arrow(790,935,900,960)
    s.box(1430,870,320,125,"3 尺度拼接\n(B,25200,85)",PURPLE,18)
    s.arrow(1300,935,1430,935)
    s.box(1430,1050,320,90,"置信度过滤 + NMS\n每图 (N,6)",PURPLE,18)
    s.arrow(1590,995,1590,1050)
    s.text(65,1065,"xy = (2σ(txy) − 0.5 + grid) × stride",20)
    s.text(65,1100,"wh = (2σ(twh))² × anchor_grid",20)
    s.text(65,1150,"v6.0 的 grid 是整数列/行索引；anchor_grid 是像素宽高。",18)
    s.save()


if __name__ == "__main__":
    architecture(); modules(); detect()
