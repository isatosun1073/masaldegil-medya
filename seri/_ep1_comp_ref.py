import numpy as np, cv2, subprocess, sys, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 24
LS = 1.25; MX, MY = 108, 192   # layer pixel scale and view margin
FD = '/usr/share/fonts/opentype/inter/'

def ease(x): x = min(max(x, 0), 1); return x*x*(3-2*x)
def eoc(x): x = min(max(x, 0), 1); return 1-(1-x)**3
def win(t, a, b, f=0.08):
    if t < a-f or t > b+f: return 0.0
    return min(1, (t-(a-f))/f if t < a else 1, ((b+f)-t)/f if t > b else 1)
def vnoise(t, seed=0):
    return (math.sin(t*7.1+seed)*0.5+math.sin(t*13.7+seed*2.3)*0.3+math.sin(t*23.3+seed*5.1)*0.2)

_cache = {}
def layer(name):
    if name not in _cache:
        im = cv2.imread(f'L/{name}.png', cv2.IMREAD_UNCHANGED)  # BGRA
        im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA).astype(np.float32)
        a = im[..., 3:4]/255.0
        im[..., :3] *= a
        _cache[name] = np.clip(im, 0, 255).astype(np.uint8)
    return _cache[name]

def mat(Z, T, pan, p, tf):
    s = 1+(Z-1)*p if p > 0 else 1+(Z-1)*0.15
    # local transform in view coords
    dx, dy, rot, sx, sy, px, py = tf
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    Lm = np.array([[c*sx, -sn*sy, 0], [sn*sx, c*sy, 0], [0, 0, 1]])
    Lm = np.array([[1, 0, px+dx], [0, 1, py+dy], [0, 0, 1]]) @ Lm @ np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
    U = np.array([[1/LS, 0, -MX], [0, 1/LS, -MY], [0, 0, 1]])  # layer px -> view
    Cm = np.array([[s, 0, (1-s)*T[0]-pan[0]*p], [0, s, (1-s)*T[1]-pan[1]*p], [0, 0, 1]])
    return (Cm @ Lm @ U)[:2]

ID = (0, 0, 0, 1, 1, 0, 0)

# ---------------- snow ----------------
class Snow:
    def __init__(s, n, seed, speed=1.0, size=1.0, wind=20, clip=None, bright=1.0):
        r = np.random.RandomState(seed)
        s.x0 = r.uniform(-100, W+100, n); s.y0 = r.uniform(0, H, n); s.d = r.uniform(0.15, 1, n)**1.6
        s.ph = r.uniform(0, 6.28, n); s.f = r.uniform(0.4, 1.2, n)
        s.speed, s.size, s.wind, s.clip, s.bright = speed, size, wind, clip, bright
    def draw(s, t):
        img = np.zeros((H, W), np.float32)
        y = (s.y0 + t*s.speed*(40+180*s.d)) % (H+40) - 20
        x = (s.x0 + np.sin(t*s.f+s.ph)*18*s.d + t*s.wind*s.d) % (W+200) - 100
        rad = (1+3.8*s.d)*s.size
        for xi, yi, ri, di in zip(x, y, rad, s.d):
            cv2.circle(img, (int(xi*4), int(yi*4)), max(1, int(ri*4)), 0.35+0.65*di, -1, cv2.LINE_AA, 2)
        img = cv2.GaussianBlur(img, (0, 0), 0.8)
        if s.clip:
            m = np.zeros_like(img); x0, y0, x1, y1 = s.clip; m[y0:y1, x0:x1] = 1; img *= m
        return img*s.bright

# ---------------- captions ----------------
FONTS = {'w': (FD+'Inter-Light.otf', 58, (236, 241, 244)),
         'a': (FD+'Inter-Bold.otf', 62, (255, 191, 115)),
         'q': (FD+'Inter-SemiBoldItalic.otf', 60, (240, 244, 247)),
         'qa': (FD+'Inter-SemiBoldItalic.otf', 60, (255, 191, 115)),
         's': (FD+'Inter-Medium.otf', 40, (200, 210, 216)),
         'b': (FD+'Inter-ExtraBold.otf', 54, (239, 230, 210)),
         'Q': (FD+'Inter-SemiBoldItalic.otf', 110, (240, 244, 247))}
