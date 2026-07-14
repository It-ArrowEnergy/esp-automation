"""4-cell ESP 3D v4 — fixes: open inlet duct, complete stairs, seated roof equipment,
realistic TR sets with elbow ducts, Arrow Energy logo."""
import numpy as np

QUADS = []
COL = {
    "CASING":"#b98873","SEAM":"#a4785f","BAND":"#9c6f57","GIRDER":"#8f6248",
    "HOPPER":"#b98873","FUNNEL":"#ab8570","CHUTE":"#a06a4e","DARK":"#4a3226",
    "SUPPORT":"#3d6ed8","DECK":"#2f57c4","GRATE":"#d8dde2",
    "RAIL":"#f2c81e","TREAD":"#cfd4d9",
    "TRSET":"#f2efe9","MIGI":"#f26a1b","MIGIBASE":"#eceff2","EROD":"#3a3a3a",
    "RAV":"#d2542a","NOZZLE":"#ab8570","PANEL":"#8898a8","LOGO":"#f04a10",
}
def Q(p1,p2,p3,p4,l): QUADS.append((np.array([p1,p2,p3,p4],float), l))
def box(x0,y0,z0,x1,y1,z1,l):
    if x0>x1: x0,x1=x1,x0
    if y0>y1: y0,y1=y1,y0
    if z0>z1: z0,z1=z1,z0
    Q((x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),l)
    Q((x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1),l)
    Q((x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1),l)
    Q((x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1),l)
    Q((x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1),l)
    Q((x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1),l)
