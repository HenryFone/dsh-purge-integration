
import math, os, struct
W,H,FPS,SEC = 960,540,30,4
TOTAL=FPS*SEC
outdir=os.path.join(os.path.dirname(os.path.abspath(__file__)),"frames_ppm")
os.makedirs(outdir,exist_ok=True)

# 5x7 点阵字体(只做需要的字符),用于渲染标题
FONT={
 'C':["01110","10001","10000","10000","10000","10001","01110"],
 'O':["01110","10001","10001","10001","10001","10001","01110"],
 'D':["11110","10001","10001","10001","10001","10001","11110"],
 'E':["11111","10000","10000","11110","10000","10000","11111"],
 'V':["10001","10001","10001","10001","10001","01010","00100"],
 'I':["11111","00100","00100","00100","00100","00100","11111"],
 '>':["10000","01000","00100","00010","00100","01000","10000"],
 ' ':["00000","00000","00000","00000","00000","00000","00000"],
 'P':["11110","10001","10001","11110","10000","10000","10000"],
 'U':["10001","10001","10001","10001","10001","10001","01110"],
 'R':["11110","10001","10001","11110","10100","10010","10001"],
 'N':["10001","11001","10101","10011","10001","10001","10001"],
 'T':["11111","00100","00100","00100","00100","00100","00100"],
 'F':["11111","10000","10000","11110","10000","10000","10000"],
 'M':["10001","11011","10101","10101","10001","10001","10001"],
 'G':["01110","10001","10000","10111","10001","10001","01110"],
}
def clamp01(x): return max(0.0,min(1.0,x))
def ease(t): return 1-(1-t)**3

def draw_text(buf,text,cx,cy,scale,rgb,alpha):
    tw=len(text)*6*scale
    x0=cx-tw//2
    for ci,ch in enumerate(text):
        g=FONT.get(ch,FONT[' '])
        for ry in range(7):
            for rx in range(5):
                if g[ry][rx]=='1':
                    for sy in range(scale):
                        for sx in range(scale):
                            px=x0+ci*6*scale+rx*scale+sx
                            py=cy+ry*scale+sy
                            if 0<=px<W and 0<=py<H:
                                idx=(py*W+px)*3
                                for k in range(3):
                                    buf[idx+k]=int(buf[idx+k]*(1-alpha)+rgb[k]*alpha)

for i in range(TOTAL):
    t=i/TOTAL; ts=t*SEC
    buf=bytearray(W*H*3)
    # 渐变背景
    for y in range(H):
        base=y/H
        hue=0.6+0.08*math.sin(t*2*math.pi)
        r=int(30+40*base+30*math.sin(t*2*math.pi))
        g=int(30+50*base)
        b=int(70+80*(1-base)+30*math.cos(t*2*math.pi))
        row=(y*W)*3
        for x in range(W):
            idx=row+x*3
            buf[idx]=max(0,min(255,r)); buf[idx+1]=max(0,min(255,g)); buf[idx+2]=max(0,min(255,b))
    # 标题淡入
    tp=ease(clamp01((ts-0.3)/1.0))
    draw_text(buf,"CODE > VIDEO", W//2, 180-int((1-tp)*30), 8, (255,255,255), tp)
    # 副标题
    sp=ease(clamp01((ts-1.2)/1.0))
    draw_text(buf,"PURE CODE NO EDITOR", W//2, 300-int((1-sp)*20), 3, (168,199,255), sp)
    draw_text(buf,"RENDERED BY FFMPEG", W//2, 330-int((1-sp)*20), 3, (168,199,255), sp)
    # 进度条
    bp=clamp01((ts-1.8)/1.6); bw=int(500*ease(bp))
    by=400; bx=(W-500)//2
    for yy in range(by,by+8):
        for xx in range(bx,bx+500):
            idx=(yy*W+xx)*3; buf[idx]=60;buf[idx+1]=70;buf[idx+2]=90
        for xx in range(bx,bx+bw):
            idx=(yy*W+xx)*3; buf[idx]=79;buf[idx+1]=157;buf[idx+2]=255
    with open(os.path.join(outdir,f"f{i:04d}.ppm"),"wb") as f:
        f.write(b"P6\n%d %d\n255\n"%(W,H)); f.write(bytes(buf))
print("frames:",TOTAL,"->",outdir)
