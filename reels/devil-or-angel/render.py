import json, math, subprocess, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, TOTAL = 1080, 1920, 30, 60.0
LINES = json.load(open("lines.json"))
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def F(s): return ImageFont.truetype(FB, s)
f_hook, f_cap, f_lab, f_big, f_mid, f_psst = F(66), F(58), F(34), F(104), F(54), F(46)

# ---------- audio analysis + timeline ----------
def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
def env(p):
    raw = subprocess.check_output(["ffmpeg","-v","error","-i",p,"-ac","1","-ar","24000","-f","s16le","-"])
    a = np.frombuffer(raw, np.int16).astype(np.float32)/32768
    hop = 24000//FPS
    n = len(a)//hop + 1
    r = np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)) if a[i*hop:(i+1)*hop].size else 0 for i in range(n)])
    return np.clip(r/ (r.max()+1e-6) * 1.3, 0, 1)

GAP = {4:0.4,10:0.4}
t = 0.5
timeline = []
for i,(who,text,style) in enumerate(LINES):
    p = f"audio/{i:02d}.wav"
    d = dur(p)
    timeline.append(dict(i=i,who=who,text=text,style=style,start=t,end=t+d,env=env(p)))
    t += d + GAP.get(i,0.22)
END_CARD = timeline[-1]["end"] + 0.35
json.dump([dict(i=x["i"],start=x["start"],end=x["end"]) for x in timeline] + [{"endcard":END_CARD}], open("timeline.json","w"), indent=1)
print("dialogue ends", timeline[-1]["end"], "endcard at", END_CARD)

def current(tt):
    for x in timeline:
        if x["start"] <= tt < x["end"]: return x
    return None
def last_line(tt):
    c = None
    for x in timeline:
        if x["start"] <= tt: c = x
    return c
def amp(x, tt):
    k = int((tt-x["start"])*FPS)
    return float(x["env"][k]) if 0 <= k < len(x["env"]) else 0.0
def ease(v): v=max(0,min(1,v)); return v*v*(3-2*v)

