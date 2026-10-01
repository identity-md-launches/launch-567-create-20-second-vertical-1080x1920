"""Offline, deterministic Swarm Pepes animation. Run: python3 src/render.py"""
from pathlib import Path
import sys, math, random, array, wave, subprocess, tarfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts'; TMP=ROOT/'test/scratch'; OUT.mkdir(exist_ok=True); TMP.mkdir(parents=True,exist_ok=True)
# Only disposable scratch receives extracted tools and Python bytecode.
RUNTIME=TMP/'runtime'
with tarfile.open(ROOT/'vendor/render-runtime.tar.xz') as tar:
    tar.extractall(RUNTIME,filter='data')
sys.dont_write_bytecode=True
sys.path.insert(0,str(RUNTIME/'python'))
from PIL import Image, ImageDraw
BIN=RUNTIME/'bin/ffmpeg'; PROBE=BIN.with_name('ffprobe')
# Hand-authored 5x7 lettering, no external fonts or artwork.
DATA='''A 01110 10001 10001 11111 10001 10001 10001
B 11110 10001 10001 11110 10001 10001 11110
C 01111 10000 10000 10000 10000 10000 01111
D 11110 10001 10001 10001 10001 10001 11110
E 11111 10000 10000 11110 10000 10000 11111
F 11111 10000 10000 11110 10000 10000 10000
G 01111 10000 10000 10111 10001 10001 01111
H 10001 10001 10001 11111 10001 10001 10001
I 11111 00100 00100 00100 00100 00100 11111
J 00111 00010 00010 00010 10010 10010 01100
K 10001 10010 10100 11000 10100 10010 10001
L 10000 10000 10000 10000 10000 10000 11111
M 10001 11011 10101 10101 10001 10001 10001
N 10001 11001 11001 10101 10011 10011 10001
O 01110 10001 10001 10001 10001 10001 01110
P 11110 10001 10001 11110 10000 10000 10000
Q 01110 10001 10001 10001 10101 10010 01101
R 11110 10001 10001 11110 10100 10010 10001
S 01111 10000 10000 01110 00001 00001 11110
T 11111 00100 00100 00100 00100 00100 00100
U 10001 10001 10001 10001 10001 10001 01110
V 10001 10001 10001 10001 10001 01010 00100
W 10001 10001 10001 10101 10101 10101 01010
X 10001 10001 01010 00100 01010 10001 10001
Y 10001 10001 01010 00100 00100 00100 00100
Z 11111 00001 00010 00100 01000 10000 11111
0 01110 10001 10011 10101 11001 10001 01110
1 00100 01100 00100 00100 00100 00100 01110
2 01110 10001 00001 00010 00100 01000 11111
3 11110 00001 00001 01110 00001 00001 11110
4 00010 00110 01010 10010 11111 00010 00010
5 11111 10000 10000 11110 00001 00001 11110
6 01110 10000 10000 11110 10001 10001 01110
7 11111 00001 00010 00100 01000 01000 01000
8 01110 10001 10001 01110 10001 10001 01110
9 01110 10001 10001 01111 00001 00001 01110
% 11001 11010 00010 00100 01000 01011 10011
? 01110 10001 00001 00010 00100 00000 00100
! 00100 00100 00100 00100 00100 00000 00100
. 00000 00000 00000 00000 00000 00110 00110
: 00000 00110 00110 00000 00110 00110 00000
/ 00001 00010 00010 00100 01000 01000 10000
- 00000 00000 00000 11111 00000 00000 00000'''
FONT={r.split()[0]:r.split()[1:] for r in DATA.splitlines()}
GREEN='#8bff55'; GOLD='#ffd65a'; INK='#080d1a'; WHITE='#e7f6d7'; MUTED='#77889b'
def txt(d,s,x,y,scale=1,color=WHITE,center=True):
    if center:x-= (len(s)*6-1)*scale//2
    for c in s.upper():
        for j,row in enumerate(FONT.get(c,[])):
            for i,v in enumerate(row):
                if v=='1':d.rectangle((x+i*scale,y+j*scale,x+(i+1)*scale-1,y+(j+1)*scale-1),fill=color)
        x+=6*scale

