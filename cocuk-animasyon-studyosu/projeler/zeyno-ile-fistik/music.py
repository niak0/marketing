# Kodla üretilen neşeli melodi (C majör, 112 BPM). Kullanım: python3 music.py cikti.wav [sure_sn]
import numpy as np, wave, sys
sr=44100; D=float(sys.argv[2]) if len(sys.argv)>2 else 34; bpm=112; beat=60/bpm
t=np.arange(int(sr*D))/sr; out=np.zeros_like(t)
def note(f,start,dur,amp=.2,kind='bell'):
    i0=int(start*sr); n=int(dur*sr); 
    if i0>=len(out): return
    n=min(n,len(out)-i0); tt=np.arange(n)/sr
    env=np.exp(-tt*(3 if kind=='bell' else 1.5))*np.minimum(1,tt*200)
    w=np.sin(2*np.pi*f*tt)+.3*np.sin(4*np.pi*f*tt)+.1*np.sin(6*np.pi*f*tt) if kind=='bell' else np.sin(2*np.pi*f*tt)
    out[i0:i0+n]+=amp*env*w
m=lambda k:440*2**((k-69)/12)
mel=[72,76,79,76, 77,81,79,0, 76,79,84,79, 77,76,74,0, 72,74,76,79, 81,79,76,74, 72,76,74,71, 72,0,0,0]
chords=[[48,55,64],[53,60,69],[48,55,64],[55,62,71],[48,55,64],[53,60,69],[55,62,71],[48,55,64]]
bar=4*beat; i=0; s=0
while s<D:
    for k,nn in enumerate(mel):
        st=s+k*beat/2
        if nn: note(m(nn),st,beat*1.2,.16)
    for c,ch in enumerate(chords):
        st=s+c*bar/2
        note(m(ch[0]-12),st,bar/2,.22,'soft'); note(m(ch[1]),st,bar/2,.05,'soft'); note(m(ch[2]),st+beat,bar/2,.05,'soft')
    s+=len(mel)*beat/2
fade=np.minimum(1,(D-t)/2.5); out*=np.clip(fade,0,1)*np.minimum(1,t/0.5)
out=out/np.abs(out).max()*.7
w=wave.open(sys.argv[1] if len(sys.argv)>1 else 'music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
