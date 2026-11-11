import sys, os, zlib, struct
def load_png_gray(path):
    d=open(path,'rb').read(); assert d[:8]==b'\x89PNG\r\n\x1a\n'
    i=8; idat=b''
    while i<len(d):
        n,=struct.unpack('>I',d[i:i+4]); t=d[i+4:i+8]; c=d[i+8:i+8+n]; i+=12+n
        if t==b'IHDR': W,H,bd,ct,_,_,il=struct.unpack('>IIBBBBB',c)
        elif t==b'IDAT': idat+=c
    assert bd==8 and il==0, (bd,il)
    ch={0:1,2:3,4:2,6:4}[ct]
    raw=zlib.decompress(idat); stride=W*ch
    prev=bytearray(stride); rows=[]; p=0
    for y in range(H):
        f=raw[p]; line=bytearray(raw[p+1:p+1+stride]); p+=1+stride
        if f==1:
            for x in range(ch,stride): line[x]=(line[x]+line[x-ch])&255
        elif f==2:
            for x in range(stride): line[x]=(line[x]+prev[x])&255
        elif f==3:
            for x in range(stride): line[x]=(line[x]+((line[x-ch] if x>=ch else 0)+prev[x])//2)&255
        elif f==4:
            for x in range(stride):
                a=line[x-ch] if x>=ch else 0; b=prev[x]; c=prev[x-ch] if x>=ch else 0
                pa=abs(b-c); pb=abs(a-c); pc=abs(a+b-2*c)
                pr=a if pa<=pb and pa<=pc else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        rows.append(line); prev=line
    def gray(line,x):
        if ch<3: return line[x*ch]
        o=x*ch; return (299*line[o]+587*line[o+1]+114*line[o+2])//1000
    MASK=os.environ.get("MASK","red")
    def fg(line,x):
        o=x*ch
        if MASK=="red": return line[o]-line[o+2] > 18
        if MASK.startswith("bright:"): return gray(line,x) > int(MASK[7:])
        return True
    return W,H,rows,gray,fg
src,cols=sys.argv[1],int(sys.argv[2]); x0,y0,x1,y1=map(int,sys.argv[3].split(',')); ratio=float(sys.argv[4])
W,H,rows,gray,fg=load_png_gray(src)
cw=(x1-x0)/cols; rh=cw*ratio; nrows=int((y1-y0)/rh)
grid=[]
for r in range(nrows):
    row=[]
    for c in range(cols):
        s=n=f=0
        for yy in range(int(y0+r*rh),int(y0+(r+1)*rh),3):
            line=rows[yy]
            for xx in range(int(x0+c*cw),int(x0+(c+1)*cw),3):
                s+=gray(line,xx); n+=1; f+=fg(line,xx)
        row.append(s/n if f/n>0.45 else -1)
    grid.append(row)
sharp=float(sys.argv[6]) if len(sys.argv)>6 else 1.0
R,C=len(grid),len(grid[0])
def nb(r,c):
    vs=[grid[rr][cc] for rr in range(r-1,r+2) for cc in range(c-1,c+2) if 0<=rr<R and 0<=cc<C and grid[rr][cc]>=0]
    return sum(vs)/len(vs)
grid=[[(-1 if grid[r][c]<0 else grid[r][c]+sharp*(grid[r][c]-nb(r,c))) for c in range(C)] for r in range(R)]
vals=sorted(v for r in grid for v in r if v>=0)
import bisect
def eq(v): return bisect.bisect_left(vals,v)/len(vals)
lo,hi=0.0,1.0
gamma=float(sys.argv[5]) if len(sys.argv)>5 else 1.0
MODE=os.environ.get("MODE","eq")
if MODE=="eq": grid=[[(-1 if v<0 else eq(v)) for v in row] for row in grid]
elif MODE=="linear": grid=[[(-1 if v<0 else max(0,min(1,v/255))) for v in row] for row in grid]
elif MODE=="lines": grid=[[(-1 if v<0 else max(0,min(1,(255-v)/255))) for v in row] for row in grid]
ramp=" .:-=+*#%@"
for row in grid:
    print("".join((' ' if v<0 else ramp[min(9,max(0,int(((min(max((v-lo)/(hi-lo),0),1))**gamma)*10)))]) for v in row).rstrip())