def make_caption(lines):
    gap = 18; ims = []
    for txt, st in lines:
        fp, sz, col = FONTS[st]; f = ImageFont.truetype(fp, sz)
        bb = f.getbbox(txt); ims.append((txt, f, col, bb))
    hs = [bb[3]-bb[1]+12 for *_, bb in ims]; Ht = sum(hs)+gap*(len(ims)-1)+80
    im = Image.new('RGBA', (W, Ht), (0, 0, 0, 0)); sh = Image.new('RGBA', (W, Ht), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); ds = ImageDraw.Draw(sh); y = 40
    for (txt, f, col, bb), h in zip(ims, hs):
        x = (W-(bb[2]-bb[0]))//2-bb[0]
        ds.text((x, y-bb[1]+3), txt, font=f, fill=(0, 0, 0, 255))
        d.text((x, y-bb[1]), txt, font=f, fill=col+(255,)); y += h+gap
    sh = sh.filter(ImageFilter.GaussianBlur(10)); sh2 = sh.filter(ImageFilter.GaussianBlur(3))
    out = Image.alpha_composite(Image.alpha_composite(sh, sh), sh2); out = Image.alpha_composite(out, im)
    a = np.asarray(out).astype(np.float32)/255.0
    return a
CAPS = [
 (0.4, 4.8, [("Gece biri adını", 'w'), ("üç kere seslense...", 'w'), ("cevap verir miydin?", 'a')], 1330),
 (5.5, 9.4, [("Zemheri ayı.", 'w'), ("Bir dağ köyü.", 'a')], 560),
 (9.6, 13.8, [("Yeni atanan öğretmen Emre,", 'w'), ("lojmandaki ilk gecesinde.", 'a')], 560),
 (14.4, 17.6, [("Muhtar giderken", 'w'), ("tek bir şey söyledi:", 'w')], 400),
 (17.8, 21.8, [("“Adını üç kere çağırırlarsa...", 'q'), ("cevap verme.”", 'qa')], 400),
 (22.5, 25.7, [("Gece", 'w'), ("03.12", 'a')], 1600),
 (26.2, 28.9, [("Kapı çalındı.", 'w')], 1600),
 (29.7, 31.8, [("Üç kere.", 'a')], 1600),
 (32.4, 35.4, [("“Emre...”", 'Q')], 1150),
 (35.8, 40.7, [("Ses, annesinin", 'w'), ("sesine benziyordu.", 'a')], 1150),
 (41.4, 45.3, [("“Emre... aç kapıyı oğlum.", 'q'), ("Üşüdüm.”", 'qa')], 380),
 (45.6, 49.7, [("Annesi", 'w'), ("600 kilometre uzaktaydı.", 'a')], 380),
 (50.4, 52.9, [("Üçüncü kez", 'w'), ("çağırmadı.", 'a')], 1680),
 (53.5, 57.7, [("Pencereye", 'w'), ("vurdu.", 'a')], 1680),
 (58.4, 60.9, [("Sabah kapının önünde", 'w'), ("izler vardı...", 'w')], 250),
 (61.0, 62.9, [("İnsan izi", 'w'), ("değildi.", 'a')], 250),
 (63.0, 64.85, [("Köylüler ona", 'w'), ("karakoncolos der.", 'a')], 250),
 (65.6, 72.0, [("Bu videoda", 'w'), ("kaç kere göründü?", 'a')], 1330),
 (66.8, 72.0, [("Dikkatli izleyen bulur. Yoruma yaz.", 's')], 1500),
 (67.6, 72.0, [("@masaldegil", 'b')], 1620),
]
_capimg = {}
def draw_caps(fr, t):
    for i, (a, b, lines, yc) in enumerate(CAPS):
        if t < a-0.01 or t > b+0.01: continue
        if i not in _capimg: _capimg[i] = make_caption(lines)
        c = _capimg[i]; al = min(1, (t-a)/0.35, (b-t)/0.3)
        al = ease(max(al, 0)); dy = int((1-al)*14)
        h = c.shape[0]; y0 = yc-h//2+dy; y1 = y0+h
        cy0, cy1 = max(0, y0), min(H, y1)
        sub = c[cy0-y0:cy1-y0]
        A = sub[..., 3:4]*al
        fr[cy0:cy1] = fr[cy0:cy1]*(1-A)+sub[..., :3]*A

# ---------------- scenes ----------------
def shake(t, hits, amp=14, dur=0.3):
    x = y = 0
    for h in hits:
        if 0 <= t-h < dur:
            k = (1-(t-h)/dur)**2*amp
            x += k*math.sin((t-h)*90); y += k*math.cos((t-h)*77)
    return x, y

def S(start, dur, cam, layers, fade=(0.25, 0.25), grade=(1, 1, 1)):
    return dict(start=start, dur=dur, cam=cam, layers=layers, fade=fade, grade=grade)

