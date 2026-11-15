"""Geometry/material helpers for procedural FPS weapon models (Blender bpy, headless).

Conventions (Blender space; glTF export converts to Y-up):
  +Y = muzzle direction (glTF -Z, i.e. "forward" for a three.js/Unity-style FPS camera)
  +Z = up, +X = right side of the weapon
  Units: metres. All helper inputs are millimetres for readability.
  Weapon origin (0,0,0) = top of the pistol grip (firing-hand pivot).
"""
import bpy, bmesh, math, os
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
MM = 0.001
TEXDIR = os.path.join(HERE, 'tex')

MATS = {}
OBJS = []  # objects created for the current weapon


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MATS.clear(); OBJS.clear()


def v(*a):
    return Vector(a) * MM


# ---------------------------------------------------------------- materials
def _img(path, colorspace):
    im = bpy.data.images.load(path, check_existing=True)
    im.colorspace_settings.name = colorspace
    return im


def mat(name):
    if name in MATS:
        return MATS[name]
    m = bpy.data.materials.new('M_' + name)
    m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes['Principled BSDF']
    special = {
        'glass': dict(color=(0.02, 0.05, 0.06, 1), rough=0.03, metal=0.0, alpha=0.25),
        'lens': dict(color=(0.05, 0.10, 0.14, 1), rough=0.02, metal=0.6, alpha=0.55),
        'reticle': dict(color=(1, 0.02, 0.02, 1), rough=0.4, metal=0.0, emit=(1, 0.05, 0.03, 1), estr=8.0),
        'bore': dict(color=(0.01, 0.01, 0.01, 1), rough=0.6, metal=0.8),
    }
    if name in special:
        s = special[name]
        bs.inputs['Base Color'].default_value = s['color']
        bs.inputs['Roughness'].default_value = s['rough']
        bs.inputs['Metallic'].default_value = s['metal']
        if 'alpha' in s:
            bs.inputs['Alpha'].default_value = s['alpha']
            m.surface_render_method = 'BLENDED'
        if 'emit' in s:
            bs.inputs['Emission Color'].default_value = s['emit']
            bs.inputs['Emission Strength'].default_value = s['estr']
    else:
        tex = TEXDIR
        a = nt.nodes.new('ShaderNodeTexImage'); a.image = _img(f'{tex}/{name}_albedo.png', 'sRGB')
        o = nt.nodes.new('ShaderNodeTexImage'); o.image = _img(f'{tex}/{name}_orm.png', 'Non-Color')
        n = nt.nodes.new('ShaderNodeTexImage'); n.image = _img(f'{tex}/{name}_normal.png', 'Non-Color')
        sep = nt.nodes.new('ShaderNodeSeparateColor')
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 1.0
        nt.links.new(a.outputs['Color'], bs.inputs['Base Color'])
        nt.links.new(o.outputs['Color'], sep.inputs['Color'])
        nt.links.new(sep.outputs['Green'], bs.inputs['Roughness'])
        nt.links.new(sep.outputs['Blue'], bs.inputs['Metallic'])
        nt.links.new(n.outputs['Color'], nm.inputs['Color'])
        nt.links.new(nm.outputs['Normal'], bs.inputs['Normal'])
        # glTF exporter picks AO from a glTF Material Output group; R channel of ORM is kept in file for engines.
    MATS[name] = m
    return m


# ---------------------------------------------------------------- mesh core
def _finish(name, bm, material, smooth_angle=35):
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for f in bm.faces:
        f.smooth = True
    lim = math.radians(smooth_angle)
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0) > lim:
            e.smooth = False
        elif len(e.link_faces) != 2:
            e.smooth = False
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat(material))
    OBJS.append(ob)
    return ob


def _bevel(bm, amount, segs=2, edges=None):
    if amount <= 0:
        return
    bmesh.ops.bevel(bm, geom=list(edges if edges is not None else bm.edges), offset=amount * MM,
                    segments=segs, profile=0.5, affect='EDGES', clamp_overlap=True)


