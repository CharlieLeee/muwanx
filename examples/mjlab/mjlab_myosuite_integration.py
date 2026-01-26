"""MJLab Integration Example with mjlab_myosuite

This example demonstrates how to build muwanx projects using mjlab_myosuite setups.
"""

import mjlab_myosuite  # noqa: F401
from mjlab.tasks.registry import list_tasks, load_env_cfg, load_rl_cfg

import muwanx


def main():
    builder = muwanx.Builder()
    mjlab_myosuite_project = builder.add_project(  # noqa: F841
        name="MJLab Integration Example with mjlab_myosuite"
    )
    task_id = "Myosuite-Manipulation-DieReorient-Myohand"
    env_cfg = load_env_cfg(task_id)  # noqa: F841
    rl_cfg = load_rl_cfg(task_id)  # noqa: F841

    print(list_tasks())


if __name__ == "__main__":
    main()