def L_(name, p=1.0, mode='n', alpha=None, tf=None): return dict(name=name, p=p, mode=mode, alpha=alpha, tf=tf)

SC = {}
SC[1] = S(0, 5, lambda t: (1+0.08*ease(t/5), (540, 960), (0, 0)),
 [L_('s1_bg', 0.1), {'snow': Snow(140, 1, 0.6, 0.9, 10, bright=0.6)},
  L_('s1_eyes', 0.5, 'a', alpha=lambda t: ease((t-2.4)/0.9), tf=lambda t: (0, 0, 0, 1, 0.08 if 3.75 < t < 3.9 else 1, 540, 960))], fade=(0.0, 0.25))
SC[2] = S(5, 9, lambda t: (1+0.2*ease(t/9), (470, 1460), (0, 0)),
 [L_('s2_sky', 0.05), L_('s2_far', 0.2), L_('s2_fog', 0.3), L_('s2_ridge', 0.4), L_('s2_hidden', 0.4, alpha=lambda t: win(t, 4.0, 4.6)),
  L_('s2_village', 0.65), {'snow': Snow(260, 2, 1.0, 1.0, 25)}, L_('s2_fg', 1.0)])
SC[3] = S(14, 8, lambda t: (1+0.1*ease(t/8), (620, 1100), (0, 0)),
 [L_('s3_bg', 0.3), L_('s3_muhtar', 0.7, tf=lambda t: (0, 0, 0, 1, 1+0.006*math.sin(t*2.2), 790, 1720)),
  L_('s3_lantern', 0.7, tf=lambda t: (0, 0, 5*math.sin(t*2.6), 1, 1, 625, 1150)),
  L_('s3_lglow', 0.7, 'a', alpha=lambda t: 0.85+0.12*vnoise(t*2, 1), tf=lambda t: (0, 0, 5*math.sin(t*2.6), 1, 1, 625, 1150)),
  {'snow': Snow(220, 3, 0.9, 1.1, 30)}, L_('s3_fg', 1.0)])
KN = [4.3, 4.8, 5.3]
SC[4] = S(22, 10, lambda t: (1+0.14*ease(t/10), (560, 900), shake(t, KN, 16)),
 [L_('s4_room', 0.5), L_('s4_hidden', 0.5, alpha=lambda t: win(t, 7.05, 7.55, 0.06)), L_('s4_frame', 0.5), L_('s4_teacher', 0.8),
  L_('s4_glow', 0.8, 'a', alpha=lambda t: 0.8+0.15*vnoise(t*1.5, 3) - (0.35 if any(0 < t-k < 0.12 for k in KN) else 0))])
SC[5] = S(32, 9, lambda t: (1+0.22*ease(t/9), (540, 1450), shake(t, [0.4], 6)),
 [L_('s5_bg', 0.6), L_('s5_feet', 0.6, tf=lambda t: (50*math.sin(t*0.8)+(30 if t > 4 else 0), 0, 0, 1, 1, 0, 0)),
  L_('s5_glow', 0.6, 'a', alpha=lambda t: 0.75+0.1*vnoise(t, 5)), L_('s5_eyes', 0.6, 'a', alpha=lambda t: win(t, 5.5, 6.2, 0.15))])
def hb(t):
    if t < 4.2: return 0
    ph = (t-4.2) % 0.85
    return math.exp(-((ph-0.0)/0.05)**2)+0.6*math.exp(-((ph-0.2)/0.05)**2)
SC[6] = S(41, 9, lambda t: (1.05+0.1*ease(t/9)+0.012*hb(t), (500, 1050), (0, 0)),
 [L_('s6_bg', 0.3), L_('s6_glow', 0.4, 'a', alpha=lambda t: 0.7+0.25*vnoise(t*1.8, 7)),
  L_('s6_teacher', 0.9, tf=lambda t: (0, 0, 0, 1, 1+0.008*math.sin(t*2.4), 700, 2000))])
SLAP = 3.2
def s7cam(t):
    z = 1.0 + (0.13*eoc((t-SLAP)/4.8) if t > SLAP else 0.02*ease(t/SLAP))
    return (z, (540, 720), shake(t, [SLAP], 28, 0.45))
def ctf(t):
    dy = 900*(1-eoc((t-0.3)/2.2))
    sc = 1+(0.05*math.exp(-((t-SLAP)/0.25)**2) if t > SLAP-0.3 else 0)
    return (0, dy, 0, sc, sc, 540, 760)
