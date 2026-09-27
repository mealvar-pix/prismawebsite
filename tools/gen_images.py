#!/usr/bin/env python3
"""Genera imágenes PLACEHOLDER para el sitio (reemplazar por fotografía real).
- hero-aerial.jpg : vista aérea procedural de parcelas agroindustriales
- band-aerial.jpg : variante para franjas (metodología / nosotros)
- cap-*.jpg       : miniaturas gráficas para las 8 capacidades
- og-image.jpg    : imagen Open Graph 1200x630
"""
import cairo, math, random, os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')
os.makedirs(OUT, exist_ok=True)


def hexc(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def to_pil(surf):
    w, h = surf.get_width(), surf.get_height()
    a = np.ndarray((h, w, 4), np.uint8, surf.get_data())
    return Image.fromarray(a[:, :, [2, 1, 0]].copy())


def aerial(W, H, seed, scale=1.0, angle=-13):
    rnd = random.Random(seed)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    c.set_source_rgb(*hexc('#6f6a52')); c.paint()
    c.translate(W / 2, H / 2); c.rotate(math.radians(angle)); c.translate(-W * .8, -H * .8)
    crops = [('#3f5d3c', 'canopy'), ('#4c6b41', 'rows'), ('#66824f', 'rows'), ('#7d8f5c', 'rows'),
             ('#8c7d5e', 'soil'), ('#557446', 'canopy'), ('#6e8a55', 'rows'), ('#9a8b68', 'soil')]
    road = hexc('#b3a888')
    y = 0
    plant_done = False
    while y < H * 1.7:
        bh = rnd.uniform(150, 260) * scale
        x = 0
        while x < W * 1.7:
            bw = rnd.uniform(200, 380) * scale
            col, kind = rnd.choice(crops)
            base = hexc(col)
            c.set_source_rgb(*base); c.rectangle(x, y, bw, bh); c.fill()
            if kind == 'rows':
                sp = rnd.uniform(5, 8) * scale
                vert = rnd.random() < .5
                c.set_line_width(sp * .45)
                dark = tuple(v * .78 for v in base)
                c.set_source_rgb(*dark)
                if vert:
                    xx = x + 2
                    while xx < x + bw:
                        c.move_to(xx, y); c.line_to(xx, y + bh); xx += sp
                else:
                    yy = y + 2
                    while yy < y + bh:
                        c.move_to(x, yy); c.line_to(x + bw, yy); yy += sp
                c.stroke()
            elif kind == 'canopy':
                n = int(bw * bh / (70 * scale * scale))
                for _ in range(n):
                    px, py = x + rnd.uniform(0, bw), y + rnd.uniform(0, bh)
                    r = rnd.uniform(3, 7) * scale
                    k = rnd.uniform(.72, 1.18)
                    c.set_source_rgba(*(min(1, v * k) for v in base), .9)
                    c.arc(px, py, r, 0, 2 * math.pi); c.fill()
            else:
                for _ in range(int(bw * bh / (400 * scale * scale))):
                    px, py = x + rnd.uniform(0, bw), y + rnd.uniform(0, bh)
                    c.set_source_rgba(*(v * rnd.uniform(.85, 1.1) for v in base), .5)
                    c.rectangle(px, py, 6 * scale, 2 * scale); c.fill()
            # packing plant
            if not plant_done and x > W * .75 and y > H * .55:
                plant_done = True
                c.set_source_rgb(*hexc('#a9a393')); c.rectangle(x, y, bw, bh); c.fill()
                for i, (dx, dy, ww, hh) in enumerate([(.08, .12, .5, .38), (.62, .12, .3, .25), (.08, .58, .35, .28)]):
                    c.set_source_rgba(0, 0, 0, .25); c.rectangle(x + bw * dx + 5, y + bh * dy + 6, bw * ww, bh * hh); c.fill()
                    c.set_source_rgb(*hexc('#dfe3e6' if i != 1 else '#c7d0d6'))
                    c.rectangle(x + bw * dx, y + bh * dy, bw * ww, bh * hh); c.fill()
                    c.set_source_rgba(0, 0, 0, .08); c.set_line_width(1.2)
                    for k in range(1, 8):
                        c.move_to(x + bw * dx + bw * ww * k / 8, y + bh * dy)
                        c.line_to(x + bw * dx + bw * ww * k / 8, y + bh * dy + bh * hh)
                    c.stroke()
                for k in range(14):
                    c.set_source_rgb(*hexc(rnd.choice(['#e9e9e4', '#6b7c8c', '#c4c9cc'])))
                    c.rectangle(x + bw * (.5 + .03 * k), y + bh * .7, bw * .02, bh * .08); c.fill()
            x += bw + 9 * scale
        y += bh + 9 * scale
    # main roads
    c.set_source_rgb(*road)
    for k in range(3):
        c.set_line_width(16 * scale)
        yy = rnd.uniform(.3, 1.3) * H
        c.move_to(-50, yy); c.curve_to(W * .5, yy + 60, W, yy - 60, W * 1.8, yy + 20); c.stroke()
    # tree lines along roads
    for k in range(260):
        px, py = rnd.uniform(0, W * 1.7), rnd.uniform(0, H * 1.7)
        c.set_source_rgba(*hexc('#2f4a31'), .85); c.arc(px, py, rnd.uniform(5, 11) * scale, 0, 2 * math.pi); c.fill()
    # canal
    c.set_source_rgb(*hexc('#5e7784')); c.set_line_width(12 * scale)
    c.move_to(W * .1, -40); c.curve_to(W * .4, H * .6, W * .2, H * 1.1, W * .7, H * 1.8); c.stroke()
    img = to_pil(s)
    arr = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(seed)
    arr += rng.normal(0, 7, arr.shape[:2])[..., None]
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))
    img = ImageEnhance.Color(img).enhance(.8)
    # cool grade
    arr = np.asarray(img).astype(np.float32)
    arr[..., 2] *= 1.06; arr[..., 0] *= .96
    # soft vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - .28 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    arr *= v[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


