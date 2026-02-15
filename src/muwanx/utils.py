"""Utility functions for muwanx."""

from __future__ import annotations

import os
import posixpath
import warnings
from pathlib import Path

import mujoco


def collect_spec_assets(spec: mujoco.MjSpec) -> dict[str, bytes]:
    """Collect all asset files referenced by a MjSpec from disk.

    Uses ``spec.modelfiledir``, ``spec.meshdir``, and ``spec.texturedir``
    to resolve file paths.  Returns a dictionary mapping POSIX-style relative
    paths (suitable for ZIP entries) to file contents.
    """
    base_dir = spec.modelfiledir or ""
    mesh_dir = spec.meshdir or ""
    texture_dir = spec.texturedir or ""

    assets: dict[str, bytes] = {}

    def _read(dir_hint: str, filename: str) -> None:
        if not filename:
            return
        # POSIX-style key for ZIP entries / MuJoCo asset references
        rel = posixpath.join(dir_hint, filename) if dir_hint else filename
        # OS-native path for filesystem reads
        full = os.path.join(base_dir, rel)
        if os.path.isfile(full):
            assets[rel] = Path(full).read_bytes()
        else:
            warnings.warn(
                f"Referenced asset not found: '{rel}' (resolved to '{full}')",
                category=RuntimeWarning,
                stacklevel=3,
            )

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


def name2id(name: str) -> str:
    """Convert a name to a URL-friendly identifier.

    This function normalizes names by converting them to lowercase
    and replacing spaces and hyphens with underscores, making them
    suitable for use in URLs, file paths, and identifiers.

    Args:
        name: The name to sanitize.

    Returns:
        A URL-friendly identifier string with lowercase letters,
        underscores instead of spaces and hyphens.

    Examples:
        >>> name2id("My Project")
        'my_project'
        >>> name2id("Test-Scene")
        'test_scene'
        >>> name2id("Complex Name-With Spaces")
        'complex_name_with_spaces'
    """
    return name.lower().replace(" ", "_").replace("-", "_")
