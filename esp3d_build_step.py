"""Arrow Energy 4-cell ESP -> TRUE SOLIDS STEP with colors + traced logo.
Usage: python3 esp3d_build_step.py  (needs cadquery; logo_polys.json beside this file)
Output: ESP_4CELL.step in current directory. See ESP_MASTER_GUIDE.md for parameters."""
import numpy as np, json, os, cadquery as cq
HERE=os.path.dirname(os.path.abspath(__file__))
Lc,Wc=16205.0,7705.0; Z0,Z1=9350.0,21115.0; ZD=Z1+130.0; FP=Lc/4; zc=(Z0+Z1)/2
COL={"CASING":(185,136,115),"SEAM":(164,120,95),"BAND":(156,111,87),"GIRDER":(143,98,72),
"HOPPER":(185,136,115),"FUNNEL":(171,133,112),"CHUTE":(160,106,78),"SUPPORT":(61,110,216),
"DECK":(47,87,196),"GRATE":(216,221,226),"RAIL":(242,200,30),"TREAD":(207,212,217),
"TRSET":(242,239,233),"MIGI":(242,106,26),"MIGIBASE":(236,239,242),"EROD":(58,58,58),
"RAV":(210,84,42),"NOZZLE":(171,133,112),"PANEL":(136,152,168),"LOGO":(240,74,16)}
parts={k:[] for k in COL}
def BOX(x0,y0,z0,x1,y1,z1,lay):
    dx,dy,dz=abs(x1-x0),abs(y1-y0),abs(z1-z0)
    if dx<1 or dy<1 or dz<1: return
    parts[lay].append(cq.Workplane("XY",origin=(min(x0,x1),min(y0,y1),min(z0,z1))).box(dx,dy,dz,centered=False).val())
def CYL(cx,cy,z0,z1,r,lay):
    parts[lay].append(cq.Workplane("XY",origin=(cx,cy,min(z0,z1))).circle(r).extrude(abs(z1-z0)).val())
def DBOX(a,b,n,width,thick,lay):
    a=np.array(a,float); b=np.array(b,float); n=np.array(n,float)
    d=b-a; Lm=np.linalg.norm(d); d/=Lm
    pl=cq.Plane(origin=tuple(a),xDir=tuple(d),normal=tuple(n))
    parts[lay].append(cq.Workplane(pl).box(Lm,width,thick,centered=(False,True,True)).val())
data=json.load(open(os.path.join(HERE,"logo_polys.json")))
H_img=484.0; S=3300.0/H_img
def mk_logo():
    sol=[]; allp=[]
    for it in data:
        for x,y in it["shell"]: allp.append((x*S,(H_img-y)*S))
    ap=np.array(allp); c=(ap.min(0)+ap.max(0))/2
    for it in data:
        sh=[(x*S-c[0],(H_img-y)*S-c[1]) for x,y in it["shell"]]
        outer=cq.Wire.makePolygon([cq.Vector(x,y,0) for x,y in sh],close=True)
        holes=[cq.Wire.makePolygon([cq.Vector(x*S-c[0],(H_img-y)*S-c[1],0) for x,y in h],close=True) for h in it["holes"]]
        sol.append(cq.Solid.extrudeLinear(cq.Face.makeFromWires(outer,holes),cq.Vector(0,0,55)))
    return sol
def place_logo(rotz,tx,ty,tz):
    for s in mk_logo():
        s2=s.rotate(cq.Vector(0,0,0),cq.Vector(1,0,0),90)
        if rotz: s2=s2.rotate(cq.Vector(0,0,0),cq.Vector(0,0,1),rotz)
        parts["LOGO"].append(s2.translate(cq.Vector(tx,ty,tz)))
place_logo(0,Lc-2900,-2,Z1-2300); place_logo(90,Lc+57,Wc/2,Z1-2300)
ZH=1700.0
for i in range(4):
    cx=FP/2+i*FP
    parts["HOPPER"].append((cq.Workplane("XY",origin=(cx,Wc/2,ZH)).rect(600,600)
       .workplane(offset=Z0-ZH).rect(FP*0.94,Wc*0.94).loft()).val())