def pepe(im,x,y,size=1,gold=False,hat='cap'):
    p=Image.new('RGBA',(64,66)); d=ImageDraw.Draw(p)
    skin='#f4bf3c' if gold else '#65b94d'; shadow='#ad6f27' if gold else '#347b3c'; hi='#ffe78b' if gold else '#99dc65'
    d.polygon([(5,65),(8,53),(18,47),(47,47),(57,55),(61,65)],fill='#554596' if not gold else '#76552c')
    d.polygon([(8,25),(14,16),(25,13),(32,17),(46,14),(54,22),(58,38),(53,48),(43,54),(22,55),(10,47),(5,36)],fill=INK)
    d.polygon([(10,26),(16,19),(25,16),(33,20),(46,17),(52,23),(55,38),(50,46),(41,51),(22,52),(12,45),(8,35)],fill=skin)
    d.polygon([(10,37),(17,44),(44,45),(54,36),(51,47),(41,51),(23,52),(12,45)],fill=shadow)
    d.rectangle((14,23,28,34),fill=WHITE); d.rectangle((35,22,49,33),fill=WHITE)
    d.rectangle((22,25,26,33),fill=INK); d.rectangle((37,24,41,32),fill=INK)
    d.line([(13,24),(20,21),(28,24)],fill=shadow,width=3); d.line([(34,23),(43,20),(50,24)],fill=shadow,width=3)
    d.line([(16,40),(23,42),(44,42),(49,39)],fill=INK,width=3)
    d.line([(20,46),(40,47),(46,44)],fill='#dc8c4a' if gold else '#b87f59',width=2)
    d.rectangle((10,31,12,35),fill=hi)
    if hat=='crown':
        d.polygon([(13,16),(10,2),(22,8),(30,0),(40,8),(53,2),(49,17)],fill=INK)
        d.polygon([(16,13),(14,6),(23,11),(30,4),(39,11),(49,6),(46,14)],fill=GOLD)
        d.rectangle((15,14,48,18),fill='#f8a927'); d.rectangle((29,12,33,16),fill='#ff566e')
    elif hat=='cap':
        d.rectangle((15,11,42,18),fill='#59667f'); d.rectangle((11,17,51,20),fill='#939eac')
    elif hat=='beanie':
        d.rectangle((16,10,43,18),fill='#ab7761');d.rectangle((13,17,47,21),fill='#db9f70')
    im.alpha_composite(p.resize((int(64*size),int(66*size)),Image.Resampling.NEAREST),(int(x),int(y)))

def icon(im,kind,val,x,y):
    d=ImageDraw.Draw(im)
    if kind==0:pepe(im,x+7,y+3,.65,val=='GOLD','none')
    elif kind==1:
        if val=='CROWN':
            d.polygon([(x+9,y+33),(x+5,y+9),(x+19,y+20),(x+27,y+5),(x+36,y+20),(x+49,y+9),(x+45,y+33)],fill=GOLD)
            d.rectangle((x+10,y+33,x+44,y+38),fill='#bb7c24'); d.rectangle((x+25,y+25,x+29,y+30),fill='#ff657d')
        else:
            d.rectangle((x+13,y+15,x+39,y+31),fill='#8897ad' if val=='CAP' else '#b98770');d.rectangle((x+7,y+29,x+46,y+35),fill='#c7cfce')
    else:
        d.rectangle((x+9,y+8,x+46,y+38),fill={'BLUE':'#376086','GRAY':'#647380','DUSK':'#855f83','GOLD':'#d3a638'}[val]);d.rectangle((x+13,y+12,x+18,y+17),fill='#d7e7ab')

