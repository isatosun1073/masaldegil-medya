"""Hizalama + ses miksi. python3 sound.py align EP ; python3 sound.py mix EP"""
import numpy as np, sys, json, re, subprocess, os
from scipy import signal
from scipy.io import wavfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zemheri as Z, engine as E
SR = 48000; WORK = E.WORK

def load(path):
    tmp = path+'.48k.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ac', '1', '-ar', str(SR), tmp], check=True)
    _, x = wavfile.read(tmp); return x.astype(np.float32)/32768

def silences(path, db=-38, d=0.25):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', f'silencedetect=noise={db}dB:d={d}', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', o)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', o)]
    return list(zip(st, en))

def align(ep):
    path = f'{WORK}/ep{ep["no"]:02d}_vo.mp3'
    x = load(path); dur = len(x)/SR
    sil = silences(path)
    # speech bounds
    s0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    s1 = sil[-1][0] if sil and sil[-1][1] > dur-0.05 else dur
    inner = [(a, b) for a, b in sil if a > s0+0.1 and b < s1-0.1]
    idx = [i for i, s in enumerate(ep['shots']) if s[2]]
    lens = [len(E.clean(ep['shots'][i][2]))+6 for i in idx]; K = len(idx)
    cum = np.cumsum(lens)[:-1]/sum(lens); exp = s0+(s1-s0)*cum
    # DP: choose K-1 silences in order minimizing (mid-exp)^2 - 0.6*len
    M = len(inner); INF = 1e18
    cost = np.full((K, M+1), INF); back = np.zeros((K, M+1), int); cost[0, :] = 0
    for k in range(1, K):
        best = INF; bj = -1
        for j in range(M):
            if j > 0 and cost[k-1, j] < best: best, bj = cost[k-1, j], j-1
            if k == 1: prev = 0; pj = -1
            else:
                prev, pj = best, bj
                if pj < 0 and k > 1: continue
            a, b = inner[j]; mid = (a+b)/2
            c = prev+(mid-exp[k-1])**2-0.6*min(b-a, 1.2)
            if c < cost[k, j+1]: cost[k, j+1] = c; back[k, j+1] = pj+1
    j = int(np.argmin(cost[K-1])) if K > 1 else 0
    cuts = []
    for k in range(K-1, 0, -1):
        cuts.append(inner[j-1]); j = back[k, j]
    cuts = cuts[::-1]
    bounds = [s0]+[c for ab in cuts for c in ab]+[s1]
    segs = [None]*len(ep['shots'])
    for n, i in enumerate(idx): segs[i] = [bounds[2*n], bounds[2*n+1]]
    json.dump({'segs': segs, 'dur': dur}, open(f'{WORK}/ep{ep["no"]:02d}_align.json', 'w'))
    for i, sg in enumerate(segs):
        if sg: print(i, ep['shots'][i][0], f'{sg[0]:.2f}-{sg[1]:.2f}', E.clean(ep['shots'][i][2])[:50])

# ---------------- sfx ----------------
rng = np.random.RandomState(7)
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, 'high', fs=SR, output='sos'), x)
def rev(x, sec=2.4, mix=0.4, seed=3):
    r = np.random.RandomState(seed); L = int(sec*SR); ir = r.randn(L)*np.exp(-np.arange(L)/SR*6.5/sec); ir = lp(ir, 5000); ir /= np.sqrt((ir**2).sum())
    w = signal.fftconvolve(x, ir); y = np.zeros(len(w)); y[:len(x)] += x*(1-mix); y += w*mix*1.2; return y
def tt(d): return np.arange(int(d*SR))/SR
def knock():
    t = tt(0.35); return np.sin(2*np.pi*(95-30*t)*t)*np.exp(-t*22)+lp(rng.randn(len(t)), 900)*np.exp(-t*45)*0.8
