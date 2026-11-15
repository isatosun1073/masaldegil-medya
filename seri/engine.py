"""MASAL DEĞİL — bölüm render motoru.
Kullanım: python3 engine.py layers EP   (katmanları çiz)
          python3 engine.py tts EP       (anlatım hizalama — vo/epNN.wav gerekir)
          python3 engine.py render EP [parça]  (video)
          python3 engine.py audio EP     (ses miksi)  ;  python3 engine.py final EP
"""
import numpy as np, cv2, subprocess, sys, math, os, json, re, hashlib, asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zemheri as Z

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get('MD_WORK', '/home/claude/md_work')
os.makedirs(WORK, exist_ok=True); os.makedirs(f'{WORK}/L', exist_ok=True)
W, H, FPS = 1080, 1920, 24
LS = 1.25; MX, MY = 108, 192
FD = '/usr/share/fonts/opentype/inter/'

def ease(x): x = min(max(x, 0), 1); return x*x*(3-2*x)
def eoc(x): x = min(max(x, 0), 1); return 1-(1-x)**3
def win(t, a, b, f=0.08):
    if t < a-f or t > b+f: return 0.0
    return min(1, (t-(a-f))/f if t < a else 1, ((b+f)-t)/f if t > b else 1)
def vnoise(t, s=0): return math.sin(t*7.1+s)*0.5+math.sin(t*13.7+s*2.3)*0.3+math.sin(t*23.3+s*5.1)*0.2
def lkey(k, p): return k if not p else k+'_'+hashlib.md5(json.dumps(p, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:8]

# ---------------- templates ----------------
def L_(k, p=None, z=1.0, mode='n', alpha=None, tf=None): return dict(k=k, p=p or {}, z=z, mode=mode, alpha=alpha, tf=tf)
def SNOW(n=220, seed=1, sp=1.0, wind=25, bright=1.0): return {'snow': (n, seed, sp, wind, bright)}
ID = (0, 0, 0, 1, 1, 0, 0)
def shake(t, hits, amp=14, dur=0.3):
    x = y = 0
    for h in hits:
        if 0 <= t-h < dur:
            k = (1-(t-h)/dur)**2*amp; x += k*math.sin((t-h)*90); y += k*math.cos((t-h)*77)
    return x, y

def template(name, p, D):
    """returns dict(layers, cam(t), capy, sfx[list of (t, kind)], extra)"""
    sfx = []; capy = 1500; extra = {}
    zf = 1.0 + (0.25 if p.get('zoom') else 0.0)
    if name == 'hook':
        ly = [L_('s1_bg', z=0.1), SNOW(150, 1, 0.6, 10, 0.6),
              L_('s1_eyes', z=0.5, mode='a', alpha=lambda t: ease((t-D*0.35)/1.0),
                 tf=lambda t: (0, 0, 0, 1, 0.08 if (t % 4.0) > 3.85 else 1, 540, 960))]
        cam = lambda t: (1+0.1*ease(t/D), (540, 960), (0, 0)); capy = 1330
        sfx.append((D*0.35, 'glass'))
    elif name == 'hook_text':
        ly = [L_('title', {'text': p['text']}, z=0.2), SNOW(120, 2, 0.5, 10, 0.5)]
        cam = lambda t: (1+0.06*ease(t/D), (540, 960), (0, 0)); capy = 1420; sfx.append((0.2, 'hit'))
    elif name == 'village':
        ly = [L_('s2_sky', z=0.05), L_('s2_far', z=0.2), L_('s2_fog', z=0.3), L_('s2_ridge', z=0.4),
              L_('s2_hidden', z=0.4, alpha=lambda t: win(t, D*0.45, D*0.45+0.6)) if p.get('hidden') else None,
              L_('s2_village', z=0.65), SNOW(260, 2), L_('s2_fg', z=1.0)]
        cam = lambda t: (1+0.2*ease(t/D), (470, 1460), (0, 0)); capy = 560
    elif name == 'muhtar_door':
        ly = [L_('s3_bg', z=0.3), L_('s3_muhtar', z=0.7, tf=lambda t: (0, 0, 0, 1, 1+0.006*math.sin(t*2.2), 790, 1720)),
              L_('s3_lantern', z=0.7, tf=lambda t: (0, 0, 5*math.sin(t*2.6), 1, 1, 625, 1150)),
              L_('s3_lglow', z=0.7, mode='a', alpha=lambda t: 0.85+0.12*vnoise(t*2, 1), tf=lambda t: (0, 0, 5*math.sin(t*2.6), 1, 1, 625, 1150)),
              SNOW(220, 3, 0.9, 30), L_('s3_fg')]
        if p.get('zoom'): cam = lambda t: (1.1+0.3*ease(t/D), (790, 1050), (0, 0))
        else: cam = lambda t: (1+0.1*ease(t/D), (620, 1100), (0, 0))
        capy = 420
    elif name == 'desk':
        kn = [D*0.55, D*0.55+0.5, D*0.55+1.0] if p.get('knock') else []
        hid = p.get('hidden')
        ly = [L_('s4_room', z=0.5), L_('s4_hidden', z=0.5, alpha=lambda t: win(t, D*0.8, D*0.8+0.5, 0.06)) if hid else None,
              L_('s4_frame', z=0.5), L_('s4_teacher', z=0.8),
              L_('s4_glow', z=0.8, mode='a', alpha=lambda t: 0.8+0.15*vnoise(t*1.5, 3)-(0.35 if any(0 < t-k < 0.12 for k in kn) else 0))]
        cam = lambda t: (1+0.14*ease(t/D), (560, 900), shake(t, kn, 16))
        sfx += [(k, 'knock') for k in kn]; sfx.append((0, 'tick')); capy = 1640
    elif name == 'door_in':
        call = p.get('call')
        ly = [L_('s5_bg', z=0.6), L_('s5_feet', z=0.6, tf=lambda t: (50*math.sin(t*0.8), 0, 0, 1, 1, 0, 0)),
              L_('s5_glow', z=0.6, mode='a', alpha=lambda t: 0.75+0.1*vnoise(t, 5)),
              L_('s5_eyes', z=0.6, mode='a', alpha=lambda t: win(t, D*0.6, D*0.6+0.7, 0.15)) if p.get('eyes') else None]
        cam = lambda t: (1+0.22*ease(t/D), (540, 1450), (0, 0)); capy = 1150
        if call: sfx.append((0.4, 'call_'+call))
        sfx.append((D*0.3, 'steps'))
    elif name == 'profile':
        ly = [L_('s6_bg', z=0.3), L_('s6_glow', z=0.4, mode='a', alpha=lambda t: 0.7+0.25*vnoise(t*1.8, 7)),
              L_('s6_teacher', z=0.9, tf=lambda t: (0, 0, 0, 1, 1+0.008*math.sin(t*2.4), 700, 2000))]
        cam = lambda t: (1.05+(0.25 if p.get('zoom') else 0.1)*ease(t/D), (480, 1050), (0, 0)); capy = 380
        sfx.append((0, 'heart'))
        if p.get('call'): sfx.append((0.4, 'call_'+p['call']))
    elif name == 'window':
        SL = D*0.5 if p.get('slam') else 1e9
        def ctf(t):
            dy = 900*(1-eoc((t-0.3)/2.2)); sc = 1+(0.05*math.exp(-((t-SL)/0.25)**2) if t > SL-0.3 else 0)
            return (0, dy, 0, sc, sc, 540, 760)
        ly = [L_('s7_out', z=0.2), SNOW(240, 7, 1.0, 35), L_('s7_creature', z=0.6, tf=ctf),
              L_('s7_ceyes', z=0.6, mode='a', alpha=lambda t: 1.0 if t > 1.6 else 0.3, tf=ctf), L_('s7_frame'),
              L_('s7_glass', mode='a', alpha=lambda t: 0.55 if t >= SL else 0)]
        cam = lambda t: ((1.0+0.13*eoc((t-SL)/4.8)) if t > SL else 1.0+0.03*ease(t/D), (540, 720), shake(t, [SL], 28, 0.45))
        capy = 1680; sfx.append((0.5, 'screech'))
        if p.get('slam'): sfx.append((SL, 'slam')); extra['flash'] = SL
    elif name == 'prints':
        ly = [L_('s8_bg'), SNOW(60, 8, 0.4, 10, 0.7)]
        cam = lambda t: (1.35-0.35*ease(t/(D*0.9)), (540, 1900-940*ease(t/(D*0.9))), (0, 0)); capy = 250
        extra['grade'] = (0.78, 0.8, 0.86)
    elif name == 'carved':
        ly = [L_('carved', {'text': p['text']})]
        cam = lambda t: (1+0.12*ease(t/D), (540, 1000), (0, 0)); capy = None; sfx.append((0.3, 'scratch'))
        extra['grade'] = (0.95, 0.9, 0.85)
    elif name == 'classroom':
        ly = [L_('cls_bg', z=0.4), L_('cls_kids', z=0.8)]
        cam = (lambda t: (1.05+0.35*ease(t/D), (880, 1600), (0, 0))) if p.get('zoom') else (lambda t: (1+0.1*ease(t/D), (540, 900), (0, 0)))
        capy = 1780 if False else 160; capy = 1500 if not p.get('zoom') else 900
    elif name == 'paper':
        ly = [L_('paper', {'lines': p['lines'], 'burn': p.get('burn', 0)})]
        if p.get('burn'): ly.append(L_('stove_glow', mode='a', alpha=lambda t: 0.4+0.2*vnoise(t*2, 9)))
        cam = lambda t: (1.02+0.1*ease(t/D), (540, 700+500*ease(t/D)), (0, 0)); capy = None
        extra['flashlight'] = True; sfx.append((0.2, 'page'))
    elif name == 'girl':
        ly = [L_('girl_bg', z=0.3), L_('girl', z=0.8, tf=lambda t: (0, 0, 0, 1, 1+0.006*math.sin(t*2.0), 540, 2100))]
        cam = lambda t: (1+(0.3 if p.get('zoom') else 0.1)*ease(t/D), (540, 900), (0, 0)); capy = 1560
    elif name == 'shadow':
        ly = [L_('shadow_wall')]; cam = lambda t: (1+0.35*ease(t/D), (860, 760), (0, 0)); capy = 1700; sfx.append((D*0.4, 'hit'))
    elif name == 'photo':
        ly = [L_('photo_bg', z=0.3), L_('photo_card', z=0.8)]
        cam = (lambda t: (1.1+0.9*ease(t/D), (540, 1180), (0, 0))) if p.get('zoom') else (lambda t: (1+0.08*ease(t/D), (540, 1000), (0, 0)))
        capy = None; extra['grade'] = (1.0, 0.92, 0.8)
    elif name == 'rope':
        ly = [L_('rope', {'knots': p.get('knots', 4)})]; cam = lambda t: (1.1+0.1*ease(t/D), (540, 600+700*ease(t/D)), (0, 0)); capy = 1500
    elif name == 'plates':
        ly = [L_('plates', {'names': p['names'], 'single': p.get('single', 0)})]
        cam = lambda t: (1+0.12*ease(t/D), (540, 960 if p.get('single') else 600+500*ease(t/D)), (0, 0)); capy = None
        if p.get('single'): sfx.append((0.3, 'hit'))
    elif name == 'road':
        ly = [L_('road', z=0.3)]
        if p.get('lights'): ly += [L_('minibus', z=0.6, alpha=lambda t: ease(t/1.5)), L_('headlights', z=0.6, mode='a', alpha=lambda t: ease(t/1.5)*(0.9+0.1*vnoise(t, 2)))]
        ly.append(SNOW(300, 11, 1.2, 60))
        cam = lambda t: (1+0.15*ease(t/D), (540, 1150), (0, 0)); capy = 560
        if p.get('lights'): sfx.append((0.2, 'engine'))
    elif name in ('ruins', 'dawn'):
        ly = [L_('ruins', {'dawn': 1 if name == 'dawn' else 0})] + ([SNOW(120, 13, 0.6, 15, 0.7)] if name == 'ruins' else [])
        cam = lambda t: (1+0.12*ease(t/D), (560, 1250), (0, 0)); capy = 560
        if name == 'dawn': sfx.append((0, 'birds'))
    elif name == 'drawing':
        ly = [L_('drawing')]; cam = lambda t: (1.05+0.2*ease(t/D), (540, 700+400*ease(t/D)), (0, 0)); capy = None; sfx.append((0.2, 'page'))
    elif name == 'phone':
        ly = [L_('phone', {'caller': p.get('caller', 'Annem'), 'static': p.get('static', 0)})]
        cam = lambda t: (1+0.12*ease(t/D), (540, 900), ((3*math.sin(t*60) if (t % 1.2) < 0.5 and not p.get('static') else 0), 0)); capy = 1530
        sfx.append((0.1, 'static' if p.get('static') else 'ring'))
    elif name == 'stove':
        ly = [L_('stove'), L_('stove_glow', mode='a', alpha=lambda t: 0.6+0.3*vnoise(t*2, 4))]
        cam = lambda t: (1+0.18*ease(t/D), (540, 1050), (0, 0)); capy = 1640; sfx.append((0, 'fire'))
    elif name == 'reveal':
        ly = [L_('reveal_bg', z=0.2), L_('reveal_cr', z=0.7, tf=lambda t: (0, 0, 0, 1, 1+0.01*math.sin(t*1.7), 560, 1500)),
              L_('reveal_eyes', z=0.7, mode='a', alpha=lambda t: ease((t-0.5)/1.0), tf=lambda t: (0, 0, 0, 1, 1+0.01*math.sin(t*1.7), 560, 1500))]
        cam = lambda t: (1+(0.35 if p.get('zoom') else 0.08)*ease(t/D), (560, 820), (0, 0)); capy = 1640
        sfx.append((0.1, 'boom'))
    elif name == 'endcard':
        ly = [L_('s9_bg', z=0.1), L_('s9_logo', z=0.4, alpha=lambda t: ease((t-0.1)/0.8))]
        cam = lambda t: (1+0.04*t/D, (540, 760), (0, 0)); capy = None
    else:
        raise ValueError(name)
    return dict(layers=[l for l in ly if l], cam=cam, capy=capy, sfx=sfx, extra=extra)

# ---------------- layer rendering (Chrome) ----------------
def needed_layers(ep):
    jobs = {}
    for name, p, _ in ep['shots'] + [('endcard', {}, '')]:
        tp = template(name, p, 10.0)
        for l in tp['layers']:
            if 'k' in l: jobs[lkey(l['k'], l['p'])] = (l['k'], l['p'])
    return jobs

async def _render_layers(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': 1296, 'height': 2304}, device_scale_factor=LS)
        await pg.goto('file://'+HERE+'/layers.html')
        for fn, (k, p) in jobs.items():
            out = f'{WORK}/L/{fn}.png'
            if os.path.exists(out): continue
            await pg.evaluate('([k,p])=>show(k,p)', [k, p]); await pg.wait_for_timeout(120)
            await pg.locator('#st').screenshot(path=out, omit_background=True)
        await b.close()

_cache = {}
def layer(fn):
    if fn not in _cache:
        im = cv2.imread(f'{WORK}/L/{fn}.png', cv2.IMREAD_UNCHANGED)
        im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA).astype(np.float32); a = im[..., 3:4]/255.0; im[..., :3] *= a
        _cache[fn] = np.clip(im, 0, 255).astype(np.uint8)
    return _cache[fn]

def mat(Z_, T, pan, p, tf):
    s = 1+(Z_-1)*p if p > 0 else 1+(Z_-1)*0.15
    dx, dy, rot, sx, sy, px, py = tf
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    Lm = np.array([[c*sx, -sn*sy, 0], [sn*sx, c*sy, 0], [0, 0, 1]])
    Lm = np.array([[1, 0, px+dx], [0, 1, py+dy], [0, 0, 1]]) @ Lm @ np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
    U = np.array([[1/LS, 0, -MX], [0, 1/LS, -MY], [0, 0, 1]])
    Cm = np.array([[s, 0, (1-s)*T[0]-pan[0]*p], [0, s, (1-s)*T[1]-pan[1]*p], [0, 0, 1]])
    return (Cm @ Lm @ U)[:2]

class Snow:
    def __init__(s, n, seed, speed=1.0, wind=20, bright=1.0):
        r = np.random.RandomState(seed)
        s.x0 = r.uniform(-100, W+100, n); s.y0 = r.uniform(0, H, n); s.d = r.uniform(0.15, 1, n)**1.6
        s.ph = r.uniform(0, 6.28, n); s.f = r.uniform(0.4, 1.2, n); s.speed, s.wind, s.bright = speed, wind, bright
    def draw(s, t):
        img = np.zeros((H, W), np.float32)
        y = (s.y0+t*s.speed*(40+180*s.d)) % (H+40)-20; x = (s.x0+np.sin(t*s.f+s.ph)*18*s.d+t*s.wind*s.d) % (W+200)-100
        rad = 1+3.8*s.d
        for xi, yi, ri, di in zip(x, y, rad, s.d):
            cv2.circle(img, (int(xi*4), int(yi*4)), max(1, int(ri*4)), 0.35+0.65*di, -1, cv2.LINE_AA, 2)
        return cv2.GaussianBlur(img, (0, 0), 0.8)*s.bright

# ---------------- captions ----------------
FONTS = {'w': (FD+'Inter-Medium.otf', 54, (240, 244, 247)), 'a': (FD+'Inter-Bold.otf', 56, (255, 191, 115)),
         's': (FD+'Inter-Medium.otf', 40, (200, 210, 216)), 'b': (FD+'Inter-ExtraBold.otf', 54, (239, 230, 210)),
         'T': (FD+'Inter-Black.otf', 76, (255, 191, 115))}
def make_caption(lines):
    gap = 16; ims = []
    for txt, st in lines:
        fp, sz, col = FONTS[st]; f = ImageFont.truetype(fp, sz); ims.append((txt, f, col, f.getbbox(txt)))
    hs = [bb[3]-bb[1]+12 for *_, bb in ims]; Ht = sum(hs)+gap*(len(ims)-1)+80
    im = Image.new('RGBA', (W, Ht), (0, 0, 0, 0)); sh = Image.new('RGBA', (W, Ht), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); ds = ImageDraw.Draw(sh); y = 40
    for (txt, f, col, bb), h in zip(ims, hs):
        x = (W-(bb[2]-bb[0]))//2-bb[0]
        ds.text((x, y-bb[1]+3), txt, font=f, fill=(0, 0, 0, 255)); d.text((x, y-bb[1]), txt, font=f, fill=col+(255,)); y += h+gap
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(sh, sh), sh), im)
    return np.asarray(out).astype(np.float32)/255.0

