# ARROW ENERGY — ESP 2D/3D AUTOMATION MASTER GUIDE
**Purpose:** Any AI session (Claude, Opus, etc.) reading this guide + the files in this `AI KIT` folder can regenerate Arrow Energy ESP 2D GA drawings and 3D models with full precision — correct logo, colors, dimensions, workflow — without user guidance.

---

## 1. GOLDEN RULES (user's standing instructions)

1. **PREVIEW FIRST, ALWAYS.** Render a PNG preview of any drawing/model and present it to the user BEFORE delivering or detailing. Never deliver unseen work. Applies to every task.
2. Deliverables go into the connected folder `Claude -gstar` (OneDrive-synced). Present files with clickable cards.
3. User's CAD is **GstarCAD**. Their edition CANNOT create 3D solids (LOFT/solid BOX blocked; BOX runs as mesh-box). It CAN display solids and colors.
4. **DWG files cannot be read** by our tools. Always ask user: open in GstarCAD → `SAVEAS` → *AutoCAD 2010 DXF* into the folder.
5. Verify everything visually: render → Read the PNG → check → iterate. Audit DXFs (`doc.audit()`) before delivery.
6. User communicates by marking up preview images with red/orange circles — read those annotations carefully.

## 2. BRAND STANDARDS

- **Logo**: serif capital "A" with an arrow crossing lower-left → upper-right, arrowhead exiting right, "ARROW ENERGY" serif text below.
  - Source image: `Claude -gstar/logo.png.png` (624×484 px).
  - **Exact traced outline**: `AI KIT/logo_polys.json` — 12 shells + 6 holes, image pixel coords. Scale: `S = target_height_mm / 484.0`, flip Y: `(x*S, (484-y)*S)`. Standard size on ESP casing: 3300 mm tall, extruded 55 mm, color LOGO orange.
  - Reference solid: `AI KIT/logo_traced.stl`.
  - Placement: casing front face near outlet-end top corner + outlet end face, centered ~2300 mm below roof line.
- **Colors** (name: hex RGB / AutoCAD ACI):
  | Part | Hex | ACI |
  |---|---|---|
  | CASING / HOPPER | #b98873 (185,136,115) | 42 |
  | SEAM (panel joints) | #a4785f | 36 |
  | BAND (stiffener bands) | #9c6f57 | 34 |
  | GIRDER (edge girders) | #8f6248 | 32 |
  | FUNNEL / NOZZLE | #ab8570 | 37 |
  | SUPPORT structure | #3d6ed8 (blue) | 5 |
  | DECK (blue platforms) | #2f57c4 | 174 |
  | GRATE (grating) | #d8dde2 | 254 |
  | RAIL (handrails) | #f2c81e (yellow) | 2 |
  | TREAD (stair treads) | #cfd4d9 | 9 |
  | TRSET (transformers) | #f2efe9 (white) | 255 |
  | MIGI rappers | #f26a1b (orange) | 30 |
  | EROD (black rods) | #3a3a3a | 250 |
  | RAV / SPOUT | #d2542a | 30 |
  | LOGO | #f04a10 | 30 |
- **Title block**: `ARROW ENERGY FRAME.dxf` — A2 frame block `AR-A2` (594×420 units at scale 1). Company: ARROW ENERGY CO., LTD. Drawing numbers like `ARE-CLD-GA-001`, `AE-E&I-025-105`.
- Style reference renders: `Claude -gstar/ESP 3D/*.png` (pictures 4, 5, 7, 9-12 show roof equipment, stairs, supports, logo placement).

## 3. REFERENCE FILES IN `Claude -gstar`

| File | Content |
|---|---|
| `CLAUDE REF esp.dxf` | Original 3-field ESP GA (plan/elevation/end view/details/tables) — THE 2D base |
| `ESP 4 CELL GA.dxf` | 4-field version (generated) |
| `ESP 2 CELL GA.dxf` | 2-field × 2-hoppers-per-field version |
| `ESP 2 CHAMBER 2 CELL GA.dxf` | 2 chambers × 2 fields, chambers flush in end view |
| `ESP 4 CELL 3D MODEL COLOR.dxf` | 3D mesh model (3DFACE + true colors) for GstarCAD |
| `ESP 4 CELL 3D MODEL.step` | 3D SOLIDS with colors + traced logo (for Autodesk Viewer / other CAD) |
| `ESP 4 CELL 3D COLOR.glb` | For Windows 3D Viewer / PowerPoint |
| `ESP 3D/Hybrird model.dxf` | User's real model: 1509 ACIS 3DSOLIDs (ESP + 4 cyclones) — readable structurally, NOT tessellatable |
| `ARROW ENERGY FRAME.dxf` | A2 title block frame |

## 4. 2D GA AUTOMATION (field/chamber count changes)

Base: `CLAUDE REF esp.dxf` (AC1024). Key facts:
- Views share X coordinates: PLAN (y≈33000–52500) and ELEVATION (y≈-3500–31000) — ONE x-operation edits both. END VIEW x≈22700–38600. Tables/details x>40000: never touch.
- Support grid bubbles A,B,C,D at x = -519, 3948, 7965, 11948 (y≈1100).
- **Field module**: C-band x∈[7930,8080], D-band x∈[11930,12080], pitch **P = 4005 mm**.
- TR sets (TRP-T plan / TRE-T elev inserts) at x = 3316, 7316, 10414.
- Plan chamber: y 38891.3–46596.3 (width 7705), chamber CL y=42743.8.