def SFX(kind):
    if kind == 'knock': return rev(knock(), 1.2, 0.3), 0.9
    if kind == 'glass':
        t = tt(3); return rev((np.sin(2*np.pi*1244*t)+np.sin(2*np.pi*1318*t))*np.minimum(t/1.2, 1)*np.exp(-np.maximum(t-1.2, 0)*2), 2, 0.5), 0.06
    if kind == 'hit':
        t = tt(3); return rev(np.sin(2*np.pi*(55-15*t)*t)*np.exp(-t*2.5)+hp(rng.randn(len(t)), 3000)*np.exp(-t*20)*0.2, 3, 0.4), 0.7
    if kind == 'boom':
        t = tt(4); return rev(np.sin(2*np.pi*(45-12*t)*t)*np.exp(-t*1.2), 3.5, 0.4), 0.9
    if kind == 'slam':
        t = tt(2.5); s = np.sin(2*np.pi*(60-25*t)*t)*np.exp(-t*3)*1.2+hp(rng.randn(len(t)), 2500)*np.exp(-t*14)*0.7
        s += sum(np.sin(2*np.pi*f*t)*np.exp(-t*a) for f, a in [(1830, 5), (2710, 7), (3990, 9)])*0.25; return rev(s, 3.2, 0.4, 7), 1.0
    if kind == 'screech':
        t = tt(2.3); s = sum(signal.sawtooth(2*np.pi*(f0*(1+t*0.35))*t) for f0 in (180, 183.5, 271)); return rev(bp(s, 400, 3000)*(t/2.3)**2, 2, 0.4), 0.16
    if kind == 'steps':
        o = np.zeros(int(4.5*SR))
        for k in range(6):
            n = int(0.12*SR); i = int((k*0.7+rng.uniform(0, .05))*SR); o[i:i+n] += bp(rng.randn(n), 1500, 6000)*np.exp(-np.arange(n)/SR*30)
        return o, 0.08
    if kind == 'scratch':
        t = tt(1.6); return bp(rng.randn(len(t)), 2000, 7000)*(0.5+0.5*np.sin(2*np.pi*7*t))**2*np.exp(-t*1.2), 0.12
    if kind == 'page':
        t = tt(0.6); return hp(rng.randn(len(t)), 1500)*np.exp(-((t-0.2)/0.12)**2), 0.12
    if kind == 'ring':
        t = tt(4.0); env = ((t % 2.0) < 1.0).astype(float)
        return (np.sin(2*np.pi*440*t)+np.sin(2*np.pi*480*t))*env*0.5, 0.18
    if kind == 'static':
        t = tt(4.0); return bp(rng.randn(len(t)), 800, 6000)*(0.6+0.4*np.sin(2*np.pi*13*t)), 0.06
    if kind == 'engine':
        t = tt(6.0); return lp(signal.sawtooth(2*np.pi*42*t)+0.4*rng.randn(len(t)), 300)*np.minimum(t/2, 1), 0.18
    if kind == 'fire':
        t = tt(8.0); c = np.zeros(len(t))
        for i in rng.randint(0, len(t)-500, 120): c[i:i+500] += hp(rng.randn(500), 3000)*np.exp(-np.arange(500)/60)
        return lp(rng.randn(len(t)), 400)*0.4+c, 0.12
    if kind == 'birds':
        t = tt(6.0); o = np.zeros(len(t))
        for k in range(8):
            i = int(rng.uniform(0.5, 5)*SR); n = int(0.18*SR); tt_ = np.arange(n)/SR
            o[i:i+n] += np.sin(2*np.pi*(3200+800*np.sin(2*np.pi*12*tt_))*tt_)*np.sin(np.pi*tt_/0.18)
        return rev(o, 1.5, 0.3), 0.04
    if kind == 'heart':
        o = np.zeros(int(8*SR))
        for s in np.arange(0, 7.5, 0.85):
            for dt, f, a in [(0, 55, 0.6), (0.2, 50, 0.4)]:
                t = tt(0.25); i = int((s+dt)*SR); o[i:i+len(t)] += np.sin(2*np.pi*f*t)*np.exp(-t*18)*a
        return o, 0.8
    if kind == 'tick':
        o = np.zeros(int(12*SR)); n = int(0.02*SR)
        for s in np.arange(0.2, 11.5, 1.0): i = int(s*SR); o[i:i+n] += hp(rng.randn(n), 2500)*np.exp(-np.arange(n)/SR*300)
        return o, 0.1
    if kind.startswith('call_'):
        f = f'{WORK}/calls/{kind[5:]}.wav'
        if os.path.exists(f):
            _, x = wavfile.read(f); x = x.astype(np.float32); x /= np.abs(x).max()+1e-9; return rev(x, 2.4, 0.5, 2), 0.55
        return np.zeros(10), 0
    return np.zeros(10), 0