for xf,xn in ((0,-5200.0),(Lc,5200.0)):
    parts["FUNNEL"].append((cq.Workplane("YZ",origin=(xf,Wc/2,zc)).rect(Wc,Z1-200-(Z0+300))
       .workplane(offset=xn).rect(1900,1900).loft()).val())
BOX(0,0,Z0,Lc,Wc,Z1,"CASING"); BOX(-50,-50,Z1,Lc+50,Wc+50,ZD,"CASING")
BOX(-140,-140,Z1-420,Lc+140,Wc+140,Z1,"GIRDER"); BOX(-150,-150,Z0-80,Lc+150,Wc+150,Z0+560,"GIRDER")
for i in range(5):
    x=i*FP
    BOX(x-110,-95,Z0+560,x+110,0,Z1-420,"GIRDER"); BOX(x-110,Wc,Z0+560,x+110,Wc+95,Z1-420,"GIRDER")
for x in np.arange(675,Lc,675):
    if min(abs(x-i*FP) for i in range(5))<200: continue
    BOX(x-22,-28,Z0+560,x+22,0,Z1-420,"SEAM"); BOX(x-22,Wc,Z0+560,x+22,Wc+28,Z1-420,"SEAM")
for y in np.arange(700,Wc,700):
    BOX(-28,y-22,Z0+560,0,y+22,Z1-420,"SEAM"); BOX(Lc,y-22,Z0+560,Lc+28,y+22,Z1-420,"SEAM")
for z in (Z0+3000,Z0+5900,Z0+8800):
    BOX(-60,-60,z-110,Lc+60,0,z+110,"BAND"); BOX(-60,Wc,z-110,Lc+60,Wc+60,z+110,"BAND")
    BOX(-60,0,z-110,0,Wc,z+110,"BAND"); BOX(Lc,0,z-110,Lc+60,Wc,z+110,"BAND")
for i in range(4):
    cx=FP/2+i*FP
    BOX(cx-250,Wc/2-250,900,cx+250,Wc/2+250,ZH,"CHUTE"); BOX(cx-320,Wc/2-320,520,cx+320,Wc/2+320,900,"RAV")
BOX(-5360,Wc/2-1070,zc-1070,-5200,Wc/2+1070,zc+1070,"NOZZLE")
BOX(Lc+5200,Wc/2-1070,zc-1070,Lc+5360,Wc/2+1070,zc+1070,"NOZZLE")
CS=360.0; cols_x=[i*FP for i in range(5)]; cols_y=[80.0,Wc-440.0]; ZB1,ZB2=3400.0,6500.0
for x in cols_x:
    for y in cols_y:
        BOX(x-CS/2,y,0,x+CS/2,y+CS,Z0-80,"SUPPORT"); BOX(x-540,y-230,0,x+540,y+CS+230,130,"SUPPORT")
for zl in (ZB1,ZB2,Z0-80):
    for i in range(4):
        for y in cols_y: BOX(cols_x[i],y+70,zl-240,cols_x[i+1],y+CS-70,zl,"SUPPORT")
    for x in cols_x: BOX(x-CS/2+70,cols_y[0]+CS,zl-240,x+CS/2-70,cols_y[1],zl,"SUPPORT")
for i in range(4):
    for y in (cols_y[0]+CS/2,cols_y[1]+CS/2):
        for za,zb in ((130,ZB1-240),(ZB1,ZB2-240),(ZB2,Z0-320)):
            DBOX((cols_x[i]+CS/2,y,za),(cols_x[i+1]-CS/2,y,zb),(0,1,0),130,80,"SUPPORT")
            DBOX((cols_x[i+1]-CS/2,y,za),(cols_x[i]+CS/2,y,zb),(0,1,0),130,80,"SUPPORT")
