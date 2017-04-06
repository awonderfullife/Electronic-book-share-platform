from PIL import Image, ImageDraw, ImageFont
import json
import os

f = open('data2.json', 'r')
root = json.loads(f.read())
f.close()

bbox = [0.0, 0.0, 2560000.0, 2560000.0]


def normalize(x, y, r, scale):
    x = float(x)
    y = float(y)
    r = float(r)
    x1 = ((x - r) - bbox[0]) / (bbox[2] - bbox[0]) * scale
    y1 = ((y - r) - bbox[1]) / (bbox[3] - bbox[1]) * scale
    x2 = ((x + r) - bbox[0]) / (bbox[2] - bbox[0]) * scale
    y2 = ((y + r) - bbox[1]) / (bbox[3] - bbox[1]) * scale
    return [x1, y1, x2, y2]


def judge(b, n):
    s = set()
    x1 = int(b[0] / 256)
    y1 = int(b[1] / 256)
    x2 = int(b[2] / 256)
    y2 = int(b[3] / 256)
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            s.add(i * n + j)  # per pixel independent coding
    return s


for level in range(0, 4):
    n = int(pow(2, level))
    if not os.path.exists("img/%d" % level):
        os.makedirs("img/%d" % level)
    ellipses = {}
    texts = {}
    for i in range(0, n * n):
        ellipses[i] = []
        texts[i] = []
    for L0 in root['child']:
        if level < 4:
            im = Image.new("RGB", (256, 256), "#ffffff")
            draw = ImageDraw.Draw(im)
            b = normalize(L0['x'], L0['y'], L0['r'], 256 * n)
            font_size = int((b[2] - b[0]) / 10)
            font = ImageFont.truetype("arial.ttf", font_size)
            w, h = draw.textsize(L0['name'], font)
            center = [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]
            s = judge([center[0] - w / 2, center[1] - h / 2, center[0] + w / 2,
                       center[1] + h / 2], n)
            for i in s:
                texts[i].append([center, font_size, L0['name']])
        for L1 in L0['child']:
            if 4 <= level < 7:
                im = Image.new("RGB", (256, 256), "#ffffff")
                draw = ImageDraw.Draw(im)
                b = normalize(L1['x'], L1['y'], L1['r'], 256 * n)
                font_size = int((b[2] - b[0]) / 10)
                font = ImageFont.truetype("arial.ttf", font_size)
                w, h = draw.textsize(L1['name'], font)
                center = [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]
                s = judge(
                    [center[0] - w / 2, center[1] - h / 2, center[0] + w / 2,
                     center[1] + h / 2], n)
                for i in s:
                    texts[i].append([center, font_size, L1['name']])

            for p in L1['papers']:
                b = normalize(p['x'], p['y'], p['r'], 256 * n)
                s = judge(b, n)
                for i in s:
                    if level < 4:
                        ellipses[i].append([b, L0['color']])
                    elif level < 7:
                        ellipses[i].append([b, L1['color']])
                    else:
                        ellipses[i].append([b, p['color']])
                        im = Image.new("RGB", (256, 256), "#ffffff")
                        draw = ImageDraw.Draw(im)
                        tb = normalize(p['x'], p['y'], p['r'], 256 * n)
                        font_size = int((tb[2] - tb[0]) / 10)
                        font = ImageFont.truetype("arial.ttf", font_size)
                        w, h = draw.textsize(p['author'], font)
                        center = [(tb[0] + tb[2]) / 2, (tb[1] + tb[3]) / 2]
                        ts = judge([center[0] - w / 2, center[1] - h / 2,
                                    center[0] + w / 2, center[1] + h / 2], n)
                        for i in ts:
                            texts[i].append([center, font_size, p['author']])

    for i in range(0, n):
        if not os.path.exists("img/%d/%d" % (level, i)):
            os.mkdir("img/%d/%d" % (level, i))
        for j in range(0, n):
            im = Image.new("RGB", (256, 256), "#ffffff")
            draw = ImageDraw.Draw(im)
            for e in ellipses[i * n + j]:
                draw.ellipse(
                    [e[0][0] - 256 * i, e[0][1] - 256 * j, e[0][2] - 256 * i,
                     e[0][3] - 256 * j], fill=e[1])
            for t in texts[i * n + j]:
                font = ImageFont.truetype("arial.ttf", t[1])
                w, h = draw.textsize(t[2], font)
                draw.text(
                    [t[0][0] - w / 2 - 256 * i, t[0][1] - h / 2 - 256 * j],
                    t[2], fill="#000000", font=font)
            del draw
            im.save("img/%d/%d/%d.png" % (level, i, j), "PNG")
    print "level %d has done!" % level
