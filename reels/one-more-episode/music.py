import numpy as np, wave
sr=44100; bpm=112; beat=60/bpm; dur=62
t_all=np.zeros(int(sr*dur))
def pluck(f,l=0.35,a=0.25):
    n=int(sr*l); t=np.arange(n)/sr
    return a*np.exp(-t*9)*(np.sin(2*np.pi*f*t)+0.3*np.sin(4*np.pi*f*t)+0.1*np.sin(6*np.pi*f*t))
N=lambda m:440*2**((m-69)/12)
# sneaky minor-ish walk: C, Eb, G, F#... playful
mel=[60,63,67,66,67,63,60,None, 58,62,65,64,65,62,58,None, 60,63,67,70,68,67,63,None, 67,66,65,63,62,63,60,None]
bass=[36,36,43,43,34,34,41,41]
i=0;t=0.0
while t<dur-1:
    m=mel[i%len(mel)]
    if m:
        s=pluck(N(m),0.3,0.18); k=int(t*sr); t_all[k:k+len(s)]+=s[:len(t_all)-k]
    if i%2==0:
        b=bass[(i//4)%len(bass)]; s=pluck(N(b),0.45,0.28); k=int(t*sr); t_all[k:k+len(s)]+=s[:len(t_all)-k]
    t+=beat/2; i+=1
t_all/=np.abs(t_all).max()*1.1
with wave.open("audio/music.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((t_all*32767).astype(np.int16).tobytes())
