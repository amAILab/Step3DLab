from pathlib import Path
import math

OUT=Path(__file__).parent

def tri(f, a,b,c):
    def normal(a,b,c):
        ux,uy,uz=b[0]-a[0],b[1]-a[1],b[2]-a[2]
        vx,vy,vz=c[0]-a[0],c[1]-a[1],c[2]-a[2]
        nx,ny,nz=uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        l=math.sqrt(nx*nx+ny*ny+nz*nz) or 1
        return nx/l,ny/l,nz/l
    n=normal(a,b,c)
    f.write(f"  facet normal {n[0]:.6g} {n[1]:.6g} {n[2]:.6g}\n    outer loop\n")
    for p in (a,b,c): f.write(f"      vertex {p[0]:.6g} {p[1]:.6g} {p[2]:.6g}\n")
    f.write("    endloop\n  endfacet\n")

def inside_hole(x,y,holes,r):
    return any((x-hx)**2+(y-hy)**2 < r*r for hx,hy in holes)

def make(name, width, height, holes, hole_r=27.5, thick=5.0, grid=2.0):
    path=OUT/name
    xmin,xmax=-width/2,width/2; ymin,ymax=-height/2,height/2
    nx=math.ceil(width/grid); ny=math.ceil(height/grid)
    dx=width/nx; dy=height/ny
    with path.open('w') as f:
        f.write(f"solid {name}\n")
        # top/bottom surfaces, grid cells outside holes
        for i in range(nx):
            x0=xmin+i*dx; x1=x0+dx
            for j in range(ny):
                y0=ymin+j*dy; y1=y0+dy; cx=(x0+x1)/2; cy=(y0+y1)/2
                if inside_hole(cx,cy,holes,hole_r): continue
                a,b,c,d=(x0,y0,thick),(x1,y0,thick),(x1,y1,thick),(x0,y1,thick)
                tri(f,a,b,c); tri(f,a,c,d)
                a,b,c,d=(x0,y0,0),(x0,y1,0),(x1,y1,0),(x1,y0,0)
                tri(f,a,b,c); tri(f,a,c,d)
        # outer side walls
        corners=[(xmin,ymin),(xmax,ymin),(xmax,ymax),(xmin,ymax)]
        for (x0,y0),(x1,y1) in zip(corners,corners[1:]+corners[:1]):
            tri(f,(x0,y0,0),(x1,y1,0),(x1,y1,thick)); tri(f,(x0,y0,0),(x1,y1,thick),(x0,y0,thick))
        # hole walls
        seg=96
        for hx,hy in holes:
            for k in range(seg):
                a=2*math.pi*k/seg; b=2*math.pi*(k+1)/seg
                p0=(hx+hole_r*math.cos(a),hy+hole_r*math.sin(a),0)
                p1=(hx+hole_r*math.cos(b),hy+hole_r*math.sin(b),0)
                p2=(p1[0],p1[1],thick); p3=(p0[0],p0[1],thick)
                tri(f,p0,p2,p1); tri(f,p0,p3,p2)
        # small countersink decorative bevel as raised thin ring around holes
        ring_r1=hole_r+2; ring_r2=hole_r+5; z=thick+0.6
        for hx,hy in holes:
            for k in range(seg):
                a=2*math.pi*k/seg; b=2*math.pi*(k+1)/seg
                p00=(hx+ring_r1*math.cos(a),hy+ring_r1*math.sin(a),thick)
                p01=(hx+ring_r1*math.cos(b),hy+ring_r1*math.sin(b),thick)
                p10=(hx+ring_r2*math.cos(a),hy+ring_r2*math.sin(a),z)
                p11=(hx+ring_r2*math.cos(b),hy+ring_r2*math.sin(b),z)
                if not inside_hole(*((p10[0]+p11[0])/2,(p10[1]+p11[1])/2), holes, hole_r):
                    tri(f,p00,p01,p11); tri(f,p00,p11,p10)
        f.write(f"endsolid {name}\n")
    return path

def svg(name,width,height,holes,hole_r=27.5):
    p=OUT/name; scale=3; margin=20
    W=width*scale+2*margin; H=height*scale+2*margin
    def X(x): return margin+(x+width/2)*scale
    def Y(y): return margin+(height/2-y)*scale
    with p.open('w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
        f.write('<rect width="100%" height="100%" fill="#f6f4ef"/>')
        f.write(f'<rect x="{margin}" y="{margin}" width="{width*scale}" height="{height*scale}" rx="24" fill="#eaf8f0" stroke="#0d2a20" stroke-width="3"/>')
        for hx,hy in holes:
            f.write(f'<circle cx="{X(hx)}" cy="{Y(hy)}" r="{hole_r*scale}" fill="#fff" stroke="#23b86a" stroke-width="3"/>')
            f.write(f'<circle cx="{X(hx)}" cy="{Y(hy)}" r="{(hole_r+5)*scale}" fill="none" stroke="#23b86a" stroke-width="1.5" opacity=".55"/>')
        f.write(f'<text x="{margin}" y="{H-6}" font-family="Arial" font-size="14" fill="#0d2a20">{width:.0f}×{height:.0f} мм · отверстие Ø{hole_r*2:.0f} мм · толщина 5 мм</text>')
        f.write('</svg>')

make('rozetka_odinary_single_80x80.stl',80,80,[(0,0)])
svg('rozetka_odinary_single_80x80_preview.svg',80,80,[(0,0)])
make('rozetka_triple_222x80.stl',222,80,[(-71,0),(0,0),(71,0)])
svg('rozetka_triple_222x80_preview.svg',222,80,[(-71,0),(0,0),(71,0)])
print('OK', OUT)