**Add a field (3→4)**: classify entities (region x<22600): keep if max_x≤7930; translate +P if min_x≥8080; pure C-band [7930,8080] → keep + clone at +P; module slice (8080,11930..12080] → translate +P AND clone at original position; LINEs crossing → move endpoints with x≥8080 by +P; wide LWPOLYLINE/HATCH (walkway) → vertex-wise stretch. INSERT/TEXT/MTEXT classify by insertion point (block bboxes are unreliable!). Then rename grid bubbles, update `NO OF FIELDS IN SERIES` text and TR SET table rows.
**Remove a field**: reverse (delete C-band + module, translate -P).
**Chamber duplication (width dir)**: copy plan chamber content (anchors in x[-600,8230], y[38870,46700]) shifted dy = -7705; funnels translate dy=-3852.5 then restore slope corner endpoints (top corner y=46380.3 stays; bottom corner y=39107.3 → 39107.3-7705); GD-screen verticals (span>5000) extend ymin by -7705 instead of translating; rework CLs (ctr layer). End view: entities bbox x∈(22700,38600), y<33000; chambers flush = shift second chamber to share wall; stretch crossing ground/rail lines back.
- Always render before/after (`AI KIT/render_view.py <dxf> <out.png> xmin xmax ymin ymax`) and visually compare.
- Watch for stick-font labels (letters drawn as LINEs on layer P) — they are not TEXT entities.

## 5. 3D MODEL SPECIFICATION (4-cell ESP, mm)

| Parameter | Value |
|---|---|
| Casing L × W | 16205 × 7705 |
| Casing z | 9350 → 21115 (roof deck top 21245) |
| Field pitch FP | 4051.25 (=L/4) |
| Hoppers | 4 pyramids, top 0.94FP × 0.94W at z=9350 → 600×600 at z=1700; chute 500 sq to z=900; RAV 640 sq z=520–900 |
| Funnels | casing face (z 9650–20915, full W) → nozzle 1900×1900 at ±5200 from face; flange ring beyond |
| Support | 5×2 columns 360 sq, x=i·FP, y=80 & 7265; beams z=3400, 6500, 9270; X-braces (130 wide ribbons) in 3 tiers; base plates |
| Mid platform | grating z=3400 + yellow railing |
| Roof | deck slab z 21115–21245; perimeter railing h=1050 (top+mid rail, posts @1300, toe plate); 3 blue balconies 2000×1500 on front side |
| MIGI rappers | per field: 2 rows × 5 (y=0.22W, 0.44W) orange r=70 h=850 on 270-sq white base + stem; 1 row × 3 black rods (y=0.64W) r=60 h=950 |
| TR sets | 4×, rear strip: tank 2000×1400×1090 white + rounded cap, 6 radiator fins, elbow duct r=430 (horizontal + vertical drop to deck), 2 bushings, blue skid |
| Stairs | front face y=-1500, width 1150; zigzag x 30%L↔60%L; levels 500, 3400, 6500, 9350, 12291, 15232, 18173, 21245; treads @235; blue stringers; landings 1600 long w/ grating + posts + wall struts (only above z=9350); ground entry flight |
| Walkway | full-length at z=9910 on front face + railing + struts |

Build scripts (in this folder):
- `esp3d_build_mesh.py` — 3DFACE mesh version (for colored GstarCAD DXF; export with ezdxf, `true_color` per face AND ACI layers).
- `esp3d_build_step.py` — cadquery TRUE SOLIDS version (~1014 solids) with traced logo → STEP with colors (`cq.Assembly`, one compound per color layer). `pip install cadquery shapely trimesh --break-system-packages`.

## 6. EXPORT FORMAT MATRIX (hard-won lessons)

| Target | Format | Notes |
|---|---|---|
| GstarCAD editing | DXF R2010, 3DFACE + true_color + ACI layers | Colors display ✓ |
| Autodesk web Viewer | **STEP** (from cadquery assembly) | ONLY solids show color there. 3DFACE DXF/DWG = always grey. ZIP not supported. OBJ needs .mtl uploaded together |
| Windows / PowerPoint | GLB (trimesh, PBR per-part) | double-click opens colored |
| GstarCAD solids scripting | **IMPOSSIBLE** on user's edition (LOFT blocked, BOX = mesh) |
| User's DWGs | Cannot read — request DXF save-as |

## 7. ENVIRONMENT PITFALLS

- Bash calls hard-timeout at 45 s; long renders → `timeout 43` inside; background processes DIE between calls.
- File tools ↔ bash mount can DESYNC (truncated .py) → when a written file errors nonsensically, run code via bash heredoc instead.
- OneDrive locks open files (PermissionError on overwrite) → save under a new name or retry after user closes it.
- `.dwl/.dwl2` files = GstarCAD locks, ignore. `.bak` = backups.
- Full-doc matplotlib renders of the ref DXF take ~40 s; use `render_view.py` with HatchPolicy SHOW_OUTLINE.
- ezdxf `bbox` on WD_* / RAP-PD block INSERTs is enormous — classify inserts by `dxf.insert` point, never bbox.

## 8. REGENERATION QUICKSTART

```bash
pip install ezdxf matplotlib cadquery shapely trimesh --break-system-packages
# 2D render check:
python3 "AI KIT/render_view.py" "ESP 4 CELL GA.dxf" out.png -11000 67000 -3500 52500
# 3D mesh DXF (GstarCAD): exec esp3d_build_mesh.py -> write 3DFACEs w/ true_color
# 3D STEP (viewer/solids): python3 "AI KIT/esp3d_build_step.py"  (reads logo_polys.json)
```

## 9. OPEN ITEMS (as of 2026-07-13)

- Design data values (gas flow, TR ratings, hopper volume, drawing numbers) still pending from user for the 2D GA tables — placeholders `***` in TR rows.
- 2-chamber GA: plan-view chamber gap not yet closed (only end view flush) — pending user decision.
- Hybrid arrangement (ESP + 4 cyclones) 3D not yet modeled; user's exact geometry available via GstarCAD `STLOUT` export if requested.