def vcyl(cx,cy,z0,z1,r,l,n=12):
    th=np.linspace(0,2*np.pi,n+1)
    for a,b in zip(th[:-1],th[1:]):
        p=[(cx+r*np.cos(a),cy+r*np.sin(a),z0),(cx+r*np.cos(b),cy+r*np.sin(b),z0),
           (cx+r*np.cos(b),cy+r*np.sin(b),z1),(cx+r*np.cos(a),cy+r*np.sin(a),z1)]
        Q(*p,l)
    top=[(cx+r*np.cos(a),cy+r*np.sin(a),z1) for a in th[:4*(n//4)+1:n//4]]
    Q((cx-r,cy-r,z1),(cx+r,cy-r,z1),(cx+r,cy+r,z1),(cx-r,cy+r,z1),l)
def hcyl_y(cx,y0,y1,cz,r,l,n=12):
    th=np.linspace(0,2*np.pi,n+1)
    for a,b in zip(th[:-1],th[1:]):
        p=[(cx+r*np.cos(a),y0,cz+r*np.sin(a)),(cx+r*np.cos(b),y0,cz+r*np.sin(b)),
           (cx+r*np.cos(b),y1,cz+r*np.sin(b)),(cx+r*np.cos(a),y1,cz+r*np.sin(a))]
        Q(*p,l)

Lc,Wc = 16205.0, 7705.0
Z0,Z1 = 9350.0, 21115.0
ZD = Z1+130.0                     # roof deck level
FP = Lc/4

# ============ CASING + ROOF DECK ============
box(0,0,Z0,Lc,Wc,Z1,"CASING")
box(-50,-50,Z1,Lc+50,Wc+50,ZD,"CASING")                      # roof deck slab
box(-140,-140,Z1-420,Lc+140,Wc+140,Z1,"GIRDER")               # top edge girder
box(-150,-150,Z0-80,Lc+150,Wc+150,Z0+560,"GIRDER")            # bottom girder
for i in range(5):
    x=i*FP
    box(x-110,-95,Z0+560,x+110,0,Z1-420,"GIRDER")
    box(x-110,Wc,Z0+560,x+110,Wc+95,Z1-420,"GIRDER")
for x in np.arange(675,Lc,675):
    if min(abs(x-i*FP) for i in range(5))<200: continue
    box(x-22,-28,Z0+560,x+22,0,Z1-420,"SEAM")
    box(x-22,Wc,Z0+560,x+22,Wc+28,Z1-420,"SEAM")
for y in np.arange(700,Wc,700):
    box(-28,y-22,Z0+560,0,y+22,Z1-420,"SEAM")
    box(Lc,y-22,Z0+560,Lc+28,y+22,Z1-420,"SEAM")
for z in (Z0+3000,Z0+5900,Z0+8800):
    box(-60,-60,z-110,Lc+60,0,z+110,"BAND")
    box(-60,Wc,z-110,Lc+60,Wc+60,z+110,"BAND")
    box(-60,0,z-110,0,Wc,z+110,"BAND")
    box(Lc,0,z-110,Lc+60,Wc,z+110,"BAND")

# Arrow Energy logo (front face top-right, and outlet end face)
def logo(xc,zc,face="front"):
    s=1400.0
    if face=="front":
        P=lambda dx,dz:( xc+dx,-40,zc+dz)
    else:
        P=lambda dx,dz:( Lc+40, xc+dx, zc+dz)   # xc is y-center on end face
    # 'A' legs
    Q(P(-s*0.45,-s*0.5),P(-s*0.15,-s*0.5),P(s*0.05,s*0.5),P(-s*0.12,s*0.5),"LOGO")
    Q(P(s*0.45,-s*0.5),P(s*0.15,-s*0.5),P(-s*0.05,s*0.5),P(s*0.12,s*0.5),"LOGO")
    Q(P(-s*0.22,-s*0.08),P(s*0.22,-s*0.08),P(s*0.18,s*0.08),P(-s*0.18,s*0.08),"LOGO")
    # text bar
    Q(P(-s*0.55,-s*0.78),P(s*0.55,-s*0.78),P(s*0.55,-s*0.62),P(-s*0.55,-s*0.62),"LOGO")
logo(Lc-2300, Z1-1700, "front")
logo(Wc/2, Z1-1700, "end")

# ============ HOPPERS ============
ZH=1700.0
for i in range(4):
    cx=FP/2+i*FP
    top=[(cx-FP*0.47,Wc*0.03,Z0),(cx+FP*0.47,Wc*0.03,Z0),(cx+FP*0.47,Wc*0.97,Z0),(cx-FP*0.47,Wc*0.97,Z0)]
    bot=[(cx-300,Wc/2-300,ZH),(cx+300,Wc/2-300,ZH),(cx+300,Wc/2+300,ZH),(cx-300,Wc/2+300,ZH)]
    for k in range(4):
        Q(top[k],top[(k+1)%4],bot[(k+1)%4],bot[k],"HOPPER")
    box(cx-250,Wc/2-250,900,cx+250,Wc/2+250,ZH,"CHUTE")
    box(cx-320,Wc/2-320,520,cx+320,Wc/2+320,900,"RAV")

# ============ FUNNELS with open duct ============
def funnel(xf,xn,noz=1900.0):
    zc=(Z0+Z1)/2
    cas=[(xf,0,Z0+300),(xf,Wc,Z0+300),(xf,Wc,Z1-200),(xf,0,Z1-200)]
    nz=[(xn,Wc/2-noz/2,zc-noz/2),(xn,Wc/2+noz/2,zc-noz/2),(xn,Wc/2+noz/2,zc+noz/2),(xn,Wc/2-noz/2,zc+noz/2)]
    for k in range(4):
        Q(cas[k],cas[(k+1)%4],nz[(k+1)%4],nz[k],"FUNNEL")
    for t in (0.22,0.44,0.66,0.88):
        ring=[np.array(cas[k])*(1-t)+np.array(nz[k])*t for k in range(4)]
        for k in range(4):
            a,b=ring[k],ring[(k+1)%4]
            Q(a,b,b+np.array((0,0,110)),a+np.array((0,0,110)),"BAND")
    # flange ring + dark open duct face
    d=-160 if xn<xf else 160
    f=120
    box(xn,Wc/2-noz/2-f,zc-noz/2-f,xn+d,Wc/2+noz/2+f,zc+noz/2+f,"NOZZLE")
    dd = xn+d-10 if xn<xf else xn+d+10
    Q((dd,Wc/2-noz/2+70,zc-noz/2+70),(dd,Wc/2+noz/2-70,zc-noz/2+70),
      (dd,Wc/2+noz/2-70,zc+noz/2-70),(dd,Wc/2-noz/2+70,zc+noz/2-70),"DARK")
funnel(0,-5200); funnel(Lc,Lc+5200)

# ============ SUPPORT STRUCTURE ============
CS=360.0
cols_x=[i*FP for i in range(5)]
cols_y=[80.0,Wc-440.0]
ZB1,ZB2=3400.0,6500.0
for x in cols_x:
    for y in cols_y:
        box(x-CS/2,y,0,x+CS/2,y+CS,Z0-80,"SUPPORT")
        box(x-540,y-230,0,x+540,y+CS+230,130,"SUPPORT")
for zl in (ZB1,ZB2,Z0-80):
    for i in range(4):
        for y in cols_y:
            box(cols_x[i],y+70,zl-240,cols_x[i+1],y+CS-70,zl,"SUPPORT")
    for x in cols_x:
        box(x-CS/2+70,cols_y[0]+CS,zl-240,x+CS/2-70,cols_y[1],zl,"SUPPORT")
BW=130.0
def ribx(a,b,l):  # ribbon in vertical plane
    a,b=np.array(a,float),np.array(b,float)
    off=np.array((0,0,BW/2))
    Q(a-off,b-off,b+off,a+off,l)
for i in range(4):
    for y in (cols_y[0]+CS/2,cols_y[1]+CS/2):
        for za,zb in ((130,ZB1-240),(ZB1,ZB2-240),(ZB2,Z0-320)):
            ribx((cols_x[i]+CS/2,y,za),(cols_x[i+1]-CS/2,y,zb),"SUPPORT")
            ribx((cols_x[i+1]-CS/2,y,za),(cols_x[i]+CS/2,y,zb),"SUPPORT")
for x in cols_x:
    for za,zb in ((130,ZB1-240),(ZB1,ZB2-240),(ZB2,Z0-320)):
        ribx((x,cols_y[0]+CS,za),(x,cols_y[1],zb),"SUPPORT")
        ribx((x,cols_y[1],za),(x,cols_y[0]+CS,zb),"SUPPORT")

def railing(path,h=1050.0,step=1300.0):
    path=[np.array(p,float) for p in path]
    for a,b in zip(path[:-1],path[1:]):
        d=b-a; ln=np.linalg.norm(d)
        for zh in (h,h*0.55):
            box(min(a[0],b[0])-28,min(a[1],b[1])-28,a[2]+zh-32,max(a[0],b[0])+28,max(a[1],b[1])+28,a[2]+zh+32,"RAIL")
        box(min(a[0],b[0])-18,min(a[1],b[1])-18,a[2],max(a[0],b[0])+18,max(a[1],b[1])+18,a[2]+105,"RAIL")
        for t in np.linspace(0,1,max(2,int(ln//step))):
            p=a+d*t
            box(p[0]-30,p[1]-30,a[2],p[0]+30,p[1]+30,a[2]+h,"RAIL")

# mid platform (RAV access)
Q((250,cols_y[0]+CS,ZB1),(Lc-250,cols_y[0]+CS,ZB1),(Lc-250,cols_y[1],ZB1),(250,cols_y[1],ZB1),"GRATE")
railing([(250,cols_y[0]+CS,ZB1),(Lc-250,cols_y[0]+CS,ZB1),(Lc-250,cols_y[1],ZB1),(250,cols_y[1],ZB1),(250,cols_y[0]+CS,ZB1)])

# ============ ROOF EQUIPMENT (seated on deck ZD) ============
railing([(60,60,ZD),(Lc-60,60,ZD),(Lc-60,Wc-60,ZD),(60,Wc-60,ZD),(60,60,ZD)])
for bx in (Lc*0.22,Lc*0.47,Lc*0.72):   # blue balconies
    box(bx,-1500,Z1-90,bx+2000,60,ZD,"DECK")
    railing([(bx,-1450,ZD),(bx,-60,ZD)],h=980,step=700)
    railing([(bx+2000,-1450,ZD),(bx+2000,-60,ZD)],h=980,step=700)
    railing([(bx,-1450,ZD),(bx+2000,-1450,ZD)],h=980,step=900)
def rapper(cx,cy,l="MIGI",h=850.0,r=70.0):
    box(cx-135,cy-135,ZD,cx+135,cy+135,ZD+40,"MIGIBASE")
    box(cx-32,cy-32,ZD+40,cx+32,cy+32,ZD+210,"MIGIBASE")
    vcyl(cx,cy,ZD+210,ZD+210+h,r,l,10)
for i in range(4):
    fx=i*FP
    for xo in np.linspace(fx+FP*0.13,fx+FP*0.87,5):
        rapper(xo,Wc*0.22); rapper(xo,Wc*0.44)
    for xo in np.linspace(fx+FP*0.2,fx+FP*0.8,3):
        rapper(xo,Wc*0.64,l="EROD",h=950.0,r=60.0)
# TR sets — tank + radiator + big elbow duct into roof + bushings
for i in range(4):
    cx=FP/2+i*FP
    box(cx-1000,Wc-2000,ZD+60,cx+1000,Wc-600,ZD+1150,"TRSET")          # tank
    box(cx-880,Wc-2060,ZD+1150,cx+880,Wc-540,ZD+1320,"TRSET")          # rounded top hint
    box(cx-1000,Wc-2000,ZD,cx+1000,Wc-600,ZD+60,"DECK")                # skid
    for k in range(6):                                                  # radiator fins
        box(cx+1000,Wc-1950+k*230,ZD+180,cx+1140,Wc-1850+k*230,ZD+1050,"TRSET")
    hcyl_y(cx,Wc-2900,Wc-2000,ZD+780,430,"TRSET")                       # elbow horizontal
    vcyl(cx,Wc-2900,ZD,ZD+780,430,"TRSET")                              # elbow drop to roof
    box(cx-140,Wc-820,ZD+1320,cx+140,Wc-580,ZD+1750,"EROD")             # bushing
    box(cx-640,Wc-820,ZD+1320,cx-360,Wc-580,ZD+1700,"EROD")
box(Lc*0.05,Wc*0.5,ZD,Lc*0.05+1100,Wc*0.5+800,ZD+1150,"PANEL")
box(Lc*0.93,Wc*0.70,ZD,Lc*0.93+900,Wc*0.70+700,ZD+800,"TRSET")

# ============ STAIR SYSTEM (front face) ============
SW=1150.0; YF=-1500.0
def flight(x0,z0,x1,z1):
    n=max(5,int(abs(z1-z0)//235))
    for t0,t1 in zip(np.linspace(0,1,n)[:-1],np.linspace(0,1,n)[1:]):
        xa,za=x0+(x1-x0)*t0,z0+(z1-z0)*t0
        xb,zb=x0+(x1-x0)*t1,z0+(z1-z0)*t1
        Q((xa,YF,za),(xb,YF,za),(xb,YF+SW,za),(xa,YF+SW,za),"TREAD")
        Q((xb,YF,za),(xb,YF,zb),(xb,YF+SW,zb),(xb,YF+SW,za),"TREAD")
    for yy in (YF-50,YF+SW):
        a=np.array((x0,yy+25,z0)); b=np.array((x1,yy+25,z1))
        Q(a-(0,0,180),b-(0,0,180),b,a,"SUPPORT")
    for yy in (YF,YF+SW):
        a=np.array((x0,yy,z0)); b=np.array((x1,yy,z1))
        for zh in (1000.0,540.0):
            Q(a+(0,0,zh-30),b+(0,0,zh-30),b+(0,0,zh+30),a+(0,0,zh+30),"RAIL")
        for t in np.linspace(0,1,7):
            p=a+(b-a)*t
            box(p[0]-28,yy-28,p[2],p[0]+28,yy+28,p[2]+1000,"RAIL")
def landing(x0,x1,z,end_rail=True):
    box(x0,YF-60,z-200,x1,YF+SW+60,z-40,"DECK")
    Q((x0,YF-60,z-38),(x1,YF-60,z-38),(x1,YF+SW+60,z-38),(x0,YF+SW+60,z-38),"GRATE")
    railing([(x0,YF,z-38),(x1,YF,z-38)],h=1000,step=700)
    if end_rail:
        xe = x0 if x1>x0 else x1
        railing([(xe,YF,z-38),(xe,YF+SW,z-38)],h=1000,step=500)
    # supports: posts + struts
    for xx in (x0+220,x1-220):
        box(xx-70,YF+SW/2-70,max(z-3400,130),xx+70,YF+SW/2+70,z-40,"SUPPORT")
        if z>=Z0:
            a=np.array((xx,YF+SW,z-120)); b=np.array((xx,0,z-120))
            Q(a-(0,0,60),b-(0,0,60),b+(0,0,60),a+(0,0,60),"SUPPORT")
            a=np.array((xx,YF+SW/2,z-160)); b=np.array((xx,0,z+750))
            Q(a-(0,0,55),b-(0,0,55),b+(0,0,55),a+(0,0,55),"SUPPORT")
zlv=[500.0,ZB1,ZB2,Z0,Z0+2941,Z0+5882,Z0+8823,ZD]
xa,xb=Lc*0.30,Lc*0.60
for k in range(len(zlv)-1):
    if k%2==0:
        flight(xa,zlv[k],xb,zlv[k+1]); landing(xb,xb+1600,zlv[k+1])
    else:
        flight(xb,zlv[k],xa,zlv[k+1]); landing(xa-1600,xa,zlv[k+1])
# ground entry flight
flight(xa-2600,0,xa,500.0); landing(xa-2600,xa-1000,500.0,end_rail=False)
# full-length access platform at hopper-top level (like ref 7)
Q((0,YF,Z0+560),(Lc,YF,Z0+560),(Lc,0,Z0+560),(0,0,Z0+560),"GRATE")
box(0,YF-60,Z0+360,Lc,YF,Z0+560,"DECK")
railing([(0,YF,Z0+560),(Lc,YF,Z0+560)],h=1000,step=1100)
for xx in np.linspace(600,Lc-600,9):
    a=np.array((xx,YF+SW/2,Z0+360)); b=np.array((xx,0,Z0-500))
    Q(a-(0,0,60),b-(0,0,60),b+(0,0,60),a+(0,0,60),"SUPPORT")

print("quads:",len(QUADS))