def clean(txt): return re.sub(r'\[.*?\]\s*', '', txt).strip()
def chunks(txt, maxc=46):
    """cümle/virgül sınırlarında altyazı parçaları; her parça en fazla 2 satır"""
    sents = re.findall(r'[^.?!]+[.?!]*', clean(txt)); out = []
    for s in sents:
        s = s.strip()
        if not s: continue
        while len(s) > maxc:
            cut = max(s.rfind(',', 0, maxc), s.rfind(' ', 0, maxc))
            out.append(s[:cut+1].strip()); s = s[cut+1:].strip()
        out.append(s)
    res = []
    for c in out:
        if len(c) <= 24: res.append([c])
        else:
            words = c.split(); best = None
            for i in range(1, len(words)):
                a, b = ' '.join(words[:i]), ' '.join(words[i:]); sc = max(len(a), len(b))
                if best is None or sc < best[0]: best = (sc, a, b)
            res.append([best[1], best[2]])
    return res

# ---------------- timeline ----------------
PRE, POST = 0.7, 0.9
def timeline(ep):
    al = json.load(open(f'{WORK}/ep{ep["no"]:02d}_align.json'))
    shots = []; t = 0.0
    for i, (name, p, txt) in enumerate(ep['shots']):
        seg = al['segs'][i]  # [a,b] in narration file or None
        nd = (seg[1]-seg[0]) if seg else 0
        D = max(4.0 if not seg else 3.0, PRE+nd+POST)
        if name == 'window': D += 1.5
        if name == 'door_in' and p.get('call') and not txt: D = 6.5
        shots.append(dict(i=i, name=name, p=p, txt=txt, start=t, dur=D, vo=(t+PRE, seg) if seg else None)); t += D
    shots.append(dict(i=len(shots), name='endcard', p={}, txt='', start=t, dur=7.0, vo=None)); t += 7.0
    return shots, t

