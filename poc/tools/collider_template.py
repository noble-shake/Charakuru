"""Spring-bone collider template for VRM 1.0 (Blender + VRM Add-on, independent of the kit code).

One sphere per thigh does not stop a skirt, and hair sinks into shoulders and a hood.
This adds capsules sized from the humanoid bones and links them to the springs:

  Tmpl_Legs  : thigh capsules                      -> springs whose name starts with --skirt-prefix
  Tmpl_Torso : neck-shoulder and upper-arm capsules,
               upper-chest front spheres            -> springs whose name starts with --hair-prefix

Sizes scale with the hips height, so the defaults fit other body sizes; --radius scales all radii
(the defaults were tuned on a loose hoodie, so a slim outfit may want 0.8).
Existing colliders are kept. If Tmpl_* groups already exist the script stops instead of stacking them.

Usage:
  blender -b character.blend --python collider_template.py -- --out character_colliders.blend [--radius 1.0]
  (inside Blender, run with no arguments to edit the open scene; save it yourself)
"""
import argparse
import sys
import uuid

import bpy
from mathutils import Vector

# radius / forward offset as a ratio of the hips height (tuned on a 0.815 m hips height)
THIGH_R = 0.071
NECK_SHOULDER_R = 0.096
UPPER_ARM_R = 0.104
CHEST_FRONT_R = 0.117
CHEST_SIDE_R = 0.092
CHEST_FORWARD = 0.09


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--out", help="save a copy to this .blend (required in background mode)")
    p.add_argument("--radius", type=float, default=1.0, help="multiplier for every radius")
    p.add_argument("--skirt-prefix", default="Skirt_")
    p.add_argument("--hair-prefix", default="Hair_")
    return p.parse_args(argv)


def find_rig():
    rigs = [o for o in bpy.data.objects if o.type == "ARMATURE" and hasattr(o.data, "vrm_addon_extension")]
    if len(rigs) != 1:
        raise RuntimeError(f"expected one armature with the VRM Add-on extension, found {len(rigs)}")
    return rigs[0]


def human_bone(rig, name):
    bone = getattr(rig.data.vrm_addon_extension.vrm1.humanoid.human_bones, name).node.bone_name
    if bone not in rig.data.bones:
        raise RuntimeError(f"humanoid bone '{name}' is not assigned")
    return rig.data.bones[bone]


class Builder:
    def __init__(self, rig, k):
        self.rig = rig
        self.sb = rig.data.vrm_addon_extension.spring_bone1
        self.mw = rig.matrix_world
        hips = human_bone(rig, "hips")
        self.s = (self.mw @ hips.head_local).z
        self.k = k

    def world(self, bone, t):
        """Point at ratio t along a bone, in world space."""
        return self.mw @ bone.head_local.lerp(bone.tail_local, t)

    def local(self, bone, p):
        return bone.matrix_local.inverted() @ (self.mw.inverted() @ p)

    def group(self, name):
        g = self.sb.collider_groups.add()
        g.vrm_name = name
        g.uuid = uuid.uuid4().hex
        return g

    def _add(self, group, bone, shape):
        c = self.sb.colliders.add()
        c.uuid = uuid.uuid4().hex
        c.node.bone_name = bone.name
        c.shape_type = shape
        c.reset_bpy_object(bpy.context, self.rig)
        group.colliders.add().collider_uuid = c.uuid
        return c

    def capsule(self, group, bone, a, b, ratio):
        c = self._add(group, bone, "Capsule")
        c.shape.capsule.offset = self.local(bone, a)
        c.shape.capsule.tail = self.local(bone, b)
        c.shape.capsule.radius = ratio * self.s * self.k

    def sphere(self, group, bone, p, ratio):
        c = self._add(group, bone, "Sphere")
        c.shape.sphere.offset = self.local(bone, p)
        c.shape.sphere.radius = ratio * self.s * self.k


def build(rig, args):
    b = Builder(rig, args.radius)
    if any(g.vrm_name.startswith("Tmpl_") for g in b.sb.collider_groups):
        raise RuntimeError("Tmpl_* collider groups already exist; start from a file without them")
    legs = b.group("Tmpl_Legs")
    torso = b.group("Tmpl_Torso")
    try:
        chest = human_bone(rig, "chest")
    except RuntimeError:
        chest = human_bone(rig, "spine")
    neck = human_bone(rig, "neck")
    fwd = Vector((0, -CHEST_FORWARD * b.s, 0))  # VRM characters face -Y in Blender
    for side in ("left", "right"):
        thigh = human_bone(rig, f"{side}_upper_leg")
        b.capsule(legs, thigh, b.world(thigh, 0.0), b.world(thigh, 0.9), THIGH_R)
        arm = human_bone(rig, f"{side}_upper_arm")
        b.capsule(torso, chest, b.mw @ neck.head_local, b.world(arm, 0.35), NECK_SHOULDER_R)
        b.capsule(torso, arm, b.world(arm, 0.0), b.world(arm, 0.75), UPPER_ARM_R)
        p = b.world(chest, 0.85) + fwd
        p.x = b.world(arm, 0.0).x * 0.75
        b.sphere(torso, chest, p, CHEST_SIDE_R)
    b.sphere(torso, chest, b.world(chest, 0.76) + fwd, CHEST_FRONT_R)
    linked = {"Tmpl_Legs": 0, "Tmpl_Torso": 0}
    for sp in b.sb.springs:
        for prefix, g in ((args.skirt_prefix, legs), (args.hair_prefix, torso)):
            if sp.vrm_name.startswith(prefix):
                sp.collider_groups.add().collider_group_uuid = g.uuid
                linked[g.vrm_name] += 1
    print(f"TEMPLATE hips={b.s:.3f} radius x{args.radius} colliders={len(b.sb.colliders)} springs linked={linked}")
    if 0 in linked.values():
        print("WARN some template groups are not linked to any spring; check --skirt-prefix/--hair-prefix")


def main():
    args = parse_args()
    if bpy.app.background and not args.out:
        sys.exit("--out is required in background mode")
    build(find_rig(), args)
    if args.out:
        bpy.ops.wm.save_as_mainfile(filepath=args.out, copy=True)
        print(f"SAVED {args.out}")


main()