def mix(ep):
    shots, total = E.timeline(ep); N = int(total*SR)+SR
    t = np.arange(N)/SR; out = np.zeros(N)
    def place(s, at, g):
        i = int(at*SR); j = min(N, i+len(s)); out[i:j] += s[:j-i]*g
    # bed: wind + drone (tension rises across episode) + silence at endcard start
    w = np.cumsum(rng.randn(N)); w = hp(w, 30); w /= np.abs(w).max()
    lfo = 0.6+0.4*np.sin(2*np.pi*t*0.13)*np.sin(2*np.pi*t*0.051+1)
    wind = bp(rng.randn(N), 250, 1400)*lfo+lp(w, 300)*0.6; out += wind/np.abs(wind).max()*0.16
    dr = sum(a*np.sin(2*np.pi*f*t+0.3*np.sin(2*np.pi*0.07*t)) for f, a in [(55, 1), (55.4, .8), (82.4, .5), (110.6, .3)])
    ten = np.clip(t/total, 0, 1)**1.5
    dr = lp(dr, 600)+lp(sum(np.sin(2*np.pi*f*t)*0.25 for f in (233.1, 246.9, 261.6)), 900)*ten
    out += dr/np.abs(dr).max()*0.14
    for s in shots:
        tp = E.template(s['name'], s['p'], s['dur'])
        for at, kind in tp['sfx']:
            snd, g = SFX(kind)
            if kind in ('heart', 'tick', 'fire'): snd = snd[:int(s['dur']*SR)]; snd[-int(0.3*SR):] *= np.linspace(1, 0, int(0.3*SR))
            place(snd, s['start']+at, g)
    # end card stinger
    end = shots[-1]['start']; place(SFX('hit')[0], end, 0.8)
    # narration
    vo = load(f'{WORK}/ep{ep["no"]:02d}_vo.mp3'); voice = np.zeros(N)
    for s in shots:
        if not s['vo']: continue
        at, (a, b) = s['vo']; seg = vo[int(max(0, a-0.05)*SR):int((b+0.08)*SR)].copy(); f = int(0.02*SR)
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        i = int((at-0.05)*SR); voice[i:i+len(seg)] += seg[:N-i]
    voice = hp(voice, 80); env = np.sqrt(np.clip(lp(voice**2, 8), 0, None)); thr = 0.12
    voice *= np.where(env > thr, (thr/np.maximum(env, 1e-6))**0.5, 1.0); voice /= np.abs(voice).max()+1e-9
    ve = np.clip(lp(np.abs(voice), 3)/0.08, 0, 1); out = out/np.abs(out).max()*(1-0.55*ve)*0.55+voice*0.95
    out = np.tanh(out*1.05); st = np.stack([out, np.roll(out, 240)*0.97+out*0.03], 1)[:int(total*SR)]
    raw = f'{WORK}/ep{ep["no"]:02d}_mix_raw.wav'; wavfile.write(raw, SR, (st/np.abs(st).max()*0.9).astype(np.float32))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', f'{WORK}/ep{ep["no"]:02d}_mix.wav'], check=True)
    print('mix ok', total)

if __name__ == '__main__':
    cmd, no = sys.argv[1], int(sys.argv[2]); ep = Z.EP[no-1]
    {'align': align, 'mix': mix}[cmd](ep)
