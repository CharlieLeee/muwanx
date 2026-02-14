"""Asset collection for MjSpec objects.

Collects all asset files (meshes, textures, heightfields, skins) referenced
by an MjSpec, reading them from disk so they can be included in .mjz archives.
"""

from __future__ import annotations

import os
from pathlib import Path

import mujoco


def collect_spec_assets(spec: mujoco.MjSpec) -> dict[str, bytes]:
    """Collect all asset files referenced by a MjSpec from disk.

    Uses ``spec.modelfiledir``, ``spec.meshdir``, and ``spec.texturedir``
    to resolve file paths.  Returns a dictionary mapping relative paths
    (as they appear in the XML) to file contents.
    """
    base_dir = spec.modelfiledir or ""
    mesh_dir = spec.meshdir or ""
    texture_dir = spec.texturedir or ""

    assets: dict[str, bytes] = {}

    def _read(dir_hint: str, filename: str) -> None:
        if not filename:
            return
        rel = os.path.join(dir_hint, filename) if dir_hint else filename
        full = os.path.join(base_dir, rel)
        if os.path.isfile(full):
            assets[rel] = Path(full).read_bytes()

    # Meshes
    for mesh in spec.meshes:
        _read(mesh_dir, mesh.file)

    # Textures (single file and cube-map faces)
    for texture in spec.textures:
        _read(texture_dir, texture.file)
        for i in range(len(texture.cubefiles)):
            _read(texture_dir, texture.cubefiles[i])

    # Heightfields
    for hfield in spec.hfields:
        _read("", hfield.file)

    # Skins
    for skin in spec.skins:
        _read("", skin.file)

    return assets