for x in cols_x:
    for za,zb in ((130,ZB1-240),(ZB1,ZB2-240),(ZB2,Z0-320)):
        DBOX((x,cols_y[0]+CS,za),(x,cols_y[1],zb),(1,0,0),130,80,"SUPPORT")
        DBOX((x,cols_y[1],za),(x,cols_y[0]+CS,zb),(1,0,0),130,80,"SUPPORT")
def RAILING(path,h=1050.0,step=1300.0):
    for a,b in zip(path[:-1],path[1:]):
        a=np.array(a,float); b=np.array(b,float); d=b-a; ln=np.linalg.norm(d)
        for zh in (h,h*0.55):
            BOX(min(a[0],b[0])-28,min(a[1],b[1])-28,a[2]+zh-32,max(a[0],b[0])+28,max(a[1],b[1])+28,a[2]+zh+32,"RAIL")
        BOX(min(a[0],b[0])-18,min(a[1],b[1])-18,a[2],max(a[0],b[0])+18,max(a[1],b[1])+18,a[2]+105,"RAIL")
        for t in np.linspace(0,1,max(2,int(ln//step))):
            p=a+d*t; BOX(p[0]-30,p[1]-30,a[2],p[0]+30,p[1]+30,a[2]+h,"RAIL")
BOX(250,cols_y[0]+CS,ZB1-60,Lc-250,cols_y[1],ZB1,"GRATE")
RAILING([(250,cols_y[0]+CS,ZB1),(Lc-250,cols_y[0]+CS,ZB1),(Lc-250,cols_y[1],ZB1),(250,cols_y[1],ZB1),(250,cols_y[0]+CS,ZB1)])
RAILING([(60,60,ZD),(Lc-60,60,ZD),(Lc-60,Wc-60,ZD),(60,Wc-60,ZD),(60,60,ZD)])
for bx in (Lc*0.22,Lc*0.47,Lc*0.72):
    BOX(bx,-1500,Z1-90,bx+2000,60,ZD,"DECK")
    RAILING([(bx,-1450,ZD),(bx,-60,ZD)],h=980,step=700)
    RAILING([(bx+2000,-1450,ZD),(bx+2000,-60,ZD)],h=980,step=700)
    RAILING([(bx,-1450,ZD),(bx+2000,-1450,ZD)],h=980,step=900)
def RAPPER(cx,cy,l="MIGI",h=850.0,r=70.0):
    BOX(cx-135,cy-135,ZD,cx+135,cy+135,ZD+40,"MIGIBASE")
    BOX(cx-32,cy-32,ZD+40,cx+32,cy+32,ZD+210,"MIGIBASE")
    CYL(cx,cy,ZD+210,ZD+210+h,r,l)
for i in range(4):
    fx=i*FP
    for xo in np.linspace(fx+FP*0.13,fx+FP*0.87,5):
        RAPPER(xo,Wc*0.22); RAPPER(xo,Wc*0.44)
    for xo in np.linspace(fx+FP*0.2,fx+FP*0.8,3):
        RAPPER(xo,Wc*0.64,l="EROD",h=950.0,r=60.0)
for i in range(4):
    cx=FP/2+i*FP
    BOX(cx-1000,Wc-2000,ZD+60,cx+1000,Wc-600,ZD+1150,"TRSET")
    BOX(cx-880,Wc-2060,ZD+1150,cx+880,Wc-540,ZD+1320,"TRSET")
    BOX(cx-1000,Wc-2000,ZD,cx+1000,Wc-600,ZD+60,"DECK")
    for k in range(6):
        BOX(cx+1000,Wc-1950+k*230,ZD+180,cx+1140,Wc-1850+k*230,ZD+1050,"TRSET")
    parts["TRSET"].append(cq.Workplane("ZX",origin=(cx,Wc-2000,ZD+780)).circle(430).extrude(-900).val())
    CYL(cx,Wc-2900,ZD,ZD+780,430,"TRSET")
    BOX(cx-140,Wc-820,ZD+1320,cx+140,Wc-580,ZD+1750,"EROD")
    BOX(cx-640,Wc-820,ZD+1320,cx-360,Wc-580,ZD+1700,"EROD")
BOX(Lc*0.05,Wc*0.5,ZD,Lc*0.05+1100,Wc*0.5+800,ZD+1150,"PANEL")
BOX(Lc*0.93,Wc*0.70,ZD,Lc*0.93+900,Wc*0.70+700,ZD+800,"TRSET")
SW=1150.0; YF=-1500.0
def FLIGHT(x0,z0,x1,z1):
    n=max(5,int(abs(z1-z0)//235)); ts=np.linspace(0,1,n)
    for t0,t1 in zip(ts[:-1],ts[1:]):
        xa=x0+(x1-x0)*t0; za=z0+(z1-z0)*t0; xb=x0+(x1-x0)*t1
        BOX(xa,YF,za-20,xb,YF+SW,za+20,"TREAD")
    for yy in (YF-50,YF+SW):
        DBOX((x0,yy+25,z0-90),(x1,yy+25,z1-90),(0,1,0),180,60,"SUPPORT")
    for yy in (YF,YF+SW):
        for zh in (1000.0,540.0):
            DBOX((x0,yy,z0+zh),(x1,yy,z1+zh),(0,1,0),60,56,"RAIL")
        for t in np.linspace(0,1,7):
            px=x0+(x1-x0)*t; pz=z0+(z1-z0)*t
            BOX(px-28,yy-28,pz,px+28,yy+28,pz+1000,"RAIL")
def LANDING(x0,x1,z,end_rail=True):
    BOX(x0,YF-60,z-200,x1,YF+SW+60,z-40,"DECK")
    BOX(x0,YF-60,z-40,x1,YF+SW+60,z-20,"GRATE")
    RAILING([(x0,YF,z-20),(x1,YF,z-20)],h=1000,step=700)
    if end_rail:
        xe=x0 if x1>x0 else x1
        RAILING([(xe,YF,z-20),(xe,YF+SW,z-20)],h=1000,step=500)
    for xx in (x0+220,x1-220):
        BOX(xx-70,YF+SW/2-70,max(z-3400,130),xx+70,YF+SW/2+70,z-40,"SUPPORT")
        if z>=Z0:
            DBOX((xx,YF+SW,z-120),(xx,0,z-120),(1,0,0),120,70,"SUPPORT")
            DBOX((xx,YF+SW/2,z-160),(xx,0,z+750),(1,0,0),110,70,"SUPPORT")
zlv=[500.0,ZB1,ZB2,Z0,Z0+2941,Z0+5882,Z0+8823,ZD]
xa,xb=Lc*0.30,Lc*0.60
for k in range(len(zlv)-1):
    if k%2==0:
        FLIGHT(xa,zlv[k],xb,zlv[k+1]); LANDING(xb,xb+1600,zlv[k+1])
    else:
        FLIGHT(xb,zlv[k],xa,zlv[k+1]); LANDING(xa-1600,xa,zlv[k+1])
FLIGHT(xa-2600,0,xa,500.0); LANDING(xa-2600,xa-1000,500.0,end_rail=False)
BOX(0,YF-60,Z0+360,Lc,YF,Z0+560,"DECK")
BOX(0,YF,Z0+540,Lc,0,Z0+560,"GRATE")
RAILING([(0,YF,Z0+560),(Lc,YF,Z0+560)],h=1000,step=1100)
for xx in np.linspace(600,Lc-600,9):
    DBOX((xx,YF+SW/2,Z0+360),(xx,0,Z0-500),(1,0,0),120,70,"SUPPORT")
print("solids:",sum(len(v) for v in parts.values()))
assy=cq.Assembly()
for lay,shapes in parts.items():
    if not shapes: continue
    r,g,b=COL[lay]
    assy.add(cq.Compound.makeCompound(shapes),name=lay,color=cq.Color(r/255,g/255,b/255))
assy.save("ESP_4CELL.step")
print("ESP_4CELL.step saved")
