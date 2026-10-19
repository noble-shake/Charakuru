"""Torso weight check after weight transfer (Blender, independent of the kit code).

Finds upper-body materials (garments whose vertices sit mostly above the hips)
with vertices dominated by a leg bone, e.g. a hoodie hem bound to upper_leg,
which makes the upper and lower body split apart when walking.

Usage:
  blender -b character.blend --python weight_check.py -- [--mesh Body] [--limit 0.05] [--json out.json]
  (inside Blender, run the file with no arguments to check every skinned mesh)

Exit code 1 when an upper-body material exceeds --limit (headless only).
"""
import argparse
import json
import sys

import bpy

LEG_KEYS = ("leg", "thigh", "knee", "calf", "foot", "toe")


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--mesh", action="append", help="mesh object name (repeatable); default: all skinned meshes")
    p.add_argument("--limit", type=float, default=0.05, help="max leg-dominant vertex ratio for an upper-body material")
    p.add_argument("--json", help="write the report as JSON")
    return p.parse_args(argv)


def kind(bone_name):
    n = bone_name.lower()
    if any(k in n for k in LEG_KEYS):
        return "leg"
    return "core"


def hips_z(arm):
    for b in arm.data.bones:
        if any(k in b.name.lower() for k in ("hips", "pelvis")):
            return (arm.matrix_world @ b.head_local).z
    raise RuntimeError(f"{arm.name}: hips bone not found")


def check_mesh(obj, limit):
    """Per material: a material whose vertices sit mostly above the hips is an upper-body
    garment, so none of its vertices should follow a leg bone."""
    arm = obj.find_armature()
    hz = hips_z(arm)
    bones = {b.name for b in arm.data.bones}
    groups = {g.index: g.name for g in obj.vertex_groups if g.name in bones}
    mw = obj.matrix_world
    vmat = {}
    for poly in obj.data.polygons:
        for vi in poly.vertices:
            vmat[vi] = poly.material_index
    mats = {}
    for v in obj.data.vertices:
        ws = [(g.weight, groups[g.group]) for g in v.groups if g.group in groups and g.weight > 0.0]
        if not ws:
            continue
        z = (mw @ v.co).z
        m = mats.setdefault(vmat.get(v.index, 0), {"z": [], "leg": 0, "bands": {}})
        m["z"].append(z)
        if kind(max(ws)[1]) == "leg":
            m["leg"] += 1
            band = round(z, 1)
            m["bands"][band] = m["bands"].get(band, 0) + 1
    rows = []
    for idx, m in sorted(mats.items()):
        slot = obj.material_slots[idx].material.name if idx < len(obj.material_slots) and obj.material_slots[idx].material else f"#{idx}"
        n = len(m["z"])
        upper = sorted(m["z"])[n // 2] > hz
        ratio = m["leg"] / n
        rows.append({
            "material": slot, "n": n, "upper_body": upper, "leg_ratio": round(ratio, 3),
            "leg_bands": sorted(m["bands"].items()), "ok": not upper or ratio <= limit,
        })
    return {"mesh": obj.name, "hips_z": round(hz, 3), "rows": rows, "ok": all(r["ok"] for r in rows)}


def main():
    args = parse_args()
    names = args.mesh or [o.name for o in bpy.data.objects if o.type == "MESH" and o.find_armature()]
    report = [check_mesh(bpy.data.objects[n], args.limit) for n in names]
    for m in report:
        print(f"[{'OK' if m['ok'] else 'WARN'}] {m['mesh']} (hips z={m['hips_z']})")
        for r in m["rows"]:
            role = "upper" if r["upper_body"] else "lower"
            bands = ", ".join(f"z{z}:{c}" for z, c in r["leg_bands"]) if r["upper_body"] and r["leg_bands"] else ""
            print(f"   {'ok ' if r['ok'] else 'BAD'} {r['material']} ({role}) n={r['n']} leg-dominant={r['leg_ratio']:.0%} {bands}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    if bpy.app.background and not all(m["ok"] for m in report):
        sys.exit(1)


main()