def frame(t):
    im=Image.new('RGBA',(270,480),INK);d=ImageDraw.Draw(im)
    for k in range(43):
        x=(k*97+13)%270;y=(k*61+int(t*3))%480
        d.rectangle((x,y,x+1,y+1),fill='#253342')
    for y in range(348,480,18):d.line((0,y,270,y),fill='#14272c')
    for x in range(-150,450,45):d.line((135,320,x,480),fill='#14272c')
    txt(d,'SWARM PEPES',135,18,2,GREEN)
    txt(d,'ONCHAIN / ETHEREUM',135,39,1,MUTED)
    if t<16:
        if t<3:
            txt(d,'CAN YOU HIT',135,66,2,WHITE)
            txt(d,'THE 1%?',135,88,3,GOLD if int(t*4)%2 else GREEN)
        elif t<11:
            n=min(2,int((t-3)/ (8/3)))
            txt(d,['SURELY THIS ONE.','ONE MORE TRY.','OK. ONE MORE.'][n],135,78,1,GREEN)
            txt(d,f'PULL 0{n+1} / 04',135,99,1,MUTED)
        else:
            txt(d,'WAIT FOR IT...' if t<14.2 else '1% ENERGY',135,74,2,GOLD)
            txt(d,'PULL 04 / 04',135,99,1,MUTED)
        machine=Image.new('RGBA',(270,265));m=ImageDraw.Draw(machine)
        m.rectangle((26,12,239,257),fill='#030711');m.rectangle((21,6,232,249),fill='#30484b');m.rectangle((25,10,228,245),fill='#101d2a',outline=GREEN,width=2)
        m.rectangle((32,17,221,49),fill='#263b35');txt(m,'TRAIT JACKPOT',127,25,2,GREEN)
        for k in range(15):
            color=GOLD if (k+int(t*8))%3==0 else '#496044';m.rectangle((33+k*13,55,37+k*13,59),fill=color)
        labels=['SKIN','HAT','BACKGROUND']
        starts=[3,17/3,25/3];lands=[4.7,7.35,10.0]
        current=max([i for i,s in enumerate(starts) if t>=s],default=0)
        spinning=False
        for k,x in enumerate([34,97,160]):
            txt(m,labels[k],x+27,69,1,WHITE)
            m.rectangle((x-2,82,x+57,153),fill='#65796b');m.rectangle((x,85,x+55,150),fill='#090f1c')
            val=['GREEN',['CAP','BEANIE','CAP'][current],['BLUE','GRAY','DUSK'][current]][k]
            if t<3:val=['GREEN','CAP','BLUE'][k]
            final=t>=11
            stop=[14.15,14.85,15.15][k] if final else lands[current]+k*.12
            active=(t>=11 and t<stop) if final else (t>=starts[current] and t<stop)
            if final and not active:val=['GOLD','CROWN','GOLD'][k]
            if active:
                spinning=True
                u=t-11
                travel=t*19 if not final else 23*u-2.8*u*u
                phase=travel%1; options=[['GREEN','GOLD','GREEN'],['CAP','CROWN','BEANIE'],['BLUE','GOLD','DUSK']][k]
                val=options[int(travel)%3]
                tile=Image.new('RGBA',(56,64),'#090f1c')
                for offset in [-64,0,64]:icon(tile,k,val,0,int(phase*64)+offset)
                machine.alpha_composite(tile,(x,86))
                for streak in range(3):m.line((x+4+streak*19,90,x+4+streak*19,99),fill='#4d6954')
            else:icon(machine,k,val,x,94)
            txt(m,val if not active else '???',x+27,161,1,GOLD if final else GREEN)
            m.line((x,118,x+55,118),fill='#344638')
        m.polygon([(27,115),(33,120),(27,125)],fill=GOLD);m.polygon([(223,115),(217,120),(223,125)],fill=GOLD)
        m.rectangle((36,183,216,213),fill='#040b12',outline='#354e4b')
        status='SPINNING...' if spinning else ('JACKPOT!!!' if t>=14.85 else 'COMMON' if t>=4.7 else '4 PULLS. 1 DREAM.')
        txt(m,status,126,193,1,GOLD if final else GREEN)
        txt(m,'FULLY ONCHAIN',127,229,1,MUTED)
        pull=max(0,1-abs(t-2.65)/.32)
        for s in starts[1:]+[11]:pull=max(pull,max(0,1-abs(t-s)/.25))
        ly=int(75+pull*70);m.rectangle((234,110,243,145),fill='#647b78');m.line((240,126,248,ly),fill='#a6b6a1',width=4);m.rectangle((242,ly-6,255,ly+7),fill=GOLD)
        shake=0 if t<12 else (1 if t<14.2 else 3)
        sx=int(math.sin(t*107)*shake);sy=int(math.cos(t*83)*shake)
        im.alpha_composite(machine,(sx,122+sy));d=ImageDraw.Draw(im)
        for i,land in enumerate(lands):
            if t>=land+.3:
                age=t-land-.3; py=392-int(max(0,1-age*3)*22)
                pepe(im,29+i*78,py,.72,False,['cap','beanie','cap'][i]); txt(d,'COMMON',52+i*78,446,1,MUTED)
        if t>=14.85:
            rng=random.Random(50)
            for i in range(95):
                x=rng.randrange(270); y=int((rng.randrange(480)+(t-14.85)*rng.randrange(35,145))%480)
                d.rectangle((x,y,x+2,y+4),fill=[GOLD,GREEN,WHITE,'#ff7474'][i%4])
        txt(d,'SWARMPEPE.XYZ',135,469,1,'#516c63')
    else:
        age=t-16
        # Stepped pixel rays and alternating aureole around the hero.
        for k in range(16):
            a=k*math.pi/8+t*.15
            pts=[(135+math.cos(a)*64,230+math.sin(a)*64),(135+math.cos(a-.045)*330,230+math.sin(a-.045)*330),(135+math.cos(a+.045)*330,230+math.sin(a+.045)*330)]
            d.polygon(pts,fill='#272418' if k%2 else '#1d221c')
        d.rectangle((0,0,269,54),fill=INK)
        txt(d,'SWARM PEPES',135,18,2,GREEN);txt(d,'ONCHAIN / ETHEREUM',135,39,1,MUTED)
        for r in [113,105,96]:d.rectangle((135-r,221-r,135+r,221+r),outline='#655128' if r==105 else '#302d1d',width=2)
        txt(d,'THE 1%.',135,68,4,GOLD)
        bob=int(math.sin(age*3)*2);pepe(im,23,121+bob,3.5,True,'crown');d=ImageDraw.Draw(im)
        for i in range(24):
            x=(i*71+9)%270;y=(i*47+int(t*16))%370+67
            if (i+int(t*5))%3==0:d.line((x-2,y,x+2,y),fill=GOLD);d.line((x,y-2,x,y+2),fill=GOLD)
        d.rectangle((11,362,259,416),fill=INK,outline='#68532b')
        txt(d,'GOLD SKIN: 1%.',135,373,2,GOLD);txt(d,'CROWN: 3%.',135,395,2,WHITE)
        if t>=18:txt(d,'SWARMPEPE.XYZ',135,438,2,GREEN)
        else:txt(d,'RARE LOOK. ONCHAIN SOUL.',135,441,1,GREEN)
        txt(d,'SWARM PEPES',135,468,1,MUTED)
    # Restrained CRT lines keep all type legible.
    overlay=Image.new('RGBA',im.size); od=ImageDraw.Draw(overlay)
    for y in range(1,480,3):od.line((0,y,269,y),fill=(0,0,0,30))
    im=Image.alpha_composite(im,overlay)
    for at in [14.15,14.85,16]:
        if 0<=t-at<.12:im=Image.blend(im,Image.new('RGBA',im.size,'#ffe8a0'),.65*(1-(t-at)/.12))
    return im.convert('RGB')