def caps_for(ep, shots):
    caps = []
    for s in shots:
        tp = template(s['name'], s['p'], s['dur'])
        if s['name'] == 'endcard':
            st = s['start']
            if ep['no'] < 10:
                caps += [(st+0.6, st+7, [(f"ZEMHERİ · {ep['no']}. BÖLÜM SONU", 's')], 1230),
                         (st+1.2, st+7, [(l, 'a' if i else 'w') for i, l in enumerate(wrap2(ep['son'].split(' Yarın')[0].split(' 2. bölüm')[0].split(' 3. bölüm')[0]))], 1360),
                         (st+2.4, st+7, [("Devamı yarın gece 00.00'da", 'w')], 1520),
                         (st+3.2, st+7, [(Z.HESAP, 'b')], 1640)]
            else:
                caps += [(st+0.6, st+7, [("SON.", 'T')], 1250), (st+1.6, st+7, [("Adını yorumlara yazma.", 'w'), ("Üç kişi yazarsa...", 'a')], 1420),
                         (st+3.0, st+7, [(Z.HESAP, 'b')], 1640)]
            continue
        if not s['vo'] or tp['capy'] is None: continue
        t0, seg = s['vo']; nd = seg[1]-seg[0]; cs = chunks(s['txt'])
        L = [sum(len(x) for x in c)+8 for c in cs]; tot = sum(L); acc = 0
        for c, l in zip(cs, L):
            a = t0+nd*acc/tot; b = t0+nd*(acc+l)/tot; acc += l
            st = 'a' if c[-1].endswith(('?', '...', '…')) else 'w'
            caps.append((a, b+0.15, [(x, st if j == len(c)-1 else 'w') for j, x in enumerate(c)], tp['capy']))
    return caps