SC[7] = S(50, 8, s7cam,
 [L_('s7_out', 0.2), {'snow': Snow(240, 7, 1.0, 1.0, 35)}, L_('s7_creature', 0.6, tf=ctf),
  L_('s7_ceyes', 0.6, 'a', alpha=lambda t: 1.0 if t > 1.6 else 0.3, tf=ctf), L_('s7_frame', 1.0),
  L_('s7_glass', 1.0, 'a', alpha=lambda t: 0.55 if t >= SLAP else 0)])
SC[8] = S(58, 7, lambda t: (1.35-0.35*ease(t/6.3), (540, 1900-940*ease(t/6.3)), (0, 0)),
 [L_('s8_bg', 1.0), {'snow': Snow(60, 8, 0.4, 0.8, 10, bright=0.7)}], grade=(0.78, 0.8, 0.86))
SC[9] = S(65, 7, lambda t: (1+0.04*t/7, (540, 760), (0, 0)),
 [L_('s9_bg', 0.1), L_('s9_logo', 0.4, alpha=lambda t: ease((t-0.1)/0.8))], fade=(0.2, 0.6))

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = 1-0.55*np.clip((((XX-W/2)/(W*0.75))**2+((YY-H/2)/(H*0.62))**2), 0, 1)**1.3
VIG = VIG[..., None]

def render_scene(k, out, preview=False):
    sc = SC[k]; n = int(round(sc['dur']*FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.RandomState(k)
    frames = range(n) if not preview else preview
    for i in frames:
        t = i/FPS; tg = sc['start']+t
        Z, T, pan = sc['cam'](t)
        fr = np.zeros((H, W, 3), np.float32)
        for Ly in sc['layers']:
            if 'snow' in Ly:
                sn = Ly['snow'].draw(t)[..., None]
                fr = fr*(1-sn*0.9)+sn*np.array([0.88, 0.94, 1.0], np.float32)
                continue
            al = Ly['alpha'](t) if Ly['alpha'] else 1.0
            if al <= 0.003: continue
            tf = Ly['tf'](t) if Ly['tf'] else ID
            M = mat(Z, T, pan, Ly['p'], tf)
            im = cv2.warpAffine(layer(Ly['name']), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT).astype(np.float32)/255.0
            if Ly['mode'] == 'a':
                fr += im[..., :3]*al
            else:
                a = im[..., 3:4]*al
                fr = fr*(1-a)+im[..., :3]*al
        # bloom
        sm = cv2.resize(fr, (W//4, H//4), interpolation=cv2.INTER_AREA)
        br = np.clip(sm-0.62, 0, None)
        br = cv2.GaussianBlur(br, (0, 0), 9)
        fr += cv2.resize(br, (W, H), interpolation=cv2.INTER_LINEAR)*0.9
        # grade: teal shadows, warm highlights
        g = np.array(sc['grade'], np.float32)
        lum = fr.mean(axis=2, keepdims=True)
        fr = fr*g + (1-np.clip(lum*3, 0, 1))*np.array([0.0, 0.012, 0.022], np.float32)
        fr *= VIG
        # chromatic aberration
        fr[..., 0] = np.roll(fr[..., 0], 1, axis=1); fr[..., 2] = np.roll(fr[..., 2], -1, axis=1)
        # slap flash
        if k == 7 and 0 <= t-SLAP < 0.12: fr += 0.35*(1-(t-SLAP)/0.12)
        # fades
        fi, fo = sc['fade']
        f = 1.0
        if fi > 0: f = min(f, t/fi)
        if fo > 0: f = min(f, (sc['dur']-t-1/FPS)/fo)
        fr *= np.clip(f, 0, 1)
        draw_caps(fr, tg)
        # grain
        gn = rng.standard_normal((H//2, W//2)).astype(np.float32)
        gn = cv2.resize(gn, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        fr += gn*0.022
        pr.stdin.write((np.clip(fr, 0, 1)*255).astype(np.uint8).tobytes())
    pr.stdin.close(); pr.wait()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':  # still frames at given global times
        for tg in map(float, sys.argv[2:]):
            k = max(kk for kk in SC if SC[kk]['start'] <= tg)
            sc = SC[k]; i = int((tg-sc['start'])*FPS)
            render_scene(k, f'/tmp/st_{tg}.mp4', preview=[i])
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'/tmp/st_{tg}.mp4', '-frames:v', '1', f'chk_{tg}.png'])
    else:
        for k in map(int, sys.argv[2:]):
            render_scene(k, f'sc{k:02d}.mp4')
            print('done', k, flush=True)
