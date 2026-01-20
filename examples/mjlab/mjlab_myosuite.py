"""MJLab Integration Example with mjlab_myosuite

This example demonstrates how to build muwanx projects using mjlab_myosuite setups.
"""

# from mjlab_myosuite.tasks.registry import load_env_cfg, load_rl_cfg

import os

import muwanx


def main():
    builder = muwanx.Builder()
    mjlab_myosuite_project = builder.add_project(  # noqa: F841
        name="MJLab Integration Example with mjlab_myosuite"
    )
    task_id = "Myosuite-Manipulation-DieReorient-Myohand"  # noqa: F841
    # env_cfg = load_env_cfg(task_id)  # noqa: F841
    # rl_cfg = load_rl_cfg(task_id)  # noqa: F841

    app = builder.build()
    if os.getenv("MUWANX_NO_LAUNCH") == "1":
        return
    app.launch()


if __name__ == "__main__":
    main()