def wrap2(s, n=26):
    w = s.split(); lines = ['']
    for x in w:
        if len(lines[-1])+len(x)+1 > n: lines.append(x)
        else: lines[-1] = (lines[-1]+' '+x).strip()
    return lines[:3]

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1-0.55*np.clip((((XX-W/2)/(W*0.75))**2+((YY-H/2)/(H*0.62))**2), 0, 1)**1.3)[..., None]
FLASH = None

def render(ep, part=None, nparts=1):
    shots, total = timeline(ep); caps = caps_for(ep, shots); capimg = {}
    n = int(round(total*FPS)); rng = np.random.RandomState(ep['no'])
    fr_range = range(n) if part is None else range(part*n//nparts, (part+1)*n//nparts)
    out = f'{WORK}/ep{ep["no"]:02d}_v{"" if part is None else part}.mp4'
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    tps = {}; snows = {}
    global FLASH
    if FLASH is None:
        FLASH = np.clip(1-(((XX-W/2)/(W*0.55))**2+((YY-H/2)/(H*0.42))**2), 0, 1)[..., None]
    for fi in fr_range:
        tg = fi/FPS
        s = next(x for x in reversed(shots) if x['start'] <= tg+1e-6); t = tg-s['start']; D = s['dur']
        if s['i'] not in tps: tps[s['i']] = template(s['name'], s['p'], D)
        tp = tps[s['i']]; Zm, T, pan = tp['cam'](t)
        fr = np.zeros((H, W, 3), np.float32)
        for Ly in tp['layers']:
            if 'snow' in Ly:
                key = (s['i'], Ly['snow'])
                if key not in snows: snows[key] = Snow(*Ly['snow'][:3], wind=Ly['snow'][3], bright=Ly['snow'][4])
                sn = snows[key].draw(t)[..., None]; fr = fr*(1-sn*0.9)+sn*np.array([0.88, 0.94, 1.0], np.float32); continue
            al = Ly['alpha'](t) if Ly['alpha'] else 1.0
            if al <= 0.003: continue
            tf = Ly['tf'](t) if Ly['tf'] else ID
            im = cv2.warpAffine(layer(lkey(Ly['k'], Ly['p'])), mat(Zm, T, pan, Ly['z'], tf), (W, H), flags=cv2.INTER_LINEAR).astype(np.float32)/255.0
            if Ly['mode'] == 'a': fr += im[..., :3]*al
            else: a = im[..., 3:4]*al; fr = fr*(1-a)+im[..., :3]*al
        if tp['extra'].get('flashlight'):
            fr *= (0.45+0.75*FLASH)
        sm = cv2.resize(fr, (W//4, H//4), interpolation=cv2.INTER_AREA)
        fr += cv2.resize(cv2.GaussianBlur(np.clip(sm-0.62, 0, None), (0, 0), 9), (W, H))*0.9
        g = np.array(tp['extra'].get('grade', (1, 1, 1)), np.float32); lum = fr.mean(axis=2, keepdims=True)
        fr = fr*g+(1-np.clip(lum*3, 0, 1))*np.array([0.0, 0.012, 0.022], np.float32)
        fr *= VIG
        fr[..., 0] = np.roll(fr[..., 0], 1, axis=1); fr[..., 2] = np.roll(fr[..., 2], -1, axis=1)
        if 'flash' in tp['extra'] and 0 <= t-tp['extra']['flash'] < 0.12: fr += 0.35*(1-(t-tp['extra']['flash'])/0.12)
        f = min(1.0, t/0.25 if s['i'] > 0 else 1.0, (D-t)/0.25 if s['name'] != 'endcard' else (D-t)/0.6)
        fr *= np.clip(f, 0, 1)
        for ci, (a, b, lines, yc) in enumerate(caps):
            if tg < a-0.01 or tg > b+0.01: continue
            if ci not in capimg: capimg[ci] = make_caption(lines)
            c = capimg[ci]; al = ease(max(min(1, (tg-a)/0.25, (b-tg)/0.25), 0)); h = c.shape[0]
            y0 = yc-h//2+int((1-al)*10); cy0, cy1 = max(0, y0), min(H, y0+h); sub = c[cy0-y0:cy1-y0]
            A = sub[..., 3:4]*al; fr[cy0:cy1] = fr[cy0:cy1]*(1-A)+sub[..., :3]*A
        gn = cv2.resize(rng.standard_normal((H//2, W//2)).astype(np.float32), (W, H))[..., None]
        fr += gn*0.022
        pr.stdin.write((np.clip(fr, 0, 1)*255).astype(np.uint8).tobytes())
    pr.stdin.close(); pr.wait(); return out

if __name__ == '__main__':
    cmd, no = sys.argv[1], int(sys.argv[2]); ep = Z.EP[no-1]
    if cmd == 'layers': asyncio.run(_render_layers(needed_layers(ep)))
    elif cmd == 'render':
        part = int(sys.argv[3]) if len(sys.argv) > 3 else None; npart = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        print(render(ep, part, npart))
    elif cmd == 'still':
        shots, total = timeline(ep)
        for tg in map(float, sys.argv[3:]):
            n = int(round(total*FPS)); fi = int(tg*FPS)
            # render one frame by using part slicing trick
            out = render(ep, part=fi, nparts=n)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-frames:v', '1', f'{WORK}/still_{no}_{tg}.png'])