def box(name, size, center, material, bevel=1.2, segs=2, rot=(0, 0, 0)):
    """size/center in mm; rot in degrees (X,Y,Z euler)."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=Vector(size) * MM, verts=bm.verts)
    _bevel(bm, min(bevel, min(size) * 0.45), segs)
    R = _rot(rot)
    bmesh.ops.transform(bm, matrix=R, verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(center) * MM, verts=bm.verts)
    return _finish(name, bm, material)


def _rot(rot):
    rx, ry, rz = (math.radians(a) for a in rot)
    return (Matrix.Rotation(rz, 4, 'Z') @ Matrix.Rotation(ry, 4, 'Y') @ Matrix.Rotation(rx, 4, 'X'))


def profile(name, pts, thick, material, x=0.0, bevel=1.5, segs=2, rot=(0, 0, 0), origin=(0, 0, 0)):
    """Side profile polygon (y,z) in mm extruded along X (thickness mm, centred on x)."""
    bm = bmesh.new()
    vs = [bm.verts.new(((x - thick / 2) * MM, p[0] * MM, p[1] * MM)) for p in pts]
    f = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[f])
    nv = [e for e in ext['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=Vector((thick * MM, 0, 0)), verts=nv)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    _bevel(bm, min(bevel, thick * 0.45), segs)
    if any(rot):
        o = Vector(origin) * MM
        bmesh.ops.translate(bm, vec=-o, verts=bm.verts)
        bmesh.ops.transform(bm, matrix=_rot(rot), verts=bm.verts)
        bmesh.ops.translate(bm, vec=o, verts=bm.verts)
    return _finish(name, bm, material)


def lathe(name, prof, material, start, axis='Y', seg=32, rot_offset=0.0, closed=True, smooth_angle=35):
    """Revolve profile [(r, d)...] (mm) around an axis. d = distance along axis from `start` (mm).
    For solid ends make first/last r=0. For a bored tube, include the inner wall and close the loop."""
    bm = bmesh.new()
    vs = [bm.verts.new((r * MM, 0, d * MM)) for r, d in prof]
    edges = [bm.edges.new((vs[i], vs[i + 1])) for i in range(len(vs) - 1)]
    if closed and prof[0][0] > 0 and prof[-1][0] > 0:
        edges.append(bm.edges.new((vs[-1], vs[0])))
    bmesh.ops.spin(bm, geom=vs + edges, axis=(0, 0, 1), cent=(0, 0, 0), steps=seg,
                   angle=math.tau, use_duplicate=False, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    if rot_offset:
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(math.radians(rot_offset), 3, 'Z'))
    R = {'Y': Matrix.Rotation(-math.pi / 2, 4, 'X'), 'X': Matrix.Rotation(math.pi / 2, 4, 'Y'),
         'Z': Matrix.Identity(4), '-Y': Matrix.Rotation(math.pi / 2, 4, 'X')}[axis]
    bmesh.ops.transform(bm, matrix=R, verts=bm.verts)
    bmesh.ops.translate(bm, vec=Vector(start) * MM, verts=bm.verts)
    return _finish(name, bm, material, smooth_angle)


def cyl(name, r, length, start, material, axis='Y', seg=24, bevel=0.8, r2=None):
    r2 = r if r2 is None else r2
    b = min(bevel, r * 0.4, length * 0.4)
    prof = [(0, 0), (r - b, 0), (r, b), (r2, length - b), (r2 - b, length), (0, length)] if b > 0 else \
        [(0, 0), (r, 0), (r2, length), (0, length)]
    return lathe(name, prof, material, start, axis, seg)


def tube(name, r_out, r_in, length, start, material, axis='Y', seg=32, bevel=0.6):
    b = bevel
    prof = [(r_in, 0), (r_out - b, 0), (r_out, b), (r_out, length - b), (r_out - b, length), (r_in, length)]
    return lathe(name, prof, material, start, axis, seg)


def rail(name, length, start_y, z, material='anodized', width=21.2, x=0.0):
    """MIL-STD-1913 Picatinny rail segment along Y, bottom at z (mm)."""
    bm = bmesh.new()

    def addbox(sx, sy, sz, cx, cy, cz, bev):
        t = bmesh.new()
        bmesh.ops.create_cube(t, size=1.0)
        bmesh.ops.scale(t, vec=Vector((sx, sy, sz)) * MM, verts=t.verts)
        _bevel(t, bev, 1)
        bmesh.ops.translate(t, vec=Vector((cx, cy, cz)) * MM, verts=t.verts)
        me = bpy.data.meshes.new('tmp'); t.to_mesh(me); t.free(); bm.from_mesh(me); bpy.data.meshes.remove(me)

    addbox(15.6, length, 3.0, x, start_y + length / 2, z + 1.5, 0.4)          # spine
    n = int((length - 3) // 10)
    off = (length - (n * 10 - 5.23)) / 2
    for i in range(n):
        cy = start_y + off + i * 10 + 2.4
        addbox(width, 4.77, 3.6, x, cy, z + 3.0 + 1.8, 0.6)                    # crossbar (dovetail top)
    addbox(width - 4, length, 1.2, x, start_y + length / 2, z + 3.6, 0.3)
    return _finish(name, bm, material)


def boolean(target, cutter, op='DIFFERENCE'):
    m = target.modifiers.new('b', 'BOOLEAN'); m.operation = op; m.object = cutter; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = target
    for o in bpy.context.view_layer.objects: o.select_set(False)
    target.select_set(True)
    bpy.ops.object.modifier_apply(modifier=m.name)
    remove(cutter)
    return target


def remove(ob):
    if ob in OBJS: OBJS.remove(ob)
    bpy.data.objects.remove(ob, do_unlink=True)


def join(name, obs):
    obs = [o for o in obs if o is not None]
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for o in obs: o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    if len(obs) > 1:
        bpy.ops.object.join()
    ob = obs[0]; ob.name = name; ob.data.name = name
    for o in obs[1:]:
        if o in OBJS: OBJS.remove(o)
    return ob


def set_origin(ob, p_mm):
    p = Vector(p_mm) * MM
    ob.data.transform(Matrix.Translation(-p))
    ob.location = ob.location + p


def empty(name, p_mm, parent, size=0.01, rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = size; e.empty_display_type = 'ARROWS'
    bpy.context.scene.collection.objects.link(e)
    e.location = Vector(p_mm) * MM
    e.rotation_euler = [math.radians(a) for a in rot]
    e.parent = parent
    return e


def uv_all(obs, cube=180.0):
    """Box-project UVs with a fixed world texel density (cube size in mm) so tiling textures match."""
    for o in bpy.context.view_layer.objects: o.select_set(False)
    for ob in obs:
        if ob.type != 'MESH':
            continue
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.cube_project(cube_size=cube * MM, scale_to_bounds=False, correct_aspect=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        ob.select_set(False)


def assemble(wname, static, moving, sockets):
    """static: list of objects merged into <W>_Body; moving: dict partname->(obj, pivot_mm); sockets: name->pos_mm"""
    root = bpy.data.objects.new(wname, None)
    bpy.context.scene.collection.objects.link(root)
    root.empty_display_size = 0.05
    uv_all(static + [o for o, _ in moving.values()])
    body = join(f'{wname}_Body', static)
    for o in [body] + [o for o, _ in moving.values()]:
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.triangulate(bm, faces=bm.faces, quad_method='BEAUTY', ngon_method='BEAUTY')
        bm.to_mesh(o.data); bm.free()
    body.parent = root
    for part, (ob, piv) in moving.items():
        set_origin(ob, piv)
        ob.name = ob.data.name = f'{wname}_{part}'
        ob.parent = root
    for s, p in sockets.items():
        if isinstance(p, tuple) and len(p) == 2 and isinstance(p[0], tuple):
            empty(f'{wname}_Socket_{s}', p[0], root, rot=p[1])
        else:
            empty(f'{wname}_Socket_{s}', p, root)
    return root


def tri_count(root):
    dg = bpy.context.evaluated_depsgraph_get(); n = 0
    for o in [root] + list(root.children_recursive):
        if o.type == 'MESH':
            e = o.evaluated_get(dg); me = e.to_mesh(); me.calc_loop_triangles(); n += len(me.loop_triangles); e.to_mesh_clear()
    return n


def export(root, path, tex_size=None):
    for o in bpy.context.view_layer.objects: o.select_set(False)
    root.select_set(True)
    for c in root.children_recursive: c.select_set(True)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if tex_size:
        for im in bpy.data.images:
            if im.size[0] > tex_size:
                im.scale(tex_size, tex_size)
    bpy.ops.export_scene.gltf(filepath=path, use_selection=True, export_format='GLB',
                              export_image_format='JPEG', export_jpeg_quality=90,
                              export_yup=True, export_apply=True, export_extras=True,
                              export_tangents=True)


def preview(root, path, views=('side', 'persp'), res=(1100, 520), samples=24):
    """Quick Cycles CPU render of the weapon for visual checking."""
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.cycles.device = 'CPU'
    sc.render.resolution_x, sc.render.resolution_y = res
    w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.35, 0.37, 0.4, 1); bg.inputs['Strength'].default_value = 0.35
    # bounds
    pts = []
    for o in root.children_recursive:
        if o.type == 'MESH':
            pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    c = (lo + hi) / 2; L = max((hi - lo).y, (hi - lo).z * 2.2)
    for nm, loc, e in [('key', (0.8, -0.4, 1.0), 120), ('fill', (-1.0, 0.3, 0.4), 40), ('rim', (0.2, 1.2, 0.6), 90)]:
        ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = e * L; ld.size = 1.2
        lo_ = bpy.data.objects.new(nm, ld); sc.collection.objects.link(lo_)
        lo_.location = c + Vector(loc) * L * 1.5
        lo_.rotation_euler = (c - lo_.location).to_track_quat('-Z', 'Y').to_euler()
    cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
    outs = []
    for vname in views:
        if vname == 'side':
            cd.type = 'ORTHO'; cd.ortho_scale = L * 1.08
            cam.location = c + Vector((3, 0, 0)); 
        else:
            cd.type = 'PERSP'; cd.lens = 50
            cam.location = c + Vector((1.3, -0.9, 0.55)) * L
        cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
        p = path.replace('.png', f'_{vname}.png'); sc.render.filepath = p
        bpy.ops.render.render(write_still=True); outs.append(p)
    return outs
