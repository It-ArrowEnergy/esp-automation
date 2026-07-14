import sys
import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.config import Configuration, HatchPolicy
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# usage: render_view.py <dxf> <out.png> <xmin> <xmax> <ymin> <ymax> [dpi]
dxf, out = sys.argv[1], sys.argv[2]
xmin, xmax, ymin, ymax = map(float, sys.argv[3:7])
dpi = int(sys.argv[7]) if len(sys.argv) > 7 else 100

doc, _ = recover.readfile(dxf)
msp = doc.modelspace()
fig = plt.figure(figsize=(18, 12), dpi=dpi)
ax = fig.add_axes([0.04, 0.04, 0.94, 0.94])
ax.set_facecolor("white")
cfg = Configuration(hatch_policy=HatchPolicy.SHOW_OUTLINE)
Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(msp, finalize=False)
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")
ax.axis("on")
ax.grid(True, alpha=0.3)
fig.savefig(out, dpi=dpi, facecolor="white")
print("saved", out)
