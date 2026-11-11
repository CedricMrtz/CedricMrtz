import sys
from xml.sax.saxutils import escape
import os
HERE=os.path.dirname(os.path.abspath(__file__))
art=open(os.path.join(HERE,"art.txt")).read().rstrip("\n").split("\n")
out=os.path.dirname(HERE)
themes={
 "dark": dict(bg="#0d1117",border="#30363d",art="#58a6ff",key="#ffa657",dim="#484f58",val="#c9d1d9",head="#58a6ff",
              pal=["#484f58","#f85149","#3fb950","#d29922","#58a6ff","#bc8cff","#39c5cf","#c9d1d9"]),
 "light":dict(bg="#ffffff",border="#d0d7de",art="#0969da",key="#bc4c00",dim="#afb8c1",val="#24292f",head="#0969da",
              pal=["#24292f","#cf222e","#1a7f37","#9a6700","#0969da","#8250df","#1b7c83","#6e7781"]),
}
COL=18      # value column (chars from label start)
WIDTH=55    # total width of info lines (chars)
info=[
 ("header","cedric@github"),
 ("kv","OS","NixOS, macOS"),
 ("kv","Shell","zsh"),
 ("kv","Host","Full-stack developer"),
 ("kv","Kernel","Systems programmer (in progress)"),
 ("kv","Uptime","Always trying new things"),
 ("kv","Languages.Code","TypeScript, Rust, C++, Python, Java"),
 ("kv","Languages.Real","Spanish, English"),
 ("kv","Frameworks","React, Next.js, Node.js, Tailwind"),
 ("kv","Systems","ROS2, Docker, Linux, PostgreSQL, Git"),
 ("gap",),
 ("section","Fun Facts"),
 ("kv","Now Playing","Baldur's Gate 3"),
 ("kv","Underwater","Writing ROS2 code for SeaFox Inventive"),
 ("gap",),
 ("section","Contact"),
 ("kv","Email","cedric.santi@gmail.com"),
 ("kv","Personal Page","cedricmartinezcv.vercel.app"),
 ("kv","LinkedIn","in/cedric-martinez-zavala-a40436294"),
 ("gap",),
 ("palette",),
]
LH=21; X=400; Y0=48
W=920
H=Y0+LH*(len(info)-1)+40
for name,t in themes.items():
    L=[]
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Consolas, \'DejaVu Sans Mono\', Menlo, monospace" font-size="14px">')
    L.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>')
    ART_FS=7.2; ART_LH=8
    ay=int((H-len(art)*ART_LH)//2+ART_LH)
    for i,line in enumerate(art):
        L.append(f'<text x="30" y="{ay+i*ART_LH}" font-size="{ART_FS}px" fill="{t["art"]}" xml:space="preserve">{escape(line)}</text>')
    y=Y0
    for row in info:
        k=row[0]
        if k=="header":
            u,h=row[1].split("@")
            L.append(f'<text x="{X}" y="{y}" xml:space="preserve"><tspan fill="{t["key"]}">{u}</tspan><tspan fill="{t["val"]}">@</tspan><tspan fill="{t["head"]}">{h}</tspan><tspan fill="{t["dim"]}"> {"─"*(WIDTH-len(row[1])-1)}</tspan></text>')
        elif k=="section":
            L.append(f'<text x="{X}" y="{y}" xml:space="preserve"><tspan fill="{t["dim"]}">─ </tspan><tspan fill="{t["head"]}">{row[1]}</tspan><tspan fill="{t["dim"]}"> {"─"*(WIDTH-len(row[1])-3)}</tspan></text>')
        elif k=="kv":
            lab,val=row[1],row[2]
            dots="."*(COL-len(lab)-2)
            L.append(f'<text x="{X}" y="{y}" xml:space="preserve"><tspan fill="{t["key"]}">{escape(lab)}:</tspan><tspan fill="{t["dim"]}">{dots} </tspan><tspan fill="{t["val"]}">{escape(val)}</tspan></text>')
        elif k=="palette":
            for j,c in enumerate(t["pal"]):
                L.append(f'<rect x="{X+j*30}" y="{y-13}" width="30" height="16" fill="{c}"/>')
        y+=LH
    L.append('</svg>')
    open(f"{out}/{name}_mode.svg","w").write("\n".join(L)+"\n")
print(H)