# Original pulse-wave score with arpeggios, noise drums, reel ticks, and a reveal drop.
SR=44100; samples=array.array('f',[0])*(20*SR)
def tone(at,dur,hz,vol=.1,kind='square',slide=0):
    start=int(at*SR);n=min(int(dur*SR),len(samples)-start);phase=0;rng=random.Random(start)
    for i in range(n):
        u=i/SR;phase+=(hz+slide*u/dur)/SR
        v=(1 if phase%1<.3 else -.43) if kind=='square' else math.sin(phase*2*math.pi) if kind=='sine' else rng.uniform(-1,1)
        env=min(1,i/180)*max(0,1-i/n)**(2 if kind=='noise' else .6)
        samples[start+i]+=vol*v*env
notes=[64,67,71,76,71,67,62,67]
at=0;step=0
while at<20:
    beat=.25 if at<11 else max(.105,.25-(at-11)*.03) if at<16 else .30
    if at>=16:note=[52,59,64,67,71,76,79,83][step%8]
    else:note=notes[step%8]
    tone(at,beat*.8,440*2**((note-69)/12),.095)
    if step%2==0:tone(at,beat*1.7,440*2**(((40 if step%8<4 else 43)-69)/12),.12)
    if step%4==0:tone(at,.16,110,.19,'sine',-75)
    if step%4==2:tone(at,.09,0,.09,'noise')
    tone(at,.035,0,.035,'noise')
    at+=beat;step+=1
for land in [4.7,7.35,10]:
    tone(land,.12,390,.14);tone(land+.13,.22,195,.12)
for at in [3,17/3,25/3,11]:
    tone(at,.12,0,.15,'noise')
for k in range(30):tone(11+k*.1,.025,800+k*35,.035)
for at,note in [(14.15,79),(14.85,86)]:tone(at,.5,440*2**((note-69)/12),.16)
tone(16,1.4,90,.3,'sine',-65);tone(16,.6,0,.18,'noise')
for midi in [48,60,64,67,72,76,79]:tone(16,1.4,440*2**((midi-69)/12),.055)
peak=max(abs(x) for x in samples); pcm=array.array('h')
for i,x in enumerate(samples):
    fade=min(1,(len(samples)-i)/(SR*.3));pcm.append(int(x/peak*.88*32767*fade))
with wave.open(str(TMP/'score.wav'),'wb') as w:w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes(pcm.tobytes())
args=[str(BIN),'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','270x480','-r','30','-i','pipe:0','-i',str(TMP/'score.wav'),'-vf','scale=1080:1920:flags=neighbor','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','44100','-movflags','+faststart','-t','20',str(OUT/'video.mp4')]
with (TMP/'encode.log').open('w') as log:
    p=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
    for i in range(600):
        p.stdin.write(frame(i/30).tobytes())
        if i%90==0:print(f'Rendered {i}/600',flush=True)
    p.stdin.close()
    if p.wait():raise RuntimeError('Encoding failed; see test/scratch/encode.log')
report=subprocess.check_output([str(PROBE),'-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,pix_fmt,r_frame_rate,sample_rate,channels,duration','-of','json',str(OUT/'video.mp4')])
(OUT/'probe.json').write_bytes(report)
print(report.decode())
# Saved reference frames are for local inspection only.
times=[1,4.9,7.8,10.5,13,14.4,15.3,16.4,18.6]
sheet=Image.new('RGB',(810,1440))
for i,t in enumerate(times):sheet.paste(frame(t),(i%3*270,i//3*480))
sheet.save(TMP/'contact.png')