# ---------- capability tiles
def tile(name, motif, seed):
    W, H = 640, 360
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, W, H)
    g.add_color_stop_rgb(0, *hexc('#0B2F5B')); g.add_color_stop_rgb(1, *hexc('#15467a'))
    c.set_source(g); c.paint()
    rnd = random.Random(seed)
    lb, gr, lg = hexc('#8EC0E6'), hexc('#A7C957'), hexc('#5A8F3C')
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    if motif == 'forecast':
        for i in range(18):
            c.set_source_rgba(*lb, .12); c.set_line_width(2)
            c.move_to(0, 120 + i * 14); c.line_to(W, 60 + i * 14); c.stroke()
        pts = [(x, 250 - 90 * (x / W) - 25 * math.sin(x / 55)) for x in range(40, 420, 8)]
        c.set_source_rgba(*lb, 1); c.set_line_width(4)
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
        c.set_dash([10, 8]); c.set_source_rgba(*gr, 1)
        c.move_to(*pts[-1]); c.line_to(600, 110); c.stroke(); c.set_dash([])
        c.set_source_rgba(*gr, .18); c.move_to(pts[-1][0], pts[-1][1] - 10); c.line_to(600, 70); c.line_to(600, 150); c.close_path(); c.fill()
    elif motif == 'field':
        for j in range(4):
            x0 = 40 + j * 150
            for i in range(9):
                c.set_source_rgba(*(gr if j % 2 else lb), .35 + .05 * i); c.set_line_width(4)
                c.move_to(x0 + i * 13, 70); c.line_to(x0 - 30 + i * 13, 300); c.stroke()
        c.set_source_rgba(*gr, 1); c.arc(430, 150, 9, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(*gr, .3); c.arc(430, 150, 26, 0, 2 * math.pi); c.fill()
    elif motif == 'labor':
        for r in range(5):
            for k in range(12):
                on = rnd.random() < .7
                c.set_source_rgba(*(gr if on else lb), .9 if on else .3)
                c.arc(90 + k * 42, 80 + r * 50, 9, 0, 2 * math.pi); c.fill()
    elif motif == 'materials':
        for i in range(6):
            h = [150, 120, 170, 90, 140, 60][i]
            c.set_source_rgba(*lb, .25); c.rectangle(80 + i * 85, 300 - h, 60, h); c.fill()
            c.set_source_rgba(*lb, .9); c.set_line_width(2); c.rectangle(80 + i * 85, 300 - h, 60, h); c.stroke()
        c.set_source_rgba(*gr, 1); c.set_line_width(3); c.set_dash([8, 6])
        c.move_to(60, 190); c.line_to(600, 190); c.stroke(); c.set_dash([])
    elif motif == 'cost':
        hs = [120, 40, 30, 22, 16]
        acc = 0
        for i, h in enumerate(hs):
            c.set_source_rgba(*(lb if i == 0 else gr), .85 - i * .08)
            c.rectangle(70 + i * 95, 310 - acc - h, 60, h); c.fill()
            acc += h
        c.set_source_rgba(*lb, .95); c.set_line_width(2)
        c.rectangle(70 + 5 * 95, 310 - acc, 60, acc); c.stroke()
    elif motif == 'suppliers':
        nodes = [(rnd.uniform(60, 580), rnd.uniform(60, 300)) for _ in range(14)]
        hub = (320, 180)
        for n in nodes:
            c.set_source_rgba(*lb, .35); c.set_line_width(1.5); c.move_to(*n); c.line_to(*hub); c.stroke()
            c.set_source_rgba(*lb, .9); c.arc(*n, 5, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(*gr, 1); c.arc(*hub, 12, 0, 2 * math.pi); c.fill()
    elif motif == 'cash':
        pts = [(x, 200 - 70 * math.sin(x / 90) + 20 * math.sin(x / 23)) for x in range(40, 610, 6)]
        c.move_to(40, 300); [c.line_to(*p) for p in pts]; c.line_to(604, 300); c.close_path()
        c.set_source_rgba(*lb, .2); c.fill()
        c.set_source_rgba(*lb, 1); c.set_line_width(3.5); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.stroke()
        c.set_source_rgba(*gr, .9); c.set_line_width(2); c.set_dash([6, 6]); c.move_to(40, 215); c.line_to(604, 215); c.stroke()
    elif motif == 'data':
        for r in range(7):
            for k in range(14):
                v = rnd.random()
                c.set_source_rgba(*(gr if v > .85 else lb), .15 + .6 * v)
                c.rectangle(60 + k * 38, 50 + r * 38, 30, 30); c.fill()
    to_pil(s).save(os.path.join(OUT, f'cap-{name}.jpg'), quality=84)


if __name__ == '__main__':
    aerial(2400, 1400, 11).save(os.path.join(OUT, 'hero-aerial.jpg'), quality=80, optimize=True, progressive=True)
    aerial(1600, 1000, 23, scale=1.5, angle=8).save(os.path.join(OUT, 'band-aerial.jpg'), quality=80, optimize=True, progressive=True)
    for i, (n, m) in enumerate([('produccion', 'forecast'), ('agronomia', 'field'), ('mano-de-obra', 'labor'),
                                ('materiales', 'materials'), ('costos', 'cost'), ('compras', 'suppliers'),
                                ('finanzas', 'cash'), ('datos', 'data')]):
        tile(n, m, i + 3)
    # OG image
    base = Image.open(os.path.join(OUT, 'hero-aerial.jpg')).resize((1200, 700)).crop((0, 35, 1200, 665))
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 630)
    c = cairo.Context(s)
    arr = np.asarray(base.convert('RGBA'))[:, :, [2, 1, 0, 3]].copy()
    img = cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, 1200, 630)
    c.set_source_surface(img); c.paint()
    g = cairo.LinearGradient(0, 0, 1200, 0)
    g.add_color_stop_rgba(0, *hexc('#0B2F5B'), .96); g.add_color_stop_rgba(.6, *hexc('#0B2F5B'), .8); g.add_color_stop_rgba(1, *hexc('#0B2F5B'), .35)
    c.set_source(g); c.paint()
    # prism mark
    c.set_source_rgb(*hexc('#8EC0E6')); c.move_to(80, 170); c.line_to(125, 92); c.line_to(170, 170); c.close_path(); c.fill()
    c.set_source_rgb(*hexc('#A7C957')); c.move_to(125, 92); c.line_to(170, 170); c.line_to(138, 170); c.close_path(); c.fill()
    c.select_font_face('Montserrat', 0, 1); c.set_font_size(44); c.set_source_rgb(1, 1, 1)
    c.move_to(192, 150); c.show_text('PRISMA')
    c.select_font_face('Montserrat SemiBold', 0, 0); c.set_font_size(15); c.set_source_rgb(*hexc('#8EC0E6'))
    c.move_to(194, 176); c.show_text('I N T E L I G E N T E')
    c.select_font_face('Montserrat', 0, 1); c.set_font_size(60); c.set_source_rgb(1, 1, 1)
    c.move_to(80, 330); c.show_text('Vea su operación')
    c.move_to(80, 405); c.show_text('desde otra perspectiva.')
    c.select_font_face('Montserrat SemiBold', 0, 0); c.set_font_size(22); c.set_source_rgb(*hexc('#A7C957'))
    c.move_to(82, 480); c.show_text('CAMPO  |  DATOS  |  ESTRATEGIA  |  RESULTADOS')
    to_pil(s).save(os.path.join(OUT, 'og-image.jpg'), quality=85)
    print(sorted(os.listdir(OUT)))