# ---------- static background ----------
SCN_H = 1080
def background():
    im = Image.new("RGB",(W,SCN_H))
    d = ImageDraw.Draw(im)
    for y in range(SCN_H):
        k = y/SCN_H
        d.line([(0,y),(W,y)], fill=(int(64+30*k), int(52+22*k), int(86+10*k)))
    # window with night sky + moon
    d.rounded_rectangle([90,120,430,470], 18, fill=(28,34,74), outline=(230,200,150), width=12)
    d.line([(260,120),(260,470)], fill=(230,200,150), width=8); d.line([(90,295),(430,295)], fill=(230,200,150), width=8)
    d.ellipse([320,150,390,220], fill=(250,240,200))
    random.seed(3)
    for _ in range(18):
        x,y = random.randint(105,415), random.randint(135,455); d.ellipse([x,y,x+4,y+4], fill=(255,255,220))
    # wall frame (heart)
    d.rounded_rectangle([680,150,960,380], 10, fill=(245,230,210), outline=(150,100,60), width=12)
    d.polygon([(820,330),(745,255),(770,215),(820,240),(870,215),(895,255)], fill=(230,90,110))
    # lamp
    d.rectangle([985,330,1000,760], fill=(80,60,50)); d.polygon([(930,250),(1055,250),(1030,340),(955,340)], fill=(255,220,150))
    glow = Image.new("RGB",(W,SCN_H),(0,0,0)); ImageDraw.Draw(glow).ellipse([820,180,1160,520], fill=(90,70,30))
    im = Image.blend(im, Image.composite(glow, im, Image.new("L",(W,SCN_H),0)), 0)
    im = Image.fromarray(np.clip(np.asarray(im).astype(int)+np.asarray(glow.filter(ImageFilter.GaussianBlur(70))).astype(int),0,255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    # floor + rug
    d.rectangle([0,930,W,SCN_H], fill=(120,80,60))
    d.ellipse([140,960,940,1070], fill=(170,70,80))
    # couch back
    d.rounded_rectangle([60,560,1020,860], 60, fill=(52,110,120))
    return im
BG = background()
def couch_front(d):
    d.rounded_rectangle([40,800,1040,960], 50, fill=(62,128,138))
    d.rounded_rectangle([20,640,150,960], 50, fill=(45,98,108))
    d.rounded_rectangle([930,640,1060,960], 50, fill=(45,98,108))
    d.rectangle([90,950,130,1000], fill=(60,40,30)); d.rectangle([950,950,990,1000], fill=(60,40,30))

# ---------- characters ----------
SKIN_H, SKIN_W = (214,160,120), (240,195,165)
def head(female, mouth, expr, look, blink, horns=0.0, halo=0.0, tt=0.0):
    L = Image.new("RGBA",(520,560),(0,0,0,0)); d = ImageDraw.Draw(L)
    cx, cy = 260, 300
    skin = SKIN_W if female else SKIN_H
    if halo > 0:
        a = int(255*halo); yy = 70 + 6*math.sin(tt*4)
        d.ellipse([150,yy,370,yy+50], outline=(255,225,90,a), width=16)
    if female:  # long hair behind
        d.rounded_rectangle([cx-150,cy-160,cx+150,cy+190], 90, fill=(70,38,30))
    # ears
    d.ellipse([cx-142,cy-20,cx-100,cy+45], fill=skin); d.ellipse([cx+100,cy-20,cx+142,cy+45], fill=skin)
    d.ellipse([cx-120,cy-140,cx+120,cy+140], fill=skin)
    if female:
        d.chord([cx-128,cy-158,cx+128,cy+40], 180, 360, fill=(70,38,30))
        d.pieslice([cx-128,cy-150,cx+40,cy+10], 180, 300, fill=(70,38,30))
        if not halo:
            d.ellipse([cx+90,cy-150,cx+140,cy-100], fill=(230,90,110))  # hair clip
    else:
        d.chord([cx-125,cy-150,cx+125,cy-10], 180, 360, fill=(40,30,28))
        d.polygon([(cx-125,cy-80),(cx-60,cy-125),(cx+40,cy-150),(cx+125,cy-80),(cx+125,cy-100),(cx-125,cy-100)], fill=(40,30,28))
    if horns > 0:
        h = 70*horns
        for s in (-1,1):
            bx = cx + s*70
            d.polygon([(bx-24,cy-118),(bx+24,cy-118),(bx+s*30,cy-118-h)], fill=(210,30,40))
    # eyes
    ex = [cx-48, cx+48]; ey = cy-10
    lx = {"left":-9,"right":9,"center":0,"up":0}[look]; ly = -8 if look=="up" else 0
    for x in ex:
        if blink or expr=="happy":
            d.arc([x-26,ey-14,x+26,ey+18], 200, 340, fill=(40,30,30), width=7)
        else:
            d.ellipse([x-26,ey-24,x+26,ey+24], fill=(255,255,255))
            d.ellipse([x-13+lx,ey-13+ly,x+13+lx,ey+13+ly], fill=(45,35,40))
            d.ellipse([x-5+lx,ey-8+ly,x+1+lx,ey-2+ly], fill=(255,255,255))
            if female:
                d.line([(x-26,ey-20),(x-34,ey-30)], fill=(30,20,20), width=5); d.line([(x+26,ey-20),(x+34,ey-30)], fill=(30,20,20), width=5)
    # brows
    by = ey-48
    for s,x in ((-1,ex[0]),(1,ex[1])):
        if expr in ("annoyed","angry"):
            inner, outer = by+ (18 if expr=="angry" else 12), by-4
        elif expr in ("confused","raised"):
            inner, outer = by-14, by-4
        elif expr=="sly":
            inner, outer = (by+6, by-10) if s<0 else (by-14, by-2)
        else:
            inner, outer = by-4, by-4
        xi, xo = x - s*26, x + s*26
        d.line([(xi,inner),(xo,outer)], fill=(40,25,20), width=10)
    # blush
    if female or expr in ("sly","happy"):
        d.ellipse([cx-100,cy+30,cx-60,cy+55], fill=(240,140,140,140)); d.ellipse([cx+60,cy+30,cx+100,cy+55], fill=(240,140,140,140))
    # nose
    d.arc([cx-14,cy+5,cx+14,cy+40], 20, 160, fill=(150,100,80), width=5)
    # mouth
    my = cy+78
    if mouth > 0.12:
        mh = 10 + 46*mouth; mw = 34 + 14*mouth
        d.ellipse([cx-mw,my-mh/2,cx+mw,my+mh/2], fill=(110,30,40))
        d.ellipse([cx-mw*0.55,my+mh/2-mh*0.45,cx+mw*0.55,my+mh/2], fill=(230,110,120))
    elif expr in ("annoyed","angry"):
        d.arc([cx-34,my-4,cx+34,my+40], 200, 340, fill=(110,40,40), width=8)
    elif expr=="sly":
        d.arc([cx-40,my-40,cx+30,my+10], 20, 130, fill=(110,40,40), width=8)
    else:
        d.arc([cx-40,my-40,cx+40,my+14], 25, 155, fill=(110,40,40), width=8)
    if female:
        d.line([(cx-30,my-1),(cx+30,my-1)], fill=(200,70,90), width=0)
    return L

def body(d, cx, female, lean):
    shirt = (230,120,150) if female else (70,100,170)
    sx = cx + lean*0.35
    d.polygon([(cx-140,840),(cx+140,840),(sx+110,620),(sx-110,620)], fill=shirt)
    d.ellipse([sx-120,590,sx+120,690], fill=shirt)
    d.rounded_rectangle([sx-30,560,sx+30,620], 10, fill=SKIN_W if female else SKIN_H)
    # legs
    pants = (60,60,80) if female else (50,60,70)
    d.rounded_rectangle([cx-125,820,cx+125,900], 40, fill=pants)
    d.rectangle([cx-110,880,cx-30,1010], fill=pants); d.rectangle([cx+30,880,cx+110,1010], fill=pants)
    d.ellipse([cx-125,990,cx-15,1040], fill=(40,40,45)); d.ellipse([cx+15,990,cx+125,1040], fill=(40,40,45))

# ---------- per-line acting ----------
WHISPER = {0,2,4,12,14}
H_EXPR = {0:"sly",2:"sly",4:"sly",5:"confused",6:"confused",7:"confused",8:"confused",9:"confused",10:"raised",11:"neutral",12:"happy",13:"happy",14:"sly",15:"raised"}
W_EXPR = {0:"annoyed",1:"annoyed",2:"annoyed",3:"annoyed",4:"annoyed",5:"angry",6:"annoyed",7:"annoyed",8:"annoyed",9:"neutral",10:"annoyed",11:"neutral",12:"happy",13:"neutral",14:"annoyed",15:"angry"}

def wrap(text, font, maxw, d):
    words, lines, cur = text.split(), [], []
    for w in words:
        if d.textlength(" ".join(cur+[w]), font=font) > maxw and cur: lines.append(cur); cur=[w]
        else: cur.append(w)
    lines.append(cur); return lines

def outlined(d, xy, txt, font, fill, stroke=(0,0,0), sw=6, anchor="la"):
    d.text(xy, txt, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)

def frame(n):
    tt = n/FPS
    cur = current(tt); lastl = last_line(tt); li = lastl["i"] if lastl else -1
    # lean state: husband leans in during whisper lines (with anticipation)
    lean_target = 0.0
    for x in timeline:
        if x["i"] in WHISPER and x["start"]-0.45 <= tt <= x["end"]+0.25:
            lean_target = max(lean_target, ease((tt-(x["start"]-0.45))/0.4) * ease((x["end"]+0.25-tt)/0.35))
    lean = lean_target
    # horns / halo
    horns = 0.0
    if 5 <= li <= 10: horns = ease((tt-timeline[5]["start"])/0.3)
    if li == 11: horns = 1-ease((tt-timeline[11]["start"])/0.5)
    if li >= 15: horns = ease((tt-timeline[15]["start"])/0.2)
    halo = 0.0
    if 12 <= li <= 13: halo = ease((tt-timeline[12]["start"])/0.5)
    if li == 14: halo = 1-ease((tt-timeline[14]["start"])/0.3)

    scene = BG.copy(); d = ImageDraw.Draw(scene)
    hx0, wx = 370, 720
    hx = hx0 + 85*lean
    body(d, hx0, False, 150*lean*1.2)
    body(d, wx, True, -20*lean)
    couch_front(d)
    # heads
    blinkH = (n % 113) < 4; blinkW = ((n+57) % 131) < 4
    hm = amp(cur, tt) if cur and cur["who"]=="H" else 0
    wm = amp(cur, tt) if cur and cur["who"]=="W" else 0
    if cur and cur["who"]=="H" and cur["i"] in WHISPER: hm *= 0.6
    hexp = H_EXPR.get(li, "sly"); wexp = W_EXPR.get(li, "annoyed")
    hlook = "right"
    wlook = "left" if (cur and (cur["who"]=="W")) or li in (5,7,9,11,13,15) else ("up" if li in (0,2,4,14) and lean>0.3 else "left")
    hh = head(False, hm, hexp, hlook, blinkH, horns, halo, tt)
    wh = head(True, wm, wexp, wlook, blinkW, 0, 0, tt)
    bob = 4*math.sin(tt*2.2)
    hang = -14*lean
    wang = 6*lean if li in (0,2,4,14) else (-4 if li in (5,7,9,11,15) else 0)
    if li == 1 or li == 3: wang = 4  # head turned away "No."
    wh_r = wh.rotate(wang, resample=Image.BICUBIC, center=(260,300))
    hh_r = hh.rotate(hang, resample=Image.BICUBIC, center=(260,300))
    scene.paste(wh_r, (int(wx-260), int(300+bob*0.7)), wh_r)
    scene.paste(hh_r, (int(hx-260+25*lean), int(300+bob+20*lean)), hh_r)
    # psst bubbles
    if cur and cur["who"]=="H" and cur["i"] in WHISPER:
        k = (tt-cur["start"])
        for j in range(3):
            ph = (k*1.4 + j*0.33) % 1.0
            x = wx-60 + 50*j + 40*ph; y = 430 - 150*ph
            a = int(255*(1-ph))
            txt = Image.new("RGBA",(260,80),(0,0,0,0)); td = ImageDraw.Draw(txt)
            td.text((10,10),"psst..." if j!=1 else "~", font=f_psst, fill=(255,255,255,a), stroke_width=4, stroke_fill=(60,40,90,a))
            scene.paste(txt,(int(x),int(y)),txt)
    # devil or angel question badges
    if li == 9 and cur:
        k = ease((tt-timeline[9]["start"])/0.4)
        for s,(lab1,lab2,col) in ((-1,("DEVIL","BAD SIDE",(200,30,45))),(1,("ANGEL","GOOD SIDE",(240,190,60)))):
            cx = 540 + s*260; y = int(60 + (1-k)*-200)
            d.rounded_rectangle([cx-200,y,cx+200,y+170], 30, fill=col, outline=(255,255,255), width=6)
            d.text((cx,y+58), lab1+"?", font=f_mid, fill=(255,255,255), anchor="mm", stroke_width=3, stroke_fill=(0,0,0))
            d.text((cx,y+125), lab2, font=f_lab, fill=(255,255,255), anchor="mm")
        d.text((540,int(60+85+(1-k)*-200)),"vs", font=f_mid, fill=(255,255,255), anchor="mm", stroke_width=4, stroke_fill=(0,0,0))
    # color grading: red for devil accusations, gold for angel
    arr = np.asarray(scene).astype(np.float32)
    red = 0.0
    for idx in (5,15):
        x = timeline[idx]
        if x["start"]-0.1 <= tt <= x["end"]+0.6: red = max(red, ease((tt-x["start"]+0.1)/0.25)*ease((x["end"]+0.6-tt)/0.5))
    if red: arr = arr*(1-0.35*red) + np.array([200,20,30])*0.35*red
    if halo: arr = arr*(1-0.18*halo) + np.array([255,215,120])*0.18*halo
    scene = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    # punch-in zoom on "Are you the devil?" and final "Devil!"
    z = 1.0
    for idx,amt in ((5,0.12),(15,0.18),(9,0.05)):
        x = timeline[idx]
        if x["start"] <= tt <= x["end"]+0.8: z = max(z, 1+amt*ease((tt-x["start"])/0.25))
    if z > 1.001:
        cw, ch = W/z, SCN_H/z; cx0 = (W-cw)/2 + (60 if z>1.1 else 0); cy0 = (SCN_H-ch)/2 - 60*(z-1)
        scene = scene.crop((cx0,cy0,cx0+cw,cy0+ch)).resize((W,SCN_H), Image.BICUBIC)
    # shake on sting
    shx = shy = 0
    for idx in (5,15):
        k = tt - timeline[idx]["start"]
        if 0 <= k < 0.5: shx = int(14*math.sin(k*90)*(1-k/0.5)); shy = int(10*math.cos(k*70)*(1-k/0.5))

    out = Image.new("RGB",(W,H),(18,14,26)); od = ImageDraw.Draw(out)
    out.paste(scene,(shx,330+shy))
    # hook header
    od.rectangle([0,0,W,330], fill=(18,14,26))
    od.text((540,110),"When he keeps", font=f_hook, fill=(255,255,255), anchor="mm")
    od.text((540,200),"whispering in your ear...", font=f_hook, fill=(255,214,70), anchor="mm")
    od.text((540,285),"devil or angel?", font=f_lab, fill=(200,190,220), anchor="mm")
    # captions
    od.rectangle([0,1410,W,H], fill=(18,14,26))
    show = cur or (lastl if lastl and tt-lastl["end"] < 0.35 else None)
    if show:
        who = "HIM" if show["who"]=="H" else "HER"
        col = (120,170,255) if show["who"]=="H" else (255,140,180)
        if show["i"] in WHISPER: who += "  (whispering)"
        od.rounded_rectangle([60,1450,60+od.textlength(who,font=f_lab)+44,1508], 22, fill=col)
        od.text((82,1479), who, font=f_lab, fill=(20,15,30), anchor="lm")
        words = show["text"].split()
        prog = (tt-show["start"])/(show["end"]-show["start"]+1e-6)
        nshown = len(words) if not cur else max(1, int(math.ceil(prog*len(words)*1.08)))
        lines = wrap(show["text"], f_cap, W-140, od)
        y = 1545; wi = 0
        for ln in lines[:5]:
            x = 70
            for w in ln:
                if wi < nshown:
                    c = (255,214,70) if wi == nshown-1 and cur else (255,255,255)
                    outlined(od,(x,y),w,f_cap,c,sw=4)
                x += od.textlength(w+" ", font=f_cap); wi += 1
            y += 74
    # end card
    if tt >= END_CARD:
        k = ease((tt-END_CARD)/0.5)
        ov = Image.new("RGB",(W,H),(22,14,40)); out = Image.blend(out, ov, 0.9*k); od = ImageDraw.Draw(out)
        a = lambda c: tuple(int(v*k) for v in c)
        od.text((540,640),"Don't be a", font=f_mid, fill=a((255,255,255)), anchor="mm")
        od.text((540,760),"DEVIL.", font=f_big, fill=a((235,50,60)), anchor="mm", stroke_width=4, stroke_fill=(0,0,0))
        od.text((540,900),"Be an", font=f_mid, fill=a((255,255,255)), anchor="mm")
        od.text((540,1020),"ANGEL.", font=f_big, fill=a((255,214,70)), anchor="mm", stroke_width=4, stroke_fill=(0,0,0))
        yy = 1130 + 6*math.sin(tt*4)
        od.ellipse([400,yy,680,yy+60], outline=a((255,214,70)), width=12)
        od.text((540,1330),"Whisper what lifts them up.", font=f_mid, fill=a((220,210,240)), anchor="mm")
        od.text((540,1460),"Tag the one who's always", font=f_lab, fill=a((200,190,220)), anchor="mm")
        od.text((540,1510),"in your ear", font=f_lab, fill=a((200,190,220)), anchor="mm")
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for s in sys.argv[1:]:
            frame(int(float(s)*FPS)).save(f"preview_{s}.png")
        sys.exit()
    p = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
                          "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","video_only.mp4"], stdin=subprocess.PIPE)
    for n in range(int(TOTAL*FPS)):
        p.stdin.write(frame(n).tobytes())
    p.stdin.close(); p.wait()
