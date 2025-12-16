"""MJLab Integration Example

This example demonstrates how to build muwanx projects using mjlab setups.
"""

import muwanx as mwx
from mjlab.tasks.registry import load_env_cfg, load_rl_cfg
from mjlab.tasks.velocity.config.g1.env_cfgs import unitree_g1_flat_env_cfg


def main():
    builder = mwx.Builder()
    mjlab_project = builder.add_project(name="MJLab Integration Example")
    env_cfg = load_env_cfg("Mjlab-Velocity-Flat-Unitree-G1")
    rl_cfg = load_rl_cfg("Mjlab-Velocity-Flat-Unitree-G1")


if __name__ == "__main__":
    main()